import os
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    render_template,
    request,
    redirect,
    url_for
)
from page_analyzer.tools import (
    get_url_id,
    set_url_data,
    norm_urls_data,
    get_url_raw,
    url_is_already_added
)
from page_analyzer.parse import (
    get_url_norm,
    extract_html_info
)
from validators import url as is_url
from page_analyzer.repo import UrlsRepository


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
INCORRECT_URL_MSG = 'Некорректный URL'
URL_ALREADY_EXISTS_MSG = 'Страница уже существует'
URL_ADDED_MSG = 'Страница успешно добавлена'
URL_CHECKED_MSG = 'Страница успешно проверена'
CHECK_ERROR_MSG = 'Произошла ошибка при проверке'
ERROR = 307
SUCCESS = 301


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/urls', methods=['POST'])
def url_error():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )

@app.route('/urls/<id>', methods=['GET', 'POST'])
def url_new(id):
    urls_repo = UrlsRepository(DATABASE_URL)
    url = urls_repo.find_url(id)
    messages = get_flashed_messages(with_categories=True)
    checks = urls_repo.get_url_checks(id)
    return render_template(
        'new.html',
        url=url,
        messages=messages,
        checks=checks
    )

@app.route('/', methods=['POST'])
def url_add():
    form_data = request.form.to_dict()
    url_raw = get_url_raw(form_data)
    if not is_url(url_raw):
        flash(INCORRECT_URL_MSG, 'error')
        return redirect(url_for('url_error'), code=ERROR)
    url_norm = get_url_norm(url_raw)
    urls_repo = UrlsRepository(DATABASE_URL)
    urls_data = urls_repo.get_urls()
    if url_is_already_added(url_norm, urls_data):
        flash(URL_ALREADY_EXISTS_MSG, 'warning')
        id = get_url_id(url_norm, urls_data)
        return redirect(url_for('url_new', id=id), code=SUCCESS)
    flash(URL_ADDED_MSG, 'success')
    url_data = set_url_data(url_norm)
    id = urls_repo.add_url(url_data)
    return redirect(url_for('url_new', id=id), code=SUCCESS)

@app.route('/urls')
def urls_show():
    urls_repo = UrlsRepository(DATABASE_URL)
    urls_data = urls_repo.get_urls()
    urls_data_norm = norm_urls_data(urls_data)
    return render_template(
        'show.html',
        urls=urls_data_norm
    )

@app.route('/urls/<id>/checks', methods=['POST'])
def url_check_new(id):
    urls_repo = UrlsRepository(DATABASE_URL)
    url_data = urls_repo.find_url(id)
    url = url_data['name']
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.RequestException:
        flash(CHECK_ERROR_MSG, 'error')
        return redirect(url_for('url_new', id=id), code=ERROR)
    flash(URL_CHECKED_MSG, 'success')
    html_info = extract_html_info(req.text)
    check_data = (id, req.status_code, *html_info)
    urls_repo.add_url_check(check_data)
    return redirect(url_for('url_new', id=id), code=SUCCESS)
