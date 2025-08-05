import requests
from typing import List, Dict


def fetch_site_content(base_url: str) -> List[Dict]:
    """Fetch normalized content from a WordPress site.

    Args:
        base_url: Base URL of the WordPress site, e.g. "https://example.com".

    Returns:
        A list of dictionaries with fields: id, title, content, date, link,
        slug and meta_description.
    """
    endpoints = ["pages", "posts", "faq"]
    results: List[Dict] = []

    for endpoint in endpoints:
        url = f"{base_url.rstrip('/')}/wp-json/wp/v2/{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                continue
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            # Skip endpoint if request fails
            continue

        if not isinstance(data, list):
            continue

        for item in data:
            meta_description = (
                item.get("yoast_head_json", {}).get("description")
                or item.get("_yoast_wpseo_metadesc")
            )
            results.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title", {}).get("rendered"),
                    "content": item.get("content", {}).get("rendered"),
                    "date": item.get("date"),
                    "link": item.get("link"),
                    "slug": item.get("slug"),
                    "meta_description": meta_description,
                }
            )

    return results
