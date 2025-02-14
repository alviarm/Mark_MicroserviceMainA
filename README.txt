# Movie Recommendation Microservice

## Key Features
- **Genre-based movie search** with chronological sorting (newest first)
- **Dynamic input validation** based on `movies.txt` contents
- **Rate limiting** (100 requests/day per IP)
- **File health monitoring** system
- Async file operations for high performance

## Service Endpoints

### 1. Movie Search (`GET /search`)
**Parameters**:
```http
GET /search?genre=Action&limit=5

Requirements:

    movies.txt must exist and follow exact format
    Minimum 3-character genres enforced by API

Response:

{
  "status": 200,
  "source": "movies.txt",
  "results": ["The Matrix", "Inception"],
  "count": 2
}

2. Health Check (GET /file_healthcheck)

Monitoring Logic:

if not os.path.exists("movies.txt"): → Triggers 500 error
if file unreadable → Error details in response

movies.txt Format

# Comment lines start with #
Title|Genre|Mood|AddedDate
The Matrix|Action|Sci-Fi|2024-02-15

3 Requirements:

    Pipe-separated (|) format
    Case-insensitive genres (stored lowercase)
    Strict YYYY-MM-DD date format

Setup Instructions

    Install dependencies:

pip3 install fastapi uvicorn slowapi aiofiles

    Start server:

python3 -m uvicorn main:app --reload

    Verify service:

curl http://localhost:8000/file_healthcheck

Error Handling
Error Case	Status Code	Response Example
Missing movies.txt	404	"Contact Mark to restore backup"
Invalid genre	400	"Valid options: action, animation"
Rate limit exceeded	429	"Rate limit exceeded"
Maintenance Guide

    Updating Movies:
        Modify movies.txt directly → Changes take effect immediately on next request
        Backup recommended before bulk edits

    Modifying Rate Limits:

# Change in main.py
@limiter.limit("200/day")  # Updated rate limit

    Recommended Monitoring:

watch -n 3600 curl http://localhost:8000/file_healthcheck  # Hourly checks

Testing Suite

Sample test cases (run these sequentially):

    Valid request:

curl "http://localhost:8000/search?genre=Action&limit=1"

    Invalid genre test:

curl "http://localhost:8000/search?genre=Romance"

    File failure test:

mv movies.txt movies.backup && curl "http://localhost:8000/search?genre=Action"

OpenAPI Docs

 available when service is running.
Security Requirements

    Keep movies.txt in secure directory with read-only permissions
    Review rate limit threshold based on usage metrics
    Do not modify CORS settings without VPN implementation
