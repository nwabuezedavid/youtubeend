from http.server import BaseHTTPRequestHandler
import json
from pytubefix import YouTube


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            content_length = int(
                self.headers['Content-Length']
            )

            body = self.rfile.read(
                content_length
            )

            data = json.loads(body)

            url = data.get("url")

            if not url:
                self.send_response(400)
                self.send_header(
                    'Content-type',
                    'application/json'
                )
                self.end_headers()

                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "No URL provided"
                }).encode())

                return

            yt = YouTube(url)

            stream = yt.streams.get_highest_resolution()

            response = {
                "success": True,
                "title": yt.title,
                "video_url": stream.url
            }

            self.send_response(200)
            self.send_header(
                'Content-type',
                'application/json'
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header(
                'Content-type',
                'application/json'
            )
            self.end_headers()

            self.wfile.write(json.dumps({
                "success": False,
                "error": str(e)
            }).encode())