import unittest

from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url_with_https(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_without_protocol(self):
        input_url = "www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self) -> None:
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self) -> None:
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_whitespace(self) -> None:
        input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Whitespace Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_basic(self) -> None:
        input_body = "<html><body><p>This is the first paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self) -> None:
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self) -> None:
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>No links here</p></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_both(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><img src="https://crawler-test.com/image.jpg"></body></html>'
        )
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/image.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_none(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_mixed(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/image.jpg"><img src="/image.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/image.jpg",
            "https://crawler-test.com/image.jpg",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/image.jpg"><img src="https://crawler-test.com/image.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/image.jpg",
            "https://crawler-test.com/image.jpg",
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
