from http.server import BaseHTTPRequestHandler
import json
import re
from pytubefix import YouTube


class handler(BaseHTTPRequestHandler):

    # =========================
    # HANDLE CORS
    # =========================
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

    # =========================
    # HANDLE POST REQUEST
    # =========================
    def do_POST(self):

        try:

            # GET BODY LENGTH
            content_length = int(
                self.headers.get('Content-Length', 0)
            )

            # READ BODY
            body = self.rfile.read(
                content_length
            )

            # PARSE JSON
            data = json.loads(body)

            # GET URL
            url = data.get("url")

            # VALIDATE URL
            if not url:

                self.send_response(400)

                self.send_header(
                    "Content-Type",
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

            # CREATE YOUTUBE OBJECT
            yt = YouTube(url)

            # GET HIGHEST QUALITY STREAM
            stream = yt.streams.get_highest_resolution()

            # CLEAN FILE NAME
            safe_title = re.sub(
                r'[\\\\/*?:"<>|]',
                "",
                yt.title
            )

            # RESPONSE
            response = {
                "success": True,
                "title": safe_title,
                "download_url": stream.url,
                "thumbnail": yt.thumbnail_url,
                "author": yt.author,
                "length": yt.length
            }

            # SEND SUCCESS RESPONSE
            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.send_header(
                "Access-Control-Allow-Origin",
                "*"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        except Exception as e:

            # ERROR RESPONSE
            self.send_response(500)

            self.send_header(
                "Content-Type",
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