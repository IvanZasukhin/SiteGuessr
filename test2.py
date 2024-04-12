from pywebcopy import save_webpage, save_website
# pip install lxml-html-clean


def webpage(url, folder, name):
    save_webpage(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=False,
        threaded=False,
    )


def website(url, folder, name):
    save_website(
        url=url,
        project_folder=folder,
        project_name=name,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=False,
    )


webpage('https://ya.ru/', 'E://Python save/SiteGuessr', 'yandex')
