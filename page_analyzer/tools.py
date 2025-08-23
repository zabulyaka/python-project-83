def get_url_raw(form_data):
    url_raw = form_data.get('url')
    return url_raw


def get_url_id(url, urls_data):
    u_filtered = list(filter(lambda url_data: url_data['name'] == url,
        urls_data))
    url_data = u_filtered[0]
    url_id = url_data['id']
    return url_id


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
