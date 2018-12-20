import argparse
from os import walk
from pathlib import Path, PurePath
from docutils.core import publish_string

import markdown

from bottle import Bottle, static_file, redirect
from bottle import jinja2_template as template

DIRECTORY = None

app = Bottle()

def is_md(file):
    """Simple check for filtering
    """
    if ".md" in file or \
     ".rst" in file:
        return True
    else:
        return False

@app.route('/')
def index():
    """Index route

    Serves md/rst files from current directory
    """
    files = []
    for (_, dir_names, file_names) in walk(DIRECTORY):
        files.extend(list(map(lambda x: (DIRECTORY.joinpath(x), x), dir_names)))
        files.extend(list(map(lambda x : (DIRECTORY.joinpath(x), x), filter(is_md,file_names))))
        break
    return template("index.html", files=files)

@app.route('/static/<file_path:path>')
def server_static(file_path):
    """Static files(css)
    """
    path = PurePath(__file__).parent.joinpath("static")
    return static_file(file_path, root=path)

@app.route("/<path:path>")
def serve_md(path):
    """Serve child directories or md/rst files
    """
    if Path(path).is_dir():
        files = []
        if "md_files" == path:
            redirect("/")
        files.append((PurePath(path).parent, ".."))
        path = PurePath(path)
        for (_, dir_names, file_names) in walk(path):
            files.extend(list(map(lambda x: (path.joinpath(PurePath(x).name), PurePath(x).name), dir_names)))
            files.extend(list(map(lambda x: (path.joinpath(x), PurePath(x).name), filter(is_md,file_names))))
            break
        return template("index.html", files=files)
    if is_md(path):
        if ".md" in path:
            with open(path) as md:
                html = markdown.markdown(md.read(), extensions=['codehilite', 'fenced_code'])
        else:
            with open(path) as rst:
                html = publish_string(rst.read(), writer_name='html').decode()
        return template("markdown.html", html=html, path=path)
    else:
        return template("nope.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve markdown/rst files in a browser as html")
    parser.add_argument("--directory", help="Serve md files from this directory, if not passed uses current directory")
    parser.add_argument('--host', default="localhost", help="Host ip/name. Default localhost.")
    parser.add_argument('--port', default=8080, type=int, help="Port number on which to serve. Default 8080.")
    parser.add_argument('--server', default="wsgiref", help="Serve to use like paste, etc. Default wsgiref.")
    args = parser.parse_args()
    DIRECTORY = PurePath(args.directory) if args.directory else None
    app.run(server=args.server, host=args.host, port=args.port)
