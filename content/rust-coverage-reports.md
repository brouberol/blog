Title: Measuring the coverage of a rust program in Github Actions
Date: 2022-04-26
Category: programming
Description: In this article, I will go through how I set up code coverage measurement for `bo`, my text editor written in Rust, and publicly hosted the coverage report on S3.
Summary: In this article, I will go through how I set up code coverage measurement for `bo`, my text editor written in Rust, and publicly hosted the coverage report on S3.
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/rust-coverage/cov.webp
hide_image: True
Tags: rust
Keywords: github, gitub-actions, coverage, ci

After having faced a couple of of regressions in [`bo`](https://github.com/brouberol/bo) (my personal text editor [written in Rust](/metaprocrastinating-on-writing-a-book-by-writing-a-text-editor)) in the past couple of days, I have tried to increase the number of unit tests related to the codebase sections handling navigation. I already had some unit tests, but I needed to know what lines of code were _not_ tested, to know what area of the codebase I needed to focus on.

To do this, I used Mozilla's excellent [`grcov`](https://github.com/mozilla/grcov) project. I followed their instructions and ran the following commands locally, in my work directory.

```console
$ export RUSTFLAGS="-Cinstrument-coverage"
$ cargo build
$ export LLVM_PROFILE_FILE="bo-%p-%m.profraw"
$ cargo test
$ grcov . -s . --binary-path ./target/debug/ -t html --branch --ignore-not-existing -o ./target/debug/coverage/
$ open ./target/debug/coverage/index.html
```

This way, I got a beautiful HTML report in which I could see my code coverage, either global, file by file,

![Coverage report](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/rust-coverage/cov.webp)

or line by line.

![Coverage report](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/rust-coverage/cov2.webp)

`grcov` even generates nice SVG badges displaying the coverage score, that I could display on the project homepage!

What I ultimately wanted though, was to have every commit touching my `main` branch to trigger a new coverage generation report, that I could host somewhere public and read at leisure when I needed to.

To do so, I set-up a publicly accessible s3 bucket, configured to host a static website, which turns out to be remarkably easy to do [in terraform](https://github.com/brouberol/infrastructure/commit/75192443319f36cfbdfbcee0086322c958e3cc82#diff-abe63f10056054dcb55782e4be3ccb2ec28b47e6192b3ee1b45e46ff1884738aR62-R74):

```terraform
resource "aws_s3_bucket" "github-brouberol-coverage" {
  bucket        = "my-bucket-name"
  provider      = aws.euwest
  acl           = "public-read"
  force_destroy = false
  versioning {
    enabled    = false
    mfa_delete = false
  }
  website {
    index_document = "index.html"
  }
}
```

I then created an AWS user, associated with an AWS access_key/secret_key pair and the following IAM policy, granting that user read/write permissions on that S3 bucket, and nothing else.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::<my-bucket-name>",
                "arn:aws:s3:::<my-bucket-name>/*"
            ]
        }
    ]
}
```

I then had to store the bucket name, keypair and AWS region name as encrypted secrets in the `bo` [repository](https://github.com/brouberol/bo), by going to `Settings > Secrets > Actions > New repository secret`.

![Secrets](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/rust-coverage/secrets.webp)

Once that was all set up, the project CI (Github Actions) needed to perform the [following actions](https://github.com/brouberol/bo/blob/main/.github/workflows/tests.yml#L28-L77):

- running the unit tests with profiling and coverage collection enabled

```yaml
- name: Run tests
  uses: actions-rs/cargo@v1
  with:
    command: test
    args: --all-features --no-fail-fast  # Customize args for your own needs
  env:
    CARGO_INCREMENTAL: '0'
    RUSTFLAGS: |
      -Zprofile -Ccodegen-units=1 -Cinline-threshold=0 -Clink-dead-code
      -Coverflow-checks=off -Cpanic=abort -Zpanic_abort_tests -Cinstrument-coverage
    RUSTDOCFLAGS: |
      -Zprofile -Ccodegen-units=1 -Cinline-threshold=0 -Clink-dead-code
      -Coverflow-checks=off -Cpanic=abort -Zpanic_abort_tests -Cinstrument-coverage'
```

- generating the coverage report using `grcov`, using the [`actions-rs/grcov`](https://github.com/actions-rs/grcov/) action.

```yaml
- name: Gather coverage data
  id: coverage
  uses: actions-rs/grcov@v0.1
```

- measuring the total coverage score, and report it in a check, if the job is associated to a pull request

```yaml
- name: Report coverage in PR status for the current commit
  if: github.ref_name != 'main'
  run: |
    set -eu
    total=$(cat ${COV_REPORT_DIR}/badges/flat.svg | egrep '<title>coverage: ' | cut -d: -f 2 | cut -d% -f 1 | sed 's/ //g')
    curl -s "https://brouberol:${GITHUB_TOKEN}@api.github.com/repos/brouberol/bo/statuses/${COMMIT_SHA}" -d "{\"state\": \"success\",\"target_url\": \"https://github.com/brouberol/bo/pull/${PULL_NUMBER}/checks?check_run_id=${RUN_ID}\",\"description\": \"${total}%\",\"context\": \"Measured coverage\"}"
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    COMMIT_SHA: ${{ github.event.pull_request.head.sha }}
    RUN_ID: ${{ github.run_id }}
    PULL_NUMBER: ${{ github.event.pull_request.number }}
    COV_REPORT_DIR: ${{ steps.coverage.outputs.report }}
```

![Secrets](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/rust-coverage/cov3.webp)

- uploading the whole HTML coverage report to S3, using the [jakejarvis/s3-sync-action](https://github.com/jakejarvis/s3-sync-action ) action. We only do this for commits belonging the `main` branch (_i.e._ direct pushes or after a pull request was merged).

```yaml
- name: "Upload the HTML coverage report to S3"
  if: github.ref_name == 'main'
  uses: jakejarvis/s3-sync-action@master
  with:
    args: --acl public-read --follow-symlinks --delete
  env:
    AWS_S3_BUCKET: ${{ secrets.AWS_BUCKET }}
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: ${{ secrets.AWS_REGION }}
    SOURCE_DIR: ${{ steps.coverage.outputs.report }}
    DEST_DIR: 'bo'
```

With all of that set up, the coverage report is now [available publicly](http://github-brouberol-coverage.s3-website.eu-west-3.amazonaws.com/bo/), refreshed every time a new commit hits `main`, and I even get a coverage shield for free! ![coverage shield](https://github-brouberol-coverage.s3.eu-west-3.amazonaws.com/bo/badges/flat.svg)