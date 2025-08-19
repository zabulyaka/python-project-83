def get_form_data(request):
    return request.form.to_dict()['url']

def get_norm_url(url_data):
    return f'{url_data.scheme}://{url_data.hostname}'

def get_url_id(url, urls_data):
    urls_filtered = filter(lambda url_data: url_data['name'] == url, urls_data)
    url_data = list(urls_filtered)[0]
    url_id = url_data['id']
    return url_id

def url_is_already_added(url, urls_data):
    urls = map(lambda url_data: url_data['name'], urls_data)
    return url in urls

def set_url_data(url):
    return (url,)
