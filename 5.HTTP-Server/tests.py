import unittest
import requests

# Define the base URL of your HTTP server
BASE_URL = 'http://127.0.0.1:80'

class TestHTTPServer(unittest.TestCase):

    def test_index_html(self):
        response = requests.get(BASE_URL + '/index')
        self.assertEqual(response.status_code, 200, f"Failed to load index.html: {response.status_code}")

    def test_redirect_doremon(self):
        response = requests.get(BASE_URL + '/doremon')
        self.assertEqual(response.status_code, 302, f"Failed to redirect /doremon: {response.status_code}")

    def test_load_abstract_jpg(self):
        response = requests.get(BASE_URL + '/abstract')
        self.assertEqual(response.status_code, 200, f"Failed to load abstract.jpg: {response.status_code}")

    def test_load_box_js(self):
        response = requests.get(BASE_URL + '/box')
        self.assertEqual(response.status_code, 200, f"Failed to load box.js: {response.status_code}")

    def test_load_jquery_min_js(self):
        response = requests.get(BASE_URL + '/jquery')
        self.assertEqual(response.status_code, 200, f"Failed to load jquery.min.js: {response.status_code}")

    def test_load_submit_js(self):
        response = requests.get(BASE_URL + '/submit')
        self.assertEqual(response.status_code, 200, f"Failed to load submit.js: {response.status_code}")

    def test_js_functionality(self):
        response = requests.get(BASE_URL + '/index')
        self.assertNotIn('<div id="js-square" style="display:none;">', response.text, "JS square not toggled correctly")

    def test_302_redirect_loading(self):
        response = requests.get(BASE_URL + '/loading')
        self.assertEqual(response.status_code, 302, f"Expected 302 redirect but received {response.status_code}")

    def test_404_not_found(self):
        response = requests.get(BASE_URL + '/nonexistent')
        self.assertEqual(response.status_code, 404, f"Expected 404 Not Found but received {response.status_code}")

    def test_server_stability(self):
        responses = []
        for _ in range(5):
            responses.append(requests.get(BASE_URL + '/index'))
        
        responses[0].close()
        
        for i in range(1, len(responses)):
            response = requests.get(BASE_URL + '/index')
            self.assertEqual(response.status_code, 200, f"Failed to refresh connection {i}: {response.status_code}")

    def test_calculate_area_with_parameters(self):
        response = requests.get(BASE_URL + '/calculate-area', params={'height': 2, 'width': 3})
        self.assertEqual(response.status_code, 200, f"Failed to calculate area with status code: {response.status_code}")
        self.assertAlmostEqual(float(response.text.strip()), 3.0, places=1, msg=f"Expected area to be 3.0 but got: {response.text.strip()}")

if __name__ == '__main__':
    unittest.main()

