import re
from requests import get

from patterns.markdown import post_item
from settings import config

import json
from operator import itemgetter


def main():
    content = ''
    list_of_posts = []

    response = get(config['endpoint']).json()

    with open('README.md', 'r') as original_file:
        content = original_file.read()

    g = itemgetter(*config['url']['keys'])
    
    for post in response:
        list_of_posts.append(
            post_item.format(
                    post[config['title']],
                    config['url']['pattern'].format(*g(post))
            )
        )

    with open('README.md', 'w') as f:
        f.write(
            re.sub(
                r'(<!--POSTS:START-->\n).*?(<!--POSTS:END-->)',
                r'\1{}\2'.format('\n'.join(list_of_posts)),
                content,
                flags=re.MULTILINE|re.DOTALL)
        )

main()
