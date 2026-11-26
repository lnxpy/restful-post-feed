## RESTful Post Feed
A GitHub Action that updates the `Recent Posts` section of your README file by listening to a RESTful API endpoint with the help of GitHub Actions. (Like RSS feed updaters)

This repository helps you in case of showing your weblog's recent posts on your profile README file so then users will be able to check your latest activities.

### Prerequisites
- A RESTful endpoint that responds JSON data.
- Profile readme for showing the result. (`username/username/README.md`)
- Patience.

### Usage
Add the `<!--POSTS:START-->` and `<!--POSTS:END-->` markers around your posts section and let the action take care of the rest. No files need to be copied into your repository anymore.

#### 1. Add the recent posts section
Open up your `README.md` file in a text editor and add the following snippet somewhere in your readme file.
```html
# My Recent Posts
<!--POSTS:START-->
<!--POSTS:END-->
```

#### 2. Create the CI workflow
Create the `.github/workflows/` directory in your repository and add a workflow file like the following one.
```yml
name: RESTful Post Feed Updater

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-posts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Updating the posts section
        id: feed
        uses: lnxpy/restful-post-feed@v1
        with:
          endpoint: 'https://api.example.com/posts'
          title: 'title'
          url_pattern: 'https://blog.example.com/post/{slug}'
          url_keys: 'slug'
          posts_count: '5'

      - name: Commit files
        if: steps.feed.outputs.updated == 'true'
        run: |
          git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add .
          if ! git diff-index --quiet HEAD; then
            git commit -m "README updated"
          fi
          git push
```

You're done. The workflow will be triggered every 6 hours. You can change it from the `schedule` section in the yaml file.

#### 3. Inputs
| Input          | Required | Default              | Description                                                              |
| :------------- | :------: | :------------------: | :----------------------------------------------------------------------- |
| `endpoint`     | Yes      | -                    | The RESTful endpoint that responds the JSON data of your posts.          |
| `title`        | Yes      | -                    | The title field name in the returned JSON objects.                       |
| `url_pattern`  | Yes      | -                    | A Python format pattern used to build each post URL.                     |
| `url_keys`     | No       | `url`                | Comma-separated replacement field names for the URL pattern.             |
| `posts_count`  | No       | `0`                  | Maximum number of posts to render. Set to `0` to render all posts.       |
| `file_path`    | No       | `README.md`          | Path of the target file containing the markers.                          |
| `start_marker` | No       | `<!--POSTS:START-->` | The start HTML-comment marker of the posts section.                      |
| `end_marker`   | No       | `<!--POSTS:END-->`   | The end HTML-comment marker of the posts section.                        |

The action also exposes two step outputs: `updated` (`true`/`false`) and `count` (number of rendered posts).

### Legacy Usage (copying the updater directory)
The old way of copying the `feed_updater` directory into your repository, configuring `feed_updater/settings.py`, and running `feed_updater/updater.py` through the `workflows/post-section-updater.yml` workflow still works, but it is now deprecated in favor of the reusable action described above.

### Example Repository
[Here is an example repository that uses the same structure for updating the `Recent Posts` section of the readme file](https://github.com/lnxpy/test-feed). You can refer to that repository anytime.

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=lnxpy&repo=test-feed)](https://github.com/lnxpy/test-feed)
