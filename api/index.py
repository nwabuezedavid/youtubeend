from http.server import BaseHTTPRequestHandler
import json
import subprocess
import shutil


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

            # =========================
            # READ BODY
            # =========================
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

            # =========================
            # COPY COOKIES TO /tmp
            # =========================
            shutil.copy(
                "cookies.txt",
                "/tmp/cookies.txt"
            )

            # =========================
            # COMMAND
            # =========================
            command = [
                "python",
                "-m",
                "yt_dlp",

                "--cookies",
                "/tmp/cookies.txt",

                "--no-cache-dir",

                "--user-agent",
                "Mozilla/5.0",

                "-g",

                url
            ]

            # =========================
            # RUN
            # =========================
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                raise Exception(
                    result.stderr
                )

            # =========================
            # VIDEO URL
            # =========================
            video_url = result.stdout.strip()

            # =========================
            # RESPONSE
            # =========================
            response = {
                "success": True,
                "download_url": video_url
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