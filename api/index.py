from http.server import BaseHTTPRequestHandler
import json
import subprocess
import re


class handler(BaseHTTPRequestHandler):

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
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(
                content_length
            ).decode("utf-8")

            data = json.loads(body)

            url = data.get("url")

            if not url:

                raise Exception(
                    "No URL provided"
                )

            # GET VIDEO INFO
            command = [
                "yt-dlp",
                "--cookies",
                "cookies.txt",
                "-f",
                "best",
                "-g",
                url
            ]

            result = subprocess.check_output(
                command
            ).decode("utf-8").strip()

            response = {
                "success": True,
                "download_url": result
            }

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