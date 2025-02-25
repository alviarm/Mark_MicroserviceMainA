README: Communication Contract for Microservice A
Version: 1.2
1. Request Data Instructions
Endpoint:
GET /search
Parameters:

    genre: String (required) - Genre name (minimum 3 characters, case-insensitive).
    limit: Integer (optional) - Number of results to return (default: 5, max: 100).

Example Call (Python):
PythonCopy

import requests

response = requests.get(
    "http://[YOUR_DOMAIN]/search",
    params={"genre": "action", "limit": 3}
)
print(response.json())

2. Response Data Instructions
Format: JSON

    status: HTTP status code (200, 400, 404, 429).
    source: "movies.txt" (data source).
    results: List of movie titles.
    count: Number of results.

Example Success Response:
JSONCopy

{
  "status": 200,
  "source": "movies.txt",
  "results": ["The Matrix", "Inception"],
  "count": 2
}

Example Error Response (Invalid Genre):
JSONCopy

{
  "status": 400,
  "error": "Invalid genre. Valid options: action, animation"
}

3. UML Sequence Diagram
![UML Sequence Diagram](images/UML_diagram.png)
Description:

    Client → Microservice: GET /search?genre=action&limit=3
    Microservice (Self): Validate parameters and rate limits.
    Microservice → movies.txt: Asynchronous read.
    Microservice (Self): Filter and sort movies.
    Microservice → Client: Return JSON response (200) or error (404, 400, 429).

4. Additional Notes

    Rate Limiting: 100 requests/day/IP.
    File Format: movies.txt must use pipe (|) delimiters and lowercase genres.
    Error Handling: Returns detailed error messages (e.g., 404 for missing files).

Git Repository:
Clone this repository for full code and dependencies:
git clone <https://github.com/[USERNAME]/microservice-a.git>
Run the service locally:
bashCopy

pip install fastapi uvicorn slowapi aiofiles
uvicorn main:app --reload