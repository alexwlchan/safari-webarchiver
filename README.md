# safari-webarchiver

This tool creates [Safari webarchive files](https://en.wikipedia.org/wiki/Webarchive) on the command line.
This gives you an offline archive of web pages, which can be stored and backed up independently of any cloud services.

```console
$ save_safari_webarchive.swift "https://example.com" "example.webarchive"
```

These archives are the same as those created by the `File > Save As…` menu item, but now you can create them programatically and in bulk.

## How it works

It opens the given URL in a `WKWebView`, calls `createWebArchiveData` to create a webarchive file, and saves it to disk.
That's the core workflow, and then there's a bunch of error handling around that.

For a more detailed explanation of this code, see <https://alexwlchan.net/2024/creating-a-safari-webarchive/>

## Installation

1.  Install the Xcode Command Line Tools
2.  Download the `save_safari_webarchive.swift` script from this repo
3.  Add the script somewhere in your PATH

You may also want to compile the script into a binary, and add the binary to your PATH instead:

```console
$ swiftc save_safari_webarchive
```

## Usage

Run the script passing two arguments: the URL you want to archive, and the path where you want to save the webarchive file.

For example, this command will save the URL to this GitHub repo to `safari-webarchiver.webarchive`:

```console
$ save_safari_webarchive.swift "https://github.com/alexwlchan/safari-webarchiver" "safari-webarchiver.webarchive"
```

It will refuse to overwrite a webarchvie that

## Acknowledgements

This is partially inspired by [a similar script](https://github.com/newzealandpaul/webarchiver) written in 2008 by newzealandpaul.
