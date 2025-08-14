import os
import psycopg2
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
from validators import url as is_url
from urllib.parse import urlparse
from page_analyzer.repo import UrlsRepository
from datetime import datetime


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
urls_repo = UrlsRepository(conn)

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

@app.route('/urls/<id>')
def url_new(id):
    url = urls_repo.find_url(id)
    messages = get_flashed_messages(with_categories=True)
#    url = {'id': 1, 'name': 'lala', 'created_at': 'hm'}
    return render_template(
        'new.html',
        url=url,
        messages=messages
    )

@app.route('/', methods=['POST'])
def url_add():
    form_data = request.form.to_dict()['url']
#    return render_template('test.html', data=form_data['url'])
    if not is_url(form_data):
        flash('Некорректный URL', 'error')
        return redirect(url_for('url_error'), code=307)
    url = urlparse(form_data)
    url_norm = f'{url.scheme}://{url.hostname}'
    urls_data = urls_repo.get_urls()
    urls = map(lambda url: url['name'], urls_data)
    if url_norm in urls:
        flash('Страница уже существует', 'warning')
        id = list(filter(lambda url: url['name'] == url_norm, urls_data))[0]['id']
#        return redirect(url_for('url_exists_already', id), code=409)
#       ADD FLASHED
        return redirect(url_for('url_new', id=id), code=409)
    flash('Страница успешно добавлена', 'success')
#    today = datetime.today().strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
#    url_data = {'name': url_norm, 'created_at': today}
    url_data = (url_norm, today)
    id = urls_repo.add_url(url_data)
    return redirect(url_for('url_new', id=id), code=300)

@app.route('/urls')
def urls_show():
    #urls = [{'id': 1, 'url': 'lala', 'last_checked': 'hm', 'code_response': 404}]
    urls_data = urls_repo.get_urls()
    return render_template(
        'show.html',
        urls=urls_data
    )
