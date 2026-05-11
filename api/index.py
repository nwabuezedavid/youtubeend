from http.server import BaseHTTPRequestHandler
import json
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress


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
    # GET
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
                "message": "API running"
            }).encode("utf-8")
        )

    # =========================
    # POST
    # =========================
    def do_POST(self):

        try:

            # -------------------------
            # BODY
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

            if not body:

                raise Exception(
                    "Request body is empty"
                )

            data = json.loads(body)

            # -------------------------
            # URL
            # -------------------------
            url = data.get("url")

            if not url:

                raise Exception(
                    "No URL provided"
                )

            # -------------------------
            # YOUTUBE
            # -------------------------
            yt = YouTube(
                url,
                on_progress_callback=on_progress,
                use_po_token=True
            )

            # -------------------------
            # STREAM
            # -------------------------
            stream = yt.streams.get_highest_resolution()

            if not stream:

                raise Exception(
                    "No stream found"
                )

            # -------------------------
            # SAFE TITLE
            # -------------------------
            safe_title = re.sub(
                r'[\\\\/*?:"<>|]',
                "",
                yt.title
            )

            # -------------------------
            # RESPONSE
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
            # SEND RESPONSE
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