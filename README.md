## RESTful Post Feed
A workflow that updates your `Recent Posts` section of `README.md` listening to a REST API endpoint other than a SOAP one with the help of GitHub Actions. (Like RSS feed updaters)

This repository helps you in case of showing your weblog's recent posts on your profile README file so then users will be able to check your latest activities.

### Prequirement
- A RESTful endpoint that responses JSON data.
- Profile readme for showing the result. (`username/username/README.md`)
- Patience.

### Usage
All you need is to clone this repository and copy the `feed_updater` directory right in the root path of your repository. Once you did that, you need to add the `Recent Posts` section for updates. Finally, you create the workflow.

#### 1. Clone this repository
Before you clone this repository, make sure you have your own reposotory already cloned locally.
```shell
git clone https://github.com/<username>/<username> && git clone https://github.com/lnxpy/restful-post-feed
```
Then, copy the required directory as follows.
```shell
cp -r restful-post-feed/feed_updater <username>
```

#### 2. Add the recent posts section 
Once you get your repository ready, open up the `<username>/README.md` file in a text editor and add the following snippet somewhere in your readme file.
```html
# My Recent Posts
<!--POSTS:START-->
<!--POSTS:END-->
```

#### 3. Configurations
Open up the `<username>/feed_updater/settings.py` file for some basic configuration. Here is a simple hint for a correct configuration.
```python
config = {
    'endpoint': '',     # --> the restful endpoint that responses the JSON data (your posts)
    'title': '',        # --> the title field name in the returned JSON data
    'url': {
        'pattern': '',  # --> a python pattern to redirect users to the post index
        'keys': [],     # --> replacement fields for the pattern
    }
}
```

#### 4. CI Workflow
Simply create the `<username>/.github/workflows/` directory and copy the original workflow.
```shell
mkdir -p <username>/.github/workflows/ && cp restful-post-feed/workflows/post-section-updater.yml <username>/.github/workflows/
```

You're done. Workflow will be trigger every 6 hours. You can change it from the `schedule` section in the yaml file.

### Example Repository
[Here is an example repository that uses the same structure for updating the `Recent Posts` section of the readme file](https://github.com/lnxpy/test-feed). You can refer to that repository anytime.

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=lnxpy&repo=test-feed)](https://github.com/lnxpy/test-feed)
