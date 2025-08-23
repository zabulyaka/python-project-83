from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_url_norm(url):
    url_data = urlparse(url)
    return f'{url_data.scheme}://{url_data.hostname}'

def extract_html_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else ''
    if not title:
        title = ''
    h1 = soup.h1.string if soup.h1 else ''
    metas = soup.find_all('meta')
    metas_filtered = list(filter(lambda meta: meta.get('name') == 'description', metas))
    desc_content = ''
    if metas_filtered:
        description = metas_filtered[0]
        desc_content = description.get('content')
    return (h1, title, desc_content)
