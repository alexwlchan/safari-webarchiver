#!/usr/bin/env swift
/// Save a web page as a Safari webarchive.
///
/// Usage: save_safari_webarchive [URL] [OUTPUT_PATH]
///
/// This will save the page to the desired file, but may fail for
/// several reasons:
///
///   - the web page can't be loaded
///   - the web page returns a non-200 status code
///   - there's already a file at that path (it won't overwrite an existing
///     webarchive)
///
/// For a detailed explanation of the code in this script, see
/// https://alexwlchan.net/2024/creating-a-safari-webarchive/

import WebKit

/// Print an error message and terminate the process if there are
/// any errors while loading a page.
class ExitOnFailureDelegate: NSObject, WKNavigationDelegate {
  var urlString: String

  init(_ urlString: String) {
    self.urlString = urlString
  }

  func webView(
    _ webView: WKWebView,
    didFail: WKNavigation!,
    withError error: Error
  ) {
    fputs("Failed to load \(self.urlString) (1): \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _ webView: WKWebView,
    didFailProvisionalNavigation: WKNavigation!,
    withError error: Error
  ) {
    fputs("Failed to load \(self.urlString) (2): \(error.localizedDescription)\n", stderr)
    exit(1)
  }

  func webView(
    _ webView: WKWebView,
    decidePolicyFor navigationResponse: WKNavigationResponse,
    decisionHandler: (WKNavigationResponsePolicy) -> Void
  ) {
    if let httpUrlResponse = (navigationResponse.response as? HTTPURLResponse) {
      if httpUrlResponse.statusCode != 200 {
        fputs("Failed to load \(self.urlString): got status code \(httpUrlResponse.statusCode)\n", stderr)
        exit(1)
      }
    }

    decisionHandler(.allow)
  }
}

let webView = WKWebView()

extension WKWebView {

  /// Load the given URL in the web view.
  ///
  /// This method will block until the URL has finished loading.
  func load(_ urlString: String) {
    let delegate = ExitOnFailureDelegate(urlString)
    webView.navigationDelegate = delegate

    if let url = URL(string: urlString) {
      let request = URLRequest(url: url)
      self.load(request)

      while (self.isLoading) {
        RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
      }
    } else {
      fputs("Unable to use \(urlString) as a URL\n", stderr)
      exit(1)
    }
  }

  /// Save a copy of the web view's contents as a webarchive file.
  ///
  /// This method will block until the webarchive has been saved,
  /// or the save has failed for some reason.
  func saveAsWebArchive(savePath: URL) {
    var isSaving = true

    self.createWebArchiveData(completionHandler: { result in
      do {
        let data = try result.get()
        try data.write(
          to: savePath,
          options: [Data.WritingOptions.withoutOverwriting]
        )
        isSaving = false
      } catch {
        fputs("Unable to save webarchive file: \(error.localizedDescription)\n", stderr)
        exit(1)
      }
    })

    while (isSaving) {
      RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.1))
    }
  }
}

guard CommandLine.arguments.count == 3 else {
    fputs("Usage: \(CommandLine.arguments[0]) <URL> <OUTPUT_PATH>\n", stderr)
    exit(1)
}

let urlString = CommandLine.arguments[1]
let savePath = URL(fileURLWithPath: CommandLine.arguments[2])

webView.load(urlString)
webView.saveAsWebArchive(savePath: savePath)

print("Saved webarchive to \(savePath)")
