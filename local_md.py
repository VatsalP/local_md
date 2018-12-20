import argparse
from os import walk
from pathlib import Path, PurePath
from docutils.core import publish_string

import markdown

from bottle import route, run, static_file
from bottle import jinja2_template as template

DIRECTORY = None

def is_md(file):
    if ".md" in file or \
     ".rst" in file:
        return True
    else:
        False

@route('/')
def index():
    files = []
    for (_, dir_names, file_names) in walk(DIRECTORY):
        files.extend(list(map(lambda x: (DIRECTORY.joinpath(x), x), dir_names)))
        files.extend(list(map(lambda x : (DIRECTORY.joinpath(x), x), filter(is_md,file_names))))
        break
    return template("index.html", files=files)

@route('/static/<file_path:path>')
def server_static(file_path):
    path = PurePath(__file__).parent.joinpath("static")
    return static_file(file_path, root=path)

@route("/<path:path>")
def serve_md(path):
    if Path(path).is_dir():
        files = []
        path = PurePath(path)
        for (_, dir_names, file_names) in walk(path):
            files.extend(list(map(lambda x: (path.joinpath(PurePath(x).name), PurePath(x).name), dir_names)))
            files.extend(list(map(lambda x: (path.joinpath(x), PurePath(x).name), filter(is_md,file_names))))
            break
        return template("index.html", files=files)
    if is_md(path):
        if ".md" in path:
            with open(path) as md:
                html = markdown.markdown(md.read(), extensions=['codehilite'])
        else:
            with open(path) as rst:
                html = publish_string(rst.read(), writer_name='html').decode()
        return template("markdown.html", html=html, path=path)
    else:
        return template("nope.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve markdown files in a browser as html")
    parser.add_argument("--directory", help="Serve md files from this directory, if not passed uses current directory")
    args = parser.parse_args()
    DIRECTORY = PurePath(args.directory) if args.directory else None
    run(host='localhost', port=8080, debug=True, reloader=True)
