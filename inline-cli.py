#!/usr/bin/env python

from __future__ import print_function
import argparse
import pprint
import subprocess

import github3
import unidiff

def inline(filename, owner, repo, pr, user, token, debug=False):
    gh = github3.GitHub(user, token=token)

    pull_request = gh.pull_request(owner, repo, pr)
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
    diff = pull_request.diff()

    messages = parse(filename, diff)
    if not debug:
        post_comments(messages, pull_request, sha)
    else:
        for m in messages:
            if m:
                print('file: {0}\tmsg: {1}'.format(m['filename'], m['content'].replace('\n', '')))


def message(filename, line, content, diff):
    if content:
        patch = unidiff.PatchSet(diff.decode('utf-8').split('\n'))
        for patched_file in patch:
            if patched_file.target_file == 'b/' + filename:
                offset = 1
                for hunk_no, hunk in enumerate(patched_file):
                    for position, hunk_line in enumerate(hunk):
                        if '+' not in hunk_line.line_type:
                            continue
                        if hunk_line.target_line_no == line:
                            return {
                                'filename': filename,
                                'line': position + offset,
                                'content': 'Line: ' + str(line) + ' \n```\n' + content.strip() + '\n```'
                            }
                    offset += len(hunk) + 1


def parse(filename, diff):
    messages = []
    current_filename = ''
    current_line = ''
    current_message_content = ''
    with open(filename) as infile:
        for line in infile:
            # new filename
            if not line.startswith(' '):
                messages.append(message(current_filename, current_line, current_message_content, diff))
                current_filename = line.strip()
                current_line = ''
                current_message_content = ''
                continue
            # new line number
            elif not line.startswith('    '):
                messages.append(message(current_filename, current_line, current_message_content, diff))
                current_line = int(line.replace('  Line: ', '').strip())
                current_message_content = ''
                continue
            # new content
            current_message_content += line

    return messages


def post_comments(messages, pull_request, sha):
    for msg in messages:
        if not msg:
            continue
        pull_request.create_review_comment(msg['content'], sha, msg['filename'], msg['line'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--owner', type=str, required=True)
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--token')
    parser.add_argument('--user', type=str)
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    inline(args.filename, args.owner, args.repo, args.pr, args.user, args.token, args.debug)
