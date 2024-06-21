import requests

# Define the base URL of your HTTP server
BASE_URL = 'http://127.0.0.1:80'

def test_basic_functionality():
    try:
        # Test loading index.html
        response = requests.get(BASE_URL + '/index')
        assert response.status_code == 200, f"Failed to load index.html: {response.status_code}"
        
        # Test redirecting /doremon to css/doremon.css
        response = requests.get(BASE_URL + '/doremon')
        assert response.status_code == 302, f"Failed to redirect /doremon: {response.status_code}"
        
        # Test loading abstract.jpg
        response = requests.get(BASE_URL + '/abstract')
        assert response.status_code == 200, f"Failed to load abstract.jpg: {response.status_code}"
        
        # Test loading box.js
        response = requests.get(BASE_URL + '/box')
        assert response.status_code == 200, f"Failed to load box.js: {response.status_code}"
        
        # Test loading jquery.min.js
        response = requests.get(BASE_URL + '/jquery')
        assert response.status_code == 200, f"Failed to load jquery.min.js: {response.status_code}"
        
        # Test loading submit.js
        response = requests.get(BASE_URL + '/submit')
        assert response.status_code == 200, f"Failed to load submit.js: {response.status_code}"
        
        # Test JavaScript functionality (replace with actual test based on JS behavior)
        response = requests.get(BASE_URL + '/index')
        assert '<div id="js-square" style="display:none;">' not in response.text, "JS square not toggled correctly"
        
        print("Basic functionality test passed.")
    except AssertionError as e:
        print(f"Basic functionality test failed: {e}")

def test_302_redirect():
    try:
        response = requests.get(BASE_URL + '/loading')
        assert response.status_code == 302, f"Expected 302 redirect but received {response.status_code}"
        print("302 Redirect test passed.")
    except AssertionError as e:
        print(f"302 Redirect test failed: {e}")

def test_404_not_found():
    try:
        response = requests.get(BASE_URL + '/nonexistent')
        assert response.status_code == 404, f"Expected 404 Not Found but received {response.status_code}"
        print("404 Not Found test passed.")
    except AssertionError as e:
        print(f"404 Not Found test failed: {e}")

def test_server_stability():
    try:
        # Open multiple connections simultaneously
        responses = []
        for _ in range(5):
            responses.append(requests.get(BASE_URL + '/index'))
        
        # Close one connection
        responses[0].close()
        
        # Refresh other connections
        for i in range(1, len(responses)):
            responses[i] = requests.get(BASE_URL + '/index')
            assert responses[i].status_code == 200, f"Failed to refresh connection {i}: {responses[i].status_code}"
        
        print("Server stability test passed.")
    except AssertionError as e:
        print(f"Server stability test failed: {e}")

def calculate_overall_score():
    score = 100
    
    # Deduct points based on test failures
    try:
        test_basic_functionality()
    except:
        score -= 60  # Deduct maximum points for basic functionality failure
    
    try:
        test_302_redirect()
    except:
        score -= 20  # Deduct points for 302 redirect failure
    
    try:
        test_404_not_found()
    except:
        score -= 20  # Deduct points for 404 Not Found failure
    
    try:
        test_server_stability()
    except:
        score -= 20  # Deduct points for server stability failure
    
    # Manual code review score adjustments as per findings
    
    return score

# Example usage:
if __name__ == '__main__':
    final_score = calculate_overall_score()
    print(f"Final score: {final_score}")
