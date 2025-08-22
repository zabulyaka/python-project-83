from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_url_raw(form_data):
    url_raw = form_data.get('url')
    return url_raw
#    return request.form.to_dict()['url']

#def get_url_norm(url_data):
def get_url_norm(url):
    url_data = urlparse(url)
    return f'{url_data.scheme}://{url_data.hostname}'

def get_url_id(url, urls_data):
    urls_filtered = filter(lambda url_data: url_data['name'] == url, urls_data)
    url_data = list(urls_filtered)[0]
    url_id = url_data['id']
    return url_id

def extract_html_info(html):
    soup = BeautifulSoup(html, 'html.parser')
#    return soup.prettify()
    title = soup.title.string if soup.title else ''
#    soup.get('title')
    h1 = soup.h1.string if soup.h1 else ''
#    description = soup.find(name='description')
#    desc_content = description['content'] if description else ''
#    desc_content = description.get('content')
    metas = soup.find_all('meta')
    metas_filtered = filter(lambda meta: meta.get('name') == 'description', metas)
    description = list(metas_filtered)[0]
#    description = list(filter(lambda meta: meta.get('name') == 'description', metas))[0]
    desc_content = description.get('content')
    return (h1, title, desc_content) 

def url_is_already_added(url, urls_data):
    urls = map(lambda url_data: url_data['name'], urls_data)
    return url in urls

def set_url_data(url):
    return (url,)

def norm_urls_data(urls):
    urls_copy = urls.copy()
    for url in urls_copy:
        if url['created_at'] is None:
            url['created_at'] = ''
        if url['status_code'] is None:
            url['status_code'] = ''
    return urls_copy
