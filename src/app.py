from fastapi import FastAPI
from fetchers.wordpress import fetch_site_content

app = FastAPI()

WORDPRESS_SITES = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
    "https://example4.com",
]


@app.get("/api/posts")
def get_posts():
    posts = []
    for url in WORDPRESS_SITES:
        posts.extend(fetch_site_content(url))
    return {"posts": posts}
