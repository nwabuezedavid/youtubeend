from http.server import BaseHTTPRequestHandler
import json
import requests
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
                    "Content-type",
                    "application/json"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "success": False,
                        "error": "No URL provided"
                    }).encode()
                )

                return

            # GET VIDEO
            yt = YouTube(url)

            stream = yt.streams.get_highest_resolution()

            # FETCH VIDEO BINARY
            video_response = requests.get(
                stream.url,
                stream=True
            )

            # SEND VIDEO DIRECTLY
            self.send_response(200)

            self.send_header(
                "Content-Type",
                "video/mp4"
            )

            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{yt.title}.mp4"'
            )

            self.end_headers()

            # STREAM VIDEO
            for chunk in video_response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    self.wfile.write(chunk)

        except Exception as e:

            self.send_response(500)

            self.send_header(
                "Content-type",
                "application/json"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode()
            )