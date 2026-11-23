from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Tag


def normalize_url(url):
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main_section = soup.find("main")
    if isinstance(main_section, Tag):
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")

    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = [a["href"] for a in soup.find_all("a", href=True)]
    return [urljoin(base_url, url) for url in urls]


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    images = [img["src"] for img in soup.find_all("img", src=True)]
    return [urljoin(base_url, img) for img in images]
