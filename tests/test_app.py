"""Black-box HTTP checks for the reference workload."""
import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer

from src.app import Handler


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.httpd.server_address[1]
        cls.worker = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.worker.join(timeout=3)

    def fetch(self, path):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            return response.status, response.getheader("Content-Type"), response.read()
        finally:
            conn.close()

    def test_root_returns_json(self):
        status, kind, data = self.fetch("/")
        self.assertEqual(status, 200)
        self.assertIn("application/json", kind)
        self.assertEqual(json.loads(data)["service"], "platform-demo")

    def test_health(self):
        self.assertEqual(self.fetch("/healthz")[0], 200)

    def test_readiness(self):
        self.assertEqual(self.fetch("/readyz")[0], 200)

    def test_metrics_exposed(self):
        status, kind, data = self.fetch("/metrics")
        self.assertEqual(status, 200)
        self.assertIn("text/plain", kind)
        self.assertIn(b"demo_http_requests_total", data)

    def test_unknown_path_is_404(self):
        status, kind, data = self.fetch("/not-here")
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(data)["error"], "not_found")


if __name__ == "__main__":
    unittest.main()
