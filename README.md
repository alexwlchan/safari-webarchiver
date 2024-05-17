# safari-webarchiver

This tool creates [Safari webarchive files](https://en.wikipedia.org/wiki/Webarchive) on the command line.
This gives you an offline archive of web pages, which can be stored and backed up independently of any cloud services.

```console
$ save_safari_webarchive "https://example.com" "example.webarchive"
```

These archives are the same as those created by the `File > Save As…` menu item, but now you can create them programatically and in bulk.

## How it works

It opens the given URL in a `WKWebView`, calls `createWebArchiveData` to create a webarchive file, and saves it to disk.
That's the core workflow, and then there's a bunch of error handling around that.

For a more detailed explanation of this code, see <https://alexwlchan.net/2024/creating-a-safari-webarchive/>

## Installation

### Install from source

1.  Install the Xcode Command Line Tools
2.  Download the `save_safari_webarchive.swift` script from this repo
3.  Compile the script into a binary:

    ```console
    $ swiftc save_safari_webarchive.swift
    ```

4.  Copy the compiled binary `save_safari_webarchive` to somewhere in your PATH.

### Install a compiled binary

1.  Find the latest [GitHub release](https://github.com/alexwlchan/safari-webarchiver/releases)
2.  Download the zip file which is appropriate for your system (Intel = `x86_64`, Apple Silion = `aarch64`)
3.  Open the zip file, and add the `save_safari_webarchive` app to your PATH

The app is just a compiled version of the Swift script.
It isn't notarised, so when you run it, you may get a warning that this app is from an unidentified developer.
You can get around this by right-clicking the app icon in Finder, and choosing `Open` from the shortcut menu.

## Usage

Run the script passing two arguments: the URL you want to archive, and the path where you want to save the webarchive file.

For example, this command will save the URL to this GitHub repo to `safari-webarchiver.webarchive`:

```console
$ save_safari_webarchive "https://github.com/alexwlchan/safari-webarchiver" "safari-webarchiver.webarchive"
```

## Acknowledgements

This is partially inspired by [a similar script](https://github.com/newzealandpaul/webarchiver) written in 2008 by newzealandpaul.
