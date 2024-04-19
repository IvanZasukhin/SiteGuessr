import os, sys, re
import requests
import itertools

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from forms.answer import AnswerForm
from flask import Flask, render_template, abort, redirect, make_response, jsonify, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'


def savePage(url, pagepath):
    def savenRename(soup, pagefolder, session, url, tag, inner):
        if not os.path.exists(pagefolder):
            os.mkdir(pagefolder)
        for res in soup.findAll(tag):
            if tag == 'title':
                res.string = 'Title'
            elif tag == 'style':
                try:
                    text = res.string.strip()
                    if 'url' in text:
                        index = 0
                        s = re.search("(url\(+)(?!\")([^)]*)", text)
                        while s:
                            urls = text[s.start() + 4 + index: s.end() + index]
                            filename = urls.split('/')[-1]
                            filepath = os.path.join(pagefolder, filename)
                            fileurl = urljoin(url, urls)
                            res.string = (res.string[:s.start() + 5 + index] + '../' +
                                          os.path.join(pagefolder, filename).replace('\\', '/') +
                                          res.string[s.end() + index + 1:])
                            if not os.path.isfile(filepath):
                                with open(filepath, 'wb') as f:
                                    filebin = session.get(fileurl)
                                    f.write(filebin.content)

                            index += s.end()
                            s = re.search("(url\(+)(?!\")([^)]*)", text[index:])
                            # s = re.search(r"url\([^)]*\)", text[index:])

                except Exception as exc:
                    res.string = text
                    print(exc, file=sys.stderr)

            elif res.has_attr(inner):
                try:
                    filename, ext = os.path.splitext(os.path.basename(res[inner]))
                    if '?' in ext:
                        ext = ext[:ext.find('?')]
                    filename = re.sub('\W+', '', filename) + ext
                    fileurl = urljoin(url, res.get(inner))
                    filepath = os.path.join(pagefolder, filename)
                    res[inner] = '../' + os.path.join(pagefolder, filename).replace('\\', '/')
                    if tag == 'img':
                        if res.has_attr('srcset'):
                            res.attrs['srcset'] = ''

                    if not os.path.isfile(filepath):  # was not downloaded
                        with open(filepath, 'wb') as file:
                            filebin = session.get(fileurl)
                            file.write(filebin.content)

                except Exception as exc:
                    print(exc, file=sys.stderr)

    def try_delete_logo(soup):
        for res in soup.findAll():
            if res.attrs:
                for attr in res.attrs:
                    if 'logo' in attr:
                        res.string = ''
                        break
                    elif res.has_attr('class'):
                        for cl in res.attrs['class']:
                            if 'logo' in cl:
                                res.string = ''
                                break

    path, _ = os.path.splitext(pagepath)
    pagefolder = 'static/' + path + '_files'
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src', 'style': '', 'title': ''}
    for tag, inner in tags_inner.items():  # saves resource files and rename refs
        savenRename(soup, pagefolder, session, url, tag, inner)

    titles = list(map(''.join, itertools.product(*zip(pagepath.upper(), pagepath.lower()))))
    for res in soup.find_all():
        if res.text and res.string:
            text = res.string
            for title in titles:
                if title in text:
                    text = text.replace(title, '*Title*')
            res.string.replace_with(text)

    header = soup.find('header')
    if header:
        try_delete_logo(header)
    footer = soup.find('footer')
    if footer:
        try_delete_logo(footer)

    with open(os.path.join('templates', f'{path}.html'), 'w') as file:
        file.write(
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'.rstrip(
                '\r\n') + '\n' + '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>'.rstrip(
                '\r\n') + '\n')

    with open(os.path.join('templates', f'{path}.html'), 'ab') as file:
        file.write(soup.prettify('utf-8'))

    with open(os.path.join('templates', f'{path}.html'), 'a') as file:
        file.write('<style>a {pointer-events: none;} button {pointer-events: none;}</style>\n')
        file.write('{% block content %} {% endblock %}')


@app.route("/game/<title>", methods=['GET', 'POST'])
def game(title):
    form = AnswerForm()
    params = {"title": title,
              "pagefolder": "discord_files",
              "form": form}
    if form.validate_on_submit():
        if form.title.data.lower() == title:
            return redirect("/game")
        else:
            params["message"] = "Неверное имя сайта"
        return render_template('answer.html', **params)
    return render_template("answer.html", **params)


# savePage('https://www.yahoo.com/', 'yahoo')
# savePage('https://www.wikipedia.org/', 'wiki')
# savePage('https://www.reddit.com/', 'reddit')
savePage('https://github.com/', 'github')
savePage('https://discord.com/', 'discord')
app.run(port=8087, host='127.0.0.1')
