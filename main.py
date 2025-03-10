from datetime import date, datetime
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import aiofiles
import os

# Initialize app and rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def parse_movies() -> tuple[list[dict], list[str]]:
    """Parse content.txt with async I/O and error handling"""
    try:
        async with aiofiles.open("content.txt", mode="r") as f:
            content = await f.read()

            movies = []
            valid_genres = set()

            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("#") or not line:
                    continue

                parts = line.split("|")
                if len(parts) < 6:
                    continue

                movies.append(
                    {
                        "title": parts[0],
                        "genre": parts[1].strip().lower(),
                        "streaming_service": parts[2],
                        "type": parts[3],
                        "details": parts[4],
                        "length": parts[5],
                    }
                )
                valid_genres.add(parts[1].strip().lower())

            return movies, sorted(valid_genres)

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Content database unavailable. Contact Mark to restore backup.",
        )


@app.get("/search")
@limiter.limit("5/minute")
async def search_movies(
    request: Request,
    genre: str = Query(..., min_length=3),
    limit: int = Query(5, gt=0, le=100),
):
    """Main search endpoint with validation and sorting"""
    movies, valid_genres = await parse_movies()
    genre_lower = genre.strip().lower()

    if genre_lower not in valid_genres:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid genre. Valid options: {', '.join(valid_genres)}",
        )

    filtered = [m["title"] for m in movies if m["genre"] == genre_lower]

    # Sort alphabetically by title
    sorted_movies = sorted(
        [m for m in movies if m["genre"] == genre_lower],
        key=lambda x: x["title"].lower(),
    )[:limit]

    results = [m["title"] for m in sorted_movies]

    return {
        "status": 200,
        "source": "content.txt",
        "results": results,
        "count": len(results),
    }


@app.get("/file_healthcheck")
async def health_check():
    """Endpoint for monitoring file status"""
    try:
        if not os.path.exists("content.txt"):
            raise FileNotFoundError

        async with aiofiles.open("content.txt", mode="r") as f:
            await f.read()

        return {"status": "healthy", "last_checked": datetime.now().isoformat()}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"File health check failed: {str(e)}"
        )
