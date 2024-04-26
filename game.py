import itertools
import os
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def save_and_rename(soup, pagefolder, session, url, tag, inner):
    if not os.path.exists(pagefolder):
        os.mkdir(pagefolder)
    for res in soup.findAll(tag):
        if tag == 'link' and res.has_attr('rel'):
            if res.attrs['rel'] == 'icon':
                res.string = ''
        if tag == 'title':
            res.string = 'Title'
        elif tag == 'base':
            res.extract()
        elif tag == 'style':
            if res.string:
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
                            localpath = '../../' + os.path.join(pagefolder, filename).replace('\\', '/')
                            text = (text[:s.start() + 4 + index] + localpath + text[s.end() - 1 + index + 1:])
                            if not os.path.isfile(filepath):
                                with open(filepath, 'wb') as f:
                                    filebin = session.get(fileurl)
                                    f.write(filebin.content)

                            index += s.end() - (len(urls) - len(localpath))
                            s = re.search("(url\(+)(?!\")([^)]*)", text[index:])
                        res.string = text
                except Exception:
                    res.string = text

        elif res.has_attr(inner):
            try:
                filename, ext = os.path.splitext(os.path.basename(res[inner]))
                if '?' in ext:
                    ext = ext[:ext.find('?')]
                filename = re.sub('\W+', '', filename) + ext
                fileurl = urljoin(url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)
                res[inner] = '../../' + os.path.join(pagefolder, filename).replace('\\', '/')
                if tag == 'img':
                    if res.has_attr('srcset'):
                        res.attrs['srcset'] = ''

                if not os.path.isfile(filepath):  # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
            except Exception:
                pass


# def try_delete_logo(soup):
#     for res in soup.findAll():
#         if res.attrs:
#             for attr in res.attrs:
#                 if 'logo' in attr:
#                     res.string = ''
#                     break
#                 elif res.has_attr('class'):
#                     for cl in res.attrs['class']:
#                         if 'logo' in cl:
#                             res.string = ''
#                             break


def save_page(url, pagepath):
    path, _ = os.path.splitext(pagepath)
    pagefolder = os.path.join('static', f'{path}_files')
    session = requests.Session()
    try:
        response = session.get(url)
    except requests.exceptions.ConnectionError:
        return
    soup = BeautifulSoup(response.content.decode('utf-8'), "html.parser")
    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src', 'style': '', 'title': '', 'base': ''}
    for tag, inner in tags_inner.items():  # saves resource files and rename refs
        save_and_rename(soup, pagefolder, session, url, tag, inner)

    titles = list(map(''.join, itertools.product(*zip(pagepath.upper(), pagepath.lower()))))
    for res in soup.find_all():
        if res.text and res.string and res.name != 'style' and res.name != 'script':
            text = res.string
            for title in titles:
                if title in text:
                    text = text.replace(title, '*Title*')
            res.string.replace_with(text)

    with open(os.path.join('templates', f'{path}.html'), 'w') as file:
        file.write(
            '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'.rstrip(
                '\r\n') + '\n' + '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>'.rstrip(
                '\r\n') + '\n')

    with open(os.path.join('templates', f'{path}.html'), 'ab') as file:
        file.write(soup.prettify('utf-8'))

    with open(os.path.join('templates', f'{path}.html'), 'a') as file:
        file.write('<style>a {pointer-events: none;} button {pointer-events: none;}</style>\n')
        file.write('<$ block content $> <$ endblock $>')
