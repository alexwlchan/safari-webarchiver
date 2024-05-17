# CONTRIBUTING

## Creating a new release

1.  Bump the version number in `save_safari_webarchive.swift`
2.  Add a changelog entry in `CHANGELOG.md`
3.  Create a Git tag with your new version number
4.  Push your changes and Git tag to GitHub

GitHub Actions will create a new release, including compiled binaries.

These binaries aren't notarised -- see https://github.com/alexwlchan/safari-webarchiver/issues/6
