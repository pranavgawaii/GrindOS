from http.server import BaseHTTPRequestHandler
import json
import os
import httpx


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
            self._respond(400, {'error': 'Invalid JSON'})
            return

        email = data.get('email', '').strip()

        if not email:
            self._respond(400, {'error': 'Email is required'})
            return

        secret = os.environ.get('CLERK_SECRET_KEY', '')
        if not secret:
            self._respond(500, {'error': 'Server config error: missing CLERK_SECRET_KEY'})
            return

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(
                    'https://api.clerk.com/v1/waitlist_entries',
                    headers={
                        'Authorization': f'Bearer {secret}',
                        'Content-Type': 'application/json',
                    },
                    json={'email_address': email},
                )

            resp_data = resp.json() if resp.content else {}

            if resp.status_code in (200, 201):
                self._respond(200, {
                    'success': True,
                    'id': resp_data.get('id'),
                    'status': resp_data.get('status')
                })
                return

            errors = resp_data.get('errors', [])
            already = any(
                e.get('code') in ('already_on_waitlist', 'form_identifier_exists')
                for e in errors
            )
            if already:
                self._respond(200, {'success': True, 'already_registered': True})
            else:
                self._respond(500, {
                    'error': f'Clerk error {resp.status_code}',
                    'details': errors,
                    'raw': resp.text[:500]
                })

        except Exception as ex:
            self._respond(503, {'error': str(ex)})

    def _respond(self, status, payload):
        self.send_response(status)
        self._cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, format, *args):
        pass
