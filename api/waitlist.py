from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except Exception:
            self.send_response(400)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode())
            return

        email = data.get('email', '').strip()
        college = data.get('college', '')
        grad = data.get('grad', '')
        goal = data.get('goal', '')

        if not email:
            self.send_response(400)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Email is required'}).encode())
            return

        secret = os.environ.get('CLERK_SECRET_KEY', '')
        if not secret:
            self.send_response(500)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Server config error'}).encode())
            return

        # Call Clerk Backend API
        try:
            payload = json.dumps({'email_address': email}).encode('utf-8')
            req = urllib.request.Request(
                'https://api.clerk.com/v1/waitlist_entries',
                data=payload,
                headers={
                    'Authorization': f'Bearer {secret}',
                    'Content-Type': 'application/json',
                },
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_data = json.loads(resp.read().decode())
                self.send_response(200)
                self._cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'id': resp_data.get('id'),
                    'status': resp_data.get('status')
                }).encode())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            try:
                err_data = json.loads(err_body)
            except Exception:
                err_data = {}
            errors = err_data.get('errors', [])
            already = any(
                er.get('code') in ('already_on_waitlist', 'form_identifier_exists')
                for er in errors
            )
            if already:
                self.send_response(200)
                self._cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'already_registered': True}).encode())
            else:
                self.send_response(500)
                self._cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': err_body, 'http_status': e.code}).encode())
        except Exception as ex:
            self.send_response(503)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(ex)}).encode())

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        pass  # suppress default logs
