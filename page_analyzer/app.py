import os
#import psycopg2
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
#    get_form_data,
    get_url_norm,
    get_url_id,
    set_url_data,
    get_url_raw,
    url_is_already_added
)
from validators import url as is_url
from urllib.parse import urlparse
from page_analyzer.repo import UrlsRepository
#from datetime import datetime


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
INCORRECT_URL_MSG = 'Некорректный URL'
URL_ALREADY_EXISTS_MSG = 'Страница уже существует'
URL_ADDED_MSG = 'Страница успешно добавлена'
CHECK_ERROR_MSG = 'Произошла ошибка при проверке'
ERROR = 307
SUCCESS = 301
#conn = psycopg2.connect(DATABASE_URL)
#urls_repo = UrlsRepository(conn)
#urls_repo.create_table()

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

#@app.route('/urls/<id>', methods=['POST'])
#def url_exists_already(id):
#    url = urls_repo.find_url(id)
#    return render_template(
#        'new.html',
#        url=url
#    )

@app.route('/urls/<id>', methods=['GET', 'POST'])
def url_new(id):
#    conn = psycopg2.connect(DATABASE_URL)
#    urls_repo = UrlsRepository(conn)
    urls_repo = UrlsRepository(DATABASE_URL)
    url = urls_repo.find_url(id)
    messages = get_flashed_messages(with_categories=True)
    checks = urls_repo.get_url_checks(id)
#    url = {'id': 1, 'name': 'lala', 'created_at': 'hm'}
#    conn.close()
    return render_template(
        'new.html',
        url=url,
        messages=messages,
        checks=checks
    )

@app.route('/', methods=['POST'])
def url_add():
#    form_data = request.form.to_dict()['url']
#    form_data = get_form_data(request)
    form_data = request.form.to_dict()
    url_raw = get_url_raw(form_data)
#    return render_template('test.html', data=form_data['url'])
#    if not is_url(form_data):
    if not is_url(url_raw):
#        flash('Некорректный URL', 'error')
        flash(INCORRECT_URL_MSG, 'error')
        return redirect(url_for('url_error'), code=ERROR)
#    url_data = urlparse(form_data)
    url_data = urlparse(url_raw)
#    url_norm = f'{url_data.scheme}://{url_data.hostname}'
    url_norm = get_url_norm(url_data)
#    conn = psycopg2.connect(DATABASE_URL)
#    urls_repo = UrlsRepository(conn)
    urls_repo = UrlsRepository(DATABASE_URL)
    urls_data = urls_repo.get_urls()
#    urls = map(lambda url: url['name'], urls_data)
#    if url_norm in urls:
    if url_is_already_added(url_norm, urls_data):
        flash(URL_ALREADY_EXISTS_MSG, 'warning')
        id = get_url_id(url_norm, urls_data)
#        id = list(filter(lambda url: url['name'] == url_norm, urls_data))[0]['id']
#        return redirect(url_for('url_exists_already', id), code=409)
#       ADD FLASHED
        return redirect(url_for('url_new', id=id), code=SUCCESS)
    flash(URL_ADDED_MSG, 'success')
#    today = datetime.today().strftime('%Y-%m-%d')
#    today = datetime.now().strftime('%Y-%m-%d')
#    url_data = {'name': url_norm, 'created_at': today}
#    url_data = (url_norm, today)
#    url_data = (url_norm,)
    url_data = set_url_data(url_norm)
    id = urls_repo.add_url(url_data)
#    conn.close()
    return redirect(url_for('url_new', id=id), code=SUCCESS)

@app.route('/urls')
def urls_show():
    #urls = [{'id': 1, 'url': 'lala', 'last_checked': 'hm', 'code_response': 404}]
#    conn = psycopg2.connect(DATABASE_URL)
#    urls_repo = UrlsRepository(conn)
    urls_repo = UrlsRepository(DATABASE_URL)
    urls_data = urls_repo.get_urls()
#    conn.close()
    return render_template(
        'show.html',
        urls=urls_data
    )

@app.route('/urls/<id>/checks', methods=['POST'])
def url_check_new(id):
    urls_repo = UrlsRepository(DATABASE_URL)
    url_data = urls_repo.find_url(id)
    url = url_data['name']
    try:
        req = requests.get(url)
        req.raise_for_status()
    except requests.RequestException as e:
        flash(CHECK_ERROR_MSG, 'error')
        return redirect(url_for('url_new', id=id), code=ERROR)
#    except requests.exceptions.HTTPError as e:
#        return redirect(url_for('index'))
#    except requests.exceptions.ConnectionError as e:
#        return redirect(url_for('index'))
    check_data = (id, req.status_code, 'd', 'e', 'y')
    urls_repo.add_url_check(check_data)
#    return render_template('test.html', data=req.status_code)
#    urls_repo = UrlsRepository(DATABASE_URL)
#    urls_repo.add_url_check(id)
    return redirect(url_for('url_new', id=id), code=SUCCESS)
