{% from "img.j2" import side_by_side_images %}
{% from "s3.j2" import s3_img %}
---
Title: Preventing a pull request from being merged until it's safe
Date: 2023-07-25
Category: programming
Description: I'll demonstrate a simple technique relying on Github Actions and pull request labels to block a pull request from being merged, until deemed safe to do so.
Summary: Sometimes, a pull request is ready to go, but shouldn't be merged before some other changes are merged first. While the patch is valid on its own, it might depend on other changes, and could even break the application if merged _before_ the other. I'll demonstrate a simple technique relying on Github Actions and pull request labels to block a pull request from being merged, until deemed safe to do so.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/do-not-merge/required-checks.png
hide_image: True
Tags:
Keywords: Github, Pull Request, CI/CD
---

Sometimes, a pull request is ready to go, but shouldn't be merged before some other changes are merged first. While the patch is valid on its own, it might depend on other changes, and could even break the application if merged _before_ the other.

I'll demonstrate a simple technique relying on Github Actions and pull request labels to fully block a pull request from being merged until deemed safe (at least without some admin privileges on the repository).

First, we introduce a Github Actions [workflow](https://github.com/brouberol/5esheets/blob/main/.github/workflows/fail-if-do-not-merge-label.yml) executed when a pull request is opened, labeled or unlabeled. This workflow will fail if labeled with `do not merge`.

```yaml
name: Check do not merge

on:
  # Check label at every push in a feature branch
  push:
    branches-ignore:
      - main
  # Check label during the lifetime of a pull request
  pull_request:
    types:
    - opened
    - labeled
    - unlabeled

jobs:
  fail-for-do-not-merge:
    if: contains(github.event.pull_request.labels.*.name, 'do not merge')
    runs-on: ubuntu-latest
    steps:
      - name: Fail if PR is labeled with do not merge
        run: |
          echo "This PR can't be merged, due to the 'do not merge' label."
          exit 1
```

We then define a branch protection rule for our `main` branch, by going to the repository `Settings`, then `Branches`. We add a new rule if none exist, tick ` Require status checks to pass before merging`, and add the `fail-for-do-not-merge` to the list of required checks.

Finally, apply the `do not merge` label to your pull request.

{{ side_by_side_images("do-not-merge", "required-checks.webp", "labels.webp", style_1="flex: 70%", style_2="flex: 30%")}}

At that point, the `fail-for-do-not-merge` check will run and fail, preventing the PR to be merged.

{{ s3_img("do-not-merge", "merge-blocked.webp") }}

When the pull request is finally safe to merge, simply remove the `do not merge` tag, and the checks will automagically pass, thus allowing you to merge.

{{ s3_img("do-not-merge", "passing-checks.webp") }}