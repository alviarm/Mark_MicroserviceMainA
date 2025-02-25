import requests


def test_search_endpoint():
    """
    Test the /search endpoint programmatically.
    """
    # Configuration (adjust port if needed)
    base_url = "http://localhost:8000"  # Replace with your microservice's URL

    # Test Case 1: Valid Request (Action genre, limit 3)
    print("\n=== TEST CASE 1: VALID REQUEST ===")
    params = {"genre": "action", "limit": 3}
    response = requests.get(f"{base_url}/search", params=params)

    # Evaluate response
    if response.status_code == 200:
        print("✅ SUCCESS:", response.json())
    else:
        print(f"❌ ERROR: Status code {response.status_code}")
        print("Response:", response.json())

    # Test Case 2: Invalid Genre (e.g., 'horror')
    print("\n=== TEST CASE 2: INVALID GENRE ===")
    params = {"genre": "horror", "limit": 2}
    response = requests.get(f"{base_url}/search", params=params)

    # Evaluate response
    if response.status_code == 400:
        print("✅ SUCCESS: Invalid genre error received")
        print("Response:", response.json())
    else:
        print(f"❌ ERROR: Expected status code 400, got {response.status_code}")
        print("Response:", response.json())

    # Test Case 3: Missing movies.txt
    print("\n=== TEST CASE 3: MISSING FILE ===")
    print("⚠️ Temporarily rename or delete movies.txt...")
    response = requests.get(f"{base_url}/search", params={"genre": "action"})

    # Evaluate response
    if response.status_code == 404:
        print("✅ SUCCESS: Missing file error received")
        print("Response:", response.json())
    else:
        print(f"❌ ERROR: Expected status code 404, got {response.status_code}")
        print("Response:", response.json())

    # Test Case 4: Rate Limit Exceeded
    print("\n=== TEST CASE 4: RATE LIMIT ===")
    for i in range(1, 6):  # Send 5 requests
        response = requests.get(f"{base_url}/search", params={"genre": "action"})
        print(f"Request {i}: Status {response.status_code}", end=" | ")

    # Check if last request was rate-limited
    if response.status_code == 429:
        print("\n✅ SUCCESS: Rate limit detected")
    else:
        print("\n❌ ERROR: Rate limit not functioning")


def test_health_endpoint():
    """
    Test the /file_healthcheck endpoint.
    """
    base_url = "http://localhost:8000"  # Update if necessary
    response = requests.get(f"{base_url}/file_healthcheck")

    if response.status_code == 200:
        print("\n\n=== HEALTH CHECK ===")
        print("✅ Healthcheck passed:", response.json())
    else:
        print(f"❌ Healthcheck failed, status {response.status_code}")


# Execute tests
if __name__ == "__main__":
    print("ITIVE randing sample\nDisney Movie recommendation test\n")
    test_search_endpoint()
    test_health_endpoint()
