from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs
import base64

DATA_FILE = "data.json"

USERNAME = "user"
PASSWORD = "pass"

def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class MotoBookingServer(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self._send_unauthorized()
            return False

        encoded_cred = auth_header.split(' ')[1]
        decoded_bytes = base64.b64decode(encoded_cred)
        decoded_str = decoded_bytes.decode('utf-8')
        username, password = decoded_str.split(':', 1)

        if username == USERNAME and password == PASSWORD:
            return True
        else:
            self._send_unauthorized()
            return False

    def _send_unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Moto Booking Server"')
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode("utf-8"))

    def do_GET(self):
        if not self._authenticate():
            return

        query = parse_qs(urlparse(self.path).query)
        bookings = read_data()
        if "id" in query:
            try:
                booking_id = int(query["id"][0])
                booking = next((b for b in bookings if b["id"] == booking_id), None)
                if booking:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(booking).encode("utf-8"))
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Booking not found"}).encode("utf-8"))
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid id parameter"}).encode("utf-8"))
        else:
            self._set_headers(200)
            self.wfile.write(json.dumps(bookings).encode("utf-8"))

    def do_POST(self):
        if not self._authenticate():
            return

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        new_booking = json.loads(post_data.decode("utf-8"))

        bookings = read_data()
        new_booking["id"] = (max((b["id"] for b in bookings), default=0) + 1)
        bookings.append(new_booking)
        write_data(bookings)

        self._set_headers(201)
        self.wfile.write(json.dumps(new_booking).encode("utf-8"))

    def do_PUT(self):
        if not self._authenticate():
            return

        query = parse_qs(urlparse(self.path).query)
        if "id" not in query:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Missing id parameter for PUT"}).encode("utf-8"))
            return
        
        try:
            booking_id = int(query["id"][0])
        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid id parameter"}).encode("utf-8"))
            return

        content_length = int(self.headers.get("Content-Length", 0))
        put_data = self.rfile.read(content_length)
        updated_booking = json.loads(put_data.decode("utf-8"))
        updated_booking["id"] = booking_id

        bookings = read_data()
        for i, booking in enumerate(bookings):
            if booking["id"] == booking_id:
                bookings[i] = updated_booking
                write_data(bookings)
                self._set_headers(200)
                self.wfile.write(json.dumps(updated_booking).encode("utf-8"))
                return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Booking not found"}).encode("utf-8"))

    def do_DELETE(self):
        if not self._authenticate():
            return

        query = parse_qs(urlparse(self.path).query)
        if "id" not in query:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Missing id parameter for DELETE"}).encode("utf-8"))
            return
        
        try:
            booking_id = int(query["id"][0])
        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid id parameter"}).encode("utf-8"))
            return

        bookings = read_data()
        new_bookings = [b for b in bookings if b["id"] != booking_id]

        if len(new_bookings) == len(bookings):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Booking not found"}).encode("utf-8"))
        else:
            write_data(new_bookings)
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": f"Booking {booking_id} deleted"}).encode("utf-8"))

    def do_PATCH(self):
        if not self._authenticate():
            return

        query = parse_qs(urlparse(self.path).query)
        if "id" not in query:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Missing id parameter for PATCH"}).encode("utf-8"))
            return
        
        try:
            booking_id = int(query["id"][0])
        except ValueError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid id parameter"}).encode("utf-8"))
            return

        content_length = int(self.headers.get("Content-Length", 0))
        patch_data = self.rfile.read(content_length)
        patch_fields = json.loads(patch_data.decode("utf-8"))

        bookings = read_data()
        for i, booking in enumerate(bookings):
            if booking["id"] == booking_id:
                bookings[i].update(patch_fields)
                write_data(bookings)
                self._set_headers(200)
                self.wfile.write(json.dumps(bookings[i]).encode("utf-8"))
                return
        
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Booking not found"}).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=MotoBookingServer, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"🚖 Moto Booking server running at http://127.0.0.1:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
