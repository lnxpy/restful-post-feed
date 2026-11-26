"""
Update the posts section of a Markdown file from a RESTful endpoint.

Designed to run inside the "RESTful Post Feed" composite GitHub Action.
All inputs are read from the INPUT_* environment variables that the
action runtime exposes from the action's `inputs` block.
"""

import json
import os
import re
import sys
from operator import itemgetter

import requests


def fail(message: str) -> None:
    print(f'::error::{message}')
    sys.exit(1)


def get_input(name: str, default: str = '') -> str:
    return os.environ.get(f'INPUT_{name.upper()}', default).strip()


def fetch_posts(endpoint: str):
    print(f'Fetching posts from {endpoint}')
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        fail(f'Fetching/parsing the endpoint failed: {exc}')

    posts = payload
    if isinstance(posts, dict):
        for key in ('posts', 'results', 'items', 'data'):
            if isinstance(posts.get(key), list):
                posts = posts[key]
                break
        else:
            fail(
                'The endpoint must respond with a JSON array, or an object '
                'holding an array under "posts", "results", "items", or "data".'
            )

    if not isinstance(posts, list):
        fail('The endpoint must respond with a JSON array of post objects.')

    return posts


def render_lines(posts, title_field: str, url_pattern: str, url_keys):
    lines = []
    for post in posts:
        try:
            title = post[title_field]
        except (TypeError, KeyError):
            fail(f'The "{title_field}" field is missing in at least one post item.')

        url = None
        try:
            # named fields, e.g. 'https://blog.example.com/post/{slug}'
            url = url_pattern.format(**post)
        except IndexError:
            # legacy positional fields, e.g. 'https://blog.example.com/post/{0}'
            try:
                url = url_pattern.format(*itemgetter(*url_keys)(post))
            except (TypeError, KeyError, IndexError) as exc:
                fail(f'Resolution of URL keys {url_keys} failed for an item: {exc}')
        except KeyError as exc:
            # a named field missing in the item — fall back to the legacy style
            try:
                url = url_pattern.format(*itemgetter(*url_keys)(post))
            except (TypeError, KeyError, IndexError) as exc2:
                fail(
                    f'Resolution of URL keys {url_keys} failed for an item: '
                    f'{exc} | {exc2}'
                )
        except TypeError as exc:
            fail(f'Post item is not a JSON object: {exc}')

        lines.append(f'- [{title}]({url})')
    return lines


def main():
    endpoint = get_input('endpoint')
    title_field = get_input('title')
    url_pattern = get_input('url_pattern')
    url_keys = [k for k in get_input('url_keys', 'url').split(',') if k.strip()] or ['url']
    posts_count = int(get_input('posts_count', '0') or 0)
    file_path = get_input('file_path', 'README.md')
    start_marker = get_input('start_marker', '<!--POSTS:START-->')
    end_marker = get_input('end_marker', '<!--POSTS:END-->')

    if not endpoint:
        fail('The `endpoint` input is required.')
    if not title_field:
        fail('The `title` input is required.')
    if not url_pattern:
        fail('The `url_pattern` input is required.')

    posts = fetch_posts(endpoint)
    if posts_count > 0:
        posts = posts[:posts_count]
    lines = render_lines(posts, title_field, url_pattern, url_keys)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError as exc:
        fail(f'Cannot read {file_path}: {exc}')

    pattern = re.compile(
        re.escape(start_marker) + r'[\s\S]*?' + re.escape(end_marker)
    )
    if not pattern.search(content):
        fail(
            f'Markers not found in {file_path}. Add `{start_marker}` and '
            f'`{end_marker}` around your posts section first.'
        )

    posts_block = '\n'.join(lines)
    replacement = f'{start_marker}\n{posts_block}\n{end_marker}' if posts_block \
        else f'{start_marker}\n{end_marker}'

    new_content = pattern.sub(lambda _: replacement, content)
    changed = new_content != content

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Posts section updated in {file_path} with {len(lines)} post(s).')
    else:
        print(f'No changes detected in {file_path}.')

    output_path = os.environ.get('GITHUB_OUTPUT')
    if output_path:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(f'updated={"true" if changed else "false"}\n')
            f.write(f'count={len(lines)}\n')


if __name__ == '__main__':
    main()
