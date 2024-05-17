# safari-webarchiver

This tool creates [Safari webachive files](https://en.wikipedia.org/wiki/Webarchive) on the command line.
This gives you an offline archive of web pages, which can be stored and backed up independently of any cloud services.

```console
$ ./save_safari_webarchive.swift "https://example.com" "example.webarchive"
```

## Installation

1.  Install the Xcode Command Line Tools
2.  Download the `save_safari_webarchive.swift` script from this repo
3.  Add the script somewhere in your PATH

## Usage

Run the script passing two arguments: the URL you want to archive, and the path where you want to save the webarchive file.

For example, this command will save the URL to this GitHub repo to `safari-webarchiver.webarchive`:

```console
$ ./save_safari_webarchive.swift "https://github.com/alexwlchan/safari-webarchiver" "safari-webarchiver.webarchive"
```

## Acknowledgements

This is partially inspired by [a similar script](https://github.com/newzealandpaul/webarchiver) written in 2008 by newzealandpaul.
