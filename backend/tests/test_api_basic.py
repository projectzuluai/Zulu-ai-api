import requests

BASE_URL = "http://localhost:5000"

def test_endpoint(path):
    url = f"{BASE_URL}{path}"
    try:
        resp = requests.get(url)
        print(f"{path}: {resp.status_code}", resp.json())
        assert resp.status_code == 200
    except Exception as e:
        print(f"Error testing {path}: {e}")
        assert False

def run_tests():
    test_endpoint("/health")
    test_endpoint("/status")
    test_endpoint("/metrics")
    test_endpoint("/ping")
    test_endpoint("/version")
    test_endpoint("/info")
    test_endpoint("/docs-link")

if __name__ == "__main__":
    run_tests()
    print("Basic API endpoint tests completed.")
