import requests
import os
import hashlib
from urllib.parse import urlparse

def hash_content(content):
    """Generate a SHA256 hash for file content to detect duplicates."""
    return hashlib.sha256(content).hexdigest()

def fetch_images(urls):
    folder = "Fetched_Images"
    os.makedirs(folder, exist_ok=True)

    seen_hashes = set()  # store content hashes to prevent duplicates

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Request the file (streaming = memory-efficient)
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Check HTTP headers for safety
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length", "Unknown")

            if not content_type.startswith("image/"):
                print(f"✗ Skipping {url} — not an image (Content-Type: {content_type})")
                continue

            # Read content and check for duplicates
            content = response.content
            file_hash = hash_content(content)

            if file_hash in seen_hashes:
                print(f"✗ Skipping {url} — duplicate image detected")
                continue
            seen_hashes.add(file_hash)

            # Extract filename or fallback
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"image_{len(seen_hashes)}.jpg"

            filepath = os.path.join(folder, filename)

            # Save the file
            with open(filepath, "wb") as f:
                f.write(content)

            print(f"✓ Downloaded {filename} ({content_length} bytes) → {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error fetching {url}: {e}")
        except Exception as e:
            print(f"✗ Unexpected error with {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A mindful tool for safely collecting images from the web\n")

    # Accept multiple URLs
    urls = input("Enter one or more image URLs (comma-separated): ").split(",")
    fetch_images(urls)

    print("\nConnection strengthened. Community enriched. 🌍")

if __name__ == "__main__":
    main()
