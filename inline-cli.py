#!/usr/bin/env python

import argparse

import requests

def inline(filename, owner, repo, pr, auth):
    messages = parse(filename)
    post_comments(messages, owner, repo, pr, auth)

def parse(filename):
    messages = []
    return messages

def post_comments(messages, owner, repo, pr, auth):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--owner', type=str, required=True)
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--auth', type=str, required=True)
    parser.add_argument('--filename', type=str, required=True)

    args = parser.parse_args()
    inline(args.filename, args.owner, args.repo, args.pr, args.auth)
