import re
from requests import get

from patterns.markdown import post_item
from settings import config

import json


def main():
    content = ''
    list_of_posts = []

    #r = get(config['endpoint']).json()
    with open('test.json', 'r') as f:
        r = json.load(f)

    with open('../README.md', 'r') as original_file:
        content = original_file.read()

    for post in r:
        list_of_posts.append(
            post_item.format(
                    post[config['title']],
                    'link' # --> post['lang'], post['slug']
            )
        )

    with open('../README.md', 'w') as f:
        f.write(
            re.sub(
                r'(<!--POSTS:START-->\n).*?(\n<!--POSTS:END-->)',
                r'\1{}\2'.format('\n'.join(list_of_posts)),
                content,
                flags=re.MULTILINE|re.DOTALL)
        )

main()