from http.server import BaseHTTPRequestHandler
import json
import requests
from pytubefix import YouTube


class handler(BaseHTTPRequestHandler):

    # HANDLE CORS
    def do_OPTIONS(self):

        self.send_response(200)

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

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

                self.send_header(
                    "Access-Control-Allow-Origin",
                    "*"
                )

                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "success": False,
                        "error": "No URL provided"
                    }).encode()
                )

                return

            yt = YouTube(url)

            stream = yt.streams.get_highest_resolution()

            video_response = requests.get(
                stream.url,
                stream=True
            )

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "video/mp4"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{yt.title}.mp4"'
            )

            self.end_headers()

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

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "success": False,
                    "error": str(e)
                }).encode()
            )