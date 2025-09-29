from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs

DATA_FILE = "data.json" 


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

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        bookings = read_data()
        if "id" in query:
            booking_id = int(query["id"][0])
            booking = next((b for b in bookings if b["id"] == booking_id), None)
            if booking:
                self._set_headers(200)
                self.wfile.write(json.dumps(booking).encode("utf-8"))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Booking not found"}).encode("utf-8"))
        else:
            self._set_headers(200)
            self.wfile.write(json.dumps(bookings).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        new_booking = json.loads(post_data.decode("utf-8"))

        bookings = read_data()
        new_booking["id"] = (max([b["id"] for b in bookings], default=0) + 1)
        bookings.append(new_booking)
        write_data(bookings)

        self._set_headers(201)
        self.wfile.write(json.dumps(new_booking).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=MotoBookingServer, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"🚖 Moto Booking server running at http://127.0.0.1:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
