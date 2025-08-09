import os
import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from validators import url as is_url
from urllib.parse import urlparse
from repo import UrlsRepository
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
    return render_template(
        'index.html'
    )

#@app.route('/urls/<id>', methods=['POST'])
#def url_exists_already(id):
#    url = urls_repo.find_url(id)
#    return render_template(
#        'new.html',
#        url=url
#    )

@app.route('urls/<id>')
def url_new(id):
    url = urls_repo.find_url(id)
    return render_template(
        'new.html',
        url=url
    )

@app.route('/', methods=['POST'])
def url_add():
    form_data = request.form
    if not is_url(form_data):
        return redirect(url_for('url_error'), code=422)
    url = urlparse(form_data)
    url_norm = f'{url.scheme}://{url.hostname}'
    urls_data = urls_repo.get_urls()
    urls = map(lambda url: url['name'], urls_data)
    if url_norm in urls:
        id = filter(lambda url: url['name'] == url_norm, urls_data)[0]['id']
#        return redirect(url_for('url_exists_already', id), code=409)
#       ADD FLASHED
        return redirect(url_for('url_new', id), code=409)
    today = datetime.today().strftime('%Y-%m-%d')
    url_data = {'name': url_norm, 'created_at': today}
    id = urls_repo.add_url(url_data)
    return redirect(url_for('url_new', id), code=300)

@app.route('/urls')
def sites_show():
    sites = [{'id': 1, 'url': 'lala', 'last_checked': 'hm', 'code_response': 404}]
    return render_template(
        'show.html',
        sites=sites
    )
