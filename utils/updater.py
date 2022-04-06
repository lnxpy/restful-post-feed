import re
from requests import get

def main():
    content = ''
    list_of_posts = []
    md_pattern = '- [{}](https://alirezayahyapour.pythonanywhere.com/{}/{}/)'

    r = get('https://alirezayahyapour.pythonanywhere.com/api/v1/posts/').json()

    with open('README.md', 'r') as original_file:
        content = original_file.read()

    for post in r:
        list_of_posts.append(
            md_pattern.format(post['title'], post['lang'], post['slug'])
        )

    with open('README.md', 'w') as f:
        f.write(
            re.sub(
                r'(<!--POSTS:START-->\n).*?(\n<!--POSTS:END-->)',
                r'\1{}\2'.format('\n'.join(list_of_posts)),
                content,
                flags=re.MULTILINE|re.DOTALL)
        )

def main2():
    import os
    print('READING FROM: {}'.format(os.environ['ENDPOINT']))
    print('TITLE IS: {}'.format(os.environ['TITLE']))
    print('URL IS: {}'.format(os.environ['URL']))

main2()