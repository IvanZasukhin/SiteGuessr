import os, sys, re
import requests
import itertools

from urllib.parse import urljoin
from bs4 import BeautifulSoup


def savePage(url, pagepath):
    def savenRename(soup, pagefolder, session, url, tag, inner):
        if not os.path.exists(pagefolder):  # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag):  # images, css, etc..
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
                            res.string = res.string[:s.start() + 5 + index] + './' + str(
                                os.path.join(os.path.basename(pagefolder),
                                             filename)).replace('\\', '/') + res.string[s.end() + index + 1:]
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

            elif res.has_attr(inner):  # check inner tag (file object) MUST exists
                try:
                    filename, ext = os.path.splitext(os.path.basename(res[inner]))  # get name and extension
                    if '?' in ext:
                        ext = ext[:ext.find('?')]
                    filename = re.sub('\W+', '', filename) + ext  # clean special chars from name
                    fileurl = urljoin(url, res.get(inner))
                    filepath = os.path.join(pagefolder, filename)
                    # rename html ref so can move html and folder of files anywhere
                    res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                    if not os.path.isfile(filepath):  # was not downloaded
                        with open(filepath, 'wb') as file:
                            filebin = session.get(fileurl)
                            file.write(filebin.content)

                except Exception as exc:
                    print(exc, file=sys.stderr)

    def delete_logo(soup):
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
    pagefolder = path + '_files'
    session = requests.Session()
    # ... whatever other requests config you need here
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
        delete_logo(header)
    footer = soup.find('footer')
    if footer:
        delete_logo(footer)

    with open(path + '.html', 'wb') as file:  # saves modified html doc
        file.write(soup.prettify('utf-8'))

    with open(path + '.html', 'a') as file:
        file.write('<style>a {pointer-events: none;} button {pointer-events: none;}</style>\n ')


savePage('https://www.yahoo.com/', 'yahoo')
savePage('https://www.wikipedia.org/', 'wiki')
savePage('https://www.reddit.com/', 'reddit')
savePage('https://github.com/', 'github')
savePage('https://discord.com/', 'discord')
