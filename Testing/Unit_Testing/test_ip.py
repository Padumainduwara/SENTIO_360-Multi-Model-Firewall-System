# test_ip.py

# Function to extract the true client IP from Render Cloud / Proxies
def extract_ip(headers):
    # Check if the X-Forwarded-For header exists
    if "X-Forwarded-For" in headers:
        # Extract the first IP (True Client IP) before the comma
        return headers["X-Forwarded-For"].split(",")[0].strip()
    return "127.0.0.1"

def test_real_ip_extraction():
    # Test Case 1: Request passing through a cloud load balancer
    # Expected Result: Should extract '192.168.1.50' ignoring the proxy IP
    mock_headers = {"X-Forwarded-For": "192.168.1.50, 10.0.0.1"}
    assert extract_ip(mock_headers) == "192.168.1.50"

def test_local_ip_fallback():
    # Test Case 2: Direct request without any proxy headers
    # Expected Result: Should fallback to default localhost IP
    mock_headers = {"Host": "localhost:8000"}
    assert extract_ip(mock_headers) == "127.0.0.1"