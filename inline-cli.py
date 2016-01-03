#!/usr/bin/env python

import argparse
import subprocess

import github3


def inline(filename, owner, repo, pr, user, token):
    gh = github3.login(user, token=token)
    messages = parse(filename)
    post_comments(messages, owner, repo, pr, gh)


def message(filename, line, content):
    return {
        'filename': filename,
        'line': line,
        'content': content
    }


def parse(filename):
    messages = []
    current_filename = ''
    current_line = ''
    current_message_content = ''
    with open(filename) as infile:
        for line in infile:
            # new filename
            if not line.startswith(' '):
                messages.append(message(current_filename, current_line, current_message_content))
                current_filename = line.strip()
                current_line = ''
                current_message_content = ''
                continue
            # new line number
            elif not line.startswith('    '):
                messages.append(message(current_filename, current_line, current_message_content))
                current_line = int(line.replace('  Line: ', '').strip())
                current_message_content = ''
                continue
            # new content
            current_message_content += line

    return messages


def post_comments(messages, owner, repo, pr, gh):
    pull_request = gh.pull_request(owner, repo, pr)
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    for msg in messages:
        if msg:
            pull_request.create_review_comment(msg['content'], sha, msg['filename'], msg['line'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--owner', type=str, required=True)
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--token', type=str)
    parser.add_argument('--user', type=str)
    parser.add_argument('--filename', type=str, required=True)

    args = parser.parse_args()
    inline(args.filename, args.owner, args.repo, args.pr, args.user, args.token)
