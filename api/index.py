from http.server import BaseHTTPRequestHandler
import json
import re
from pytubefix import YouTube


class handler(BaseHTTPRequestHandler):

    # =========================
    # CORS
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
    # GET REQUEST
    # =========================
    def do_GET(self):

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
            json.dumps({
                "success": True,
                "message": "YouTube Downloader API is running"
            }).encode("utf-8")
        )

    # =========================
    # POST REQUEST
    # =========================
    def do_POST(self):

        try:

            # -------------------------
            # READ REQUEST BODY
            # -------------------------
            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(
                content_length
            ).decode("utf-8")

            # -------------------------
            # CHECK EMPTY BODY
            # -------------------------
            if not body:

                raise Exception(
                    "Request body is empty"
                )

            # -------------------------
            # PARSE JSON
            # -------------------------
            data = json.loads(body)

            # -------------------------
            # GET URL
            # -------------------------
            url = data.get("url")

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
                    }).encode("utf-8")
                )

                return

            # -------------------------
            # LOAD YOUTUBE VIDEO
            # -------------------------
            yt = YouTube(url)

            # -------------------------
            # GET BEST STREAM
            # -------------------------
            stream = yt.streams.get_highest_resolution()

            if not stream:

                raise Exception(
                    "No downloadable stream found"
                )

            # -------------------------
            # CLEAN TITLE
            # -------------------------
            safe_title = re.sub(
                r'[\\\\/*?:"<>|]',
                "",
                yt.title
            )

            # -------------------------
            # RESPONSE DATA
            # -------------------------
            response = {
                "success": True,
                "title": safe_title,
                "download_url": stream.url,
                "thumbnail": yt.thumbnail_url,
                "author": yt.author,
                "length": yt.length,
                "views": yt.views
            }

            # -------------------------
            # SUCCESS RESPONSE
            # -------------------------
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
                json.dumps(response).encode("utf-8")
            )

        except json.JSONDecodeError:

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
                    "error": "Invalid JSON body"
                }).encode("utf-8")
            )

        except Exception as e:

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
                }).encode("utf-8")
            )