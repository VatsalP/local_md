# Local Markdown file server

Serves local mardown or rst files in browser

Installation:
```
$ pip install -r requirements.txt
$ python local_md.py -h
usage: local_md.py [-h] [--directory DIRECTORY] [--host HOST] [--port PORT]
                   [--server SERVER]

Serve markdown/rst files in a browser as html

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Serve md files from this directory, if not passed uses
                        current directory
  --host HOST           Host ip/name. Default localhost.
  --port PORT           Port number on which to serve. Default 8080.
  --server SERVER       Serve to use like paste, etc. Default wsgiref.
```

CSS theme used: [modest.css](https://github.com/markdowncss/modest)
