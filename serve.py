#!/usr/bin/env python3
"""Serve Evergreen locally with byte-range support for video playback."""
import argparse
import errno
import functools
import http.server
import pathlib
import re
import threading
import webbrowser

class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range = None
        path = pathlib.Path(self.translate_path(self.path))
        range_header = self.headers.get('Range')
        if not range_header or not path.is_file():
            return super().send_head()
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header.strip())
        size = path.stat().st_size
        if not match or not any(match.groups()) or size == 0:
            self.send_response(416)
            self.send_header('Content-Range', 'bytes */{}'.format(size))
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        first, last = match.groups()
        start = int(first) if first else max(0, size - int(last))
        end = min(int(last), size - 1) if first and last else size - 1
        if start > end or start >= size:
            self.send_response(416)
            self.send_header('Content-Range', 'bytes */{}'.format(size))
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        stream = path.open('rb')
        self.byte_range = (start, end)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Range', 'bytes {}-{}/{}'.format(start, end, size))
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        stream.seek(start)
        return stream

    def copyfile(self, source, outputfile):
        if not self.byte_range:
            return super().copyfile(source, outputfile)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        while remaining:
            chunk = source.read(min(65536, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            error_page = pathlib.Path(self.directory) / '404.html'
            if error_page.exists():
                body = error_page.read_bytes()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    handler = functools.partial(PreviewHandler, directory=str(root))
    try:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError as error:
        if error.errno != errno.EADDRINUSE:
            raise
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    url = 'http://127.0.0.1:{}/'.format(server.server_port)
    print('\nEvergreen website: ' + url, flush=True)
    print('Keep this window open. Press Ctrl+C to stop.\n', flush=True)
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nWebsite server stopped.')
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
