Movie Recommendation Microservice
Key Features

    Genre-based movie and TV series search with alphabetical sorting
    Dynamic input validation based on content.txt contents
    Rate limiting (5 requests/minute per IP)
    File health monitoring system
    Async file operations for high performance

Service Endpoints

1. Movie/TV Series Search (GET /search)
   Parameters:
   httpCopy

GET /search?genre=Action&limit=5

Requirements:

- `content.txt` must exist and follow the exact format
- Minimum 3-character genres enforced by API

Response:
{
"status": 200,
"source": "content.txt",
"results": ["Interstellar", "Friends"],
"count": 2
}

2.  Health Check (GET /file_healthcheck)
    Monitoring Logic:

        Checks if content.txt exists and is readable

Data Format
content.txt Format:
Copy

# Comment lines start with

title|genre|streaming_service|type|details|length
Interstellar|sci-fi|netflix|movie|A movie about space exploration...|169
Friends|comedy|max|series|A group of 6 friends living together in Manhattan|22

Requirements:

    Pipe-separated (|) format
    Case-insensitive genres (stored lowercase)

Setup Instructions
Install dependencies:
bashCopy

pip install fastapi uvicorn slowapi aiofiles

Start the server:
bashCopy

uvicorn main:app --reload

Verify service:
bashCopy

curl http://localhost:8000/file_healthcheck

Error Handling
Error Case Status Code Response Example
Missing content.txt 404 "Contact Mark to restore backup"
Invalid genre 400 "Valid options: action, comedy, sci-fi"
Rate limit exceeded 429 "Rate limit exceeded"
Built-in Application Security
Use AI to find and fix vulnerabilities—freeing your teams to ship more secure software faster.
Work together, achieve more
Collaborate with your teams, use management tools that sync with your projects, and code from anywhere—all on a single, integrated platform.
Example Test Cases
Valid request:
bashCopy

curl "http://localhost:8000/search?genre=comedy&limit=2"

Invalid genre test:
bashCopy

curl "http://localhost:8000/search?genre=horror"

File failure test:
bashCopy

mv content.txt content.backup && curl "http://localhost:8000/search?genre=comedy"

OpenAPI Docs
Available when service is running.

UML Sequence Diagram
https://github.com/alviarm/Mark_MicroserviceMainA/raw/main/images/UML_diagram.png
Description:

    Client → Microservice: GET /search?genre=action&limit=3
    Microservice (Self): Validate parameters and rate limits.
    Microservice → content.txt: Asynchronous read.
    Microservice (Self): Filter and sort movies/TV series.
    Microservice → Client: Return JSON response (200) or error (404, 400, 429).

Additional Notes

    Rate Limiting: 5 requests/minute/IP (updated from 100/day for testing purposes).
    File Format: content.txt must use pipe (|) delimiters and lowercase genres.
    Error Handling: Returns detailed error messages (e.g., 404 for missing files).
    The microservice now supports both movies and TV series in the same file, with sorting by title.

Git Repository
Clone this repository for full code and dependencies:
bashCopy

git clone https://github.com/alviarm/Mark_MicroserviceMainA.git

Run the service locally:
bashCopy

pip install fastapi uvicorn slowapi aiofiles
uvicorn main:app --reload
