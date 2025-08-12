import os
import io
import json
import hashlib
import urllib.request
from datetime import datetime

READ_SIZE = 65536

def calculate_hash_from_url(url):
    """Download file from URL and calculate SHA256 hash"""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
            hash_obj = hashlib.sha256(content)
            return hash_obj.hexdigest()
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def calculate_hash_from_file(file_path):
    """Calculate SHA256 hash from local file"""
    hash_obj = hashlib.sha256()
    try:
        with io.open(file_path, "rb") as f:
            data = f.read(READ_SIZE)
            while data:
                hash_obj.update(data)
                data = f.read(READ_SIZE)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return None

def update_timestamp_info(json_obj):
    """Update timestamp information"""
    mtime = int(datetime.now().timestamp())
    dt = datetime.fromtimestamp(mtime)
    json_obj["update_timestamp"] = mtime
    json_obj["update_time_utc"] = dt.strftime("%Y-%m-%d %H:%M:%S")
    return mtime, dt

print("=== Updating Package Hashes ===")

# Load repository.json
with io.open("repository.json", "r", encoding="utf-8") as f:
    repository = json.load(f)

# Load packages.json
with io.open("packages.json", "r", encoding="utf-8") as f:
    packages = json.load(f)

# Get the resources URL from repository.json
resources_url = repository["resources"]["url"]
print(f"Resources URL: {resources_url}")

# Calculate hash from GitHub
resources_hash = calculate_hash_from_url(resources_url)
if resources_hash:
    print(f"GitHub resources.zip hash: {resources_hash}")
    
    # Update download_sha256 in packages.json
    for package in packages["packages"]:
        for version in package["versions"]:
            if "download_sha256" in version:
                old_hash = version["download_sha256"]
                version["download_sha256"] = resources_hash
                print(f"Updated packages.json download_sha256: {old_hash} -> {resources_hash}")
    
    # Save updated packages.json
    with io.open("packages.json", "w", encoding="utf-8") as f:
        json.dump(packages, f, indent=2)
    print("✓ packages.json updated")
    
    # Calculate new hash of packages.json as served from GitHub (avoids CRLF mismatches)
    packages_hash = calculate_hash_from_url(repository["packages"]["url"]) or calculate_hash_from_file("packages.json")
    if packages_hash:
        print(f"New packages.json hash: {packages_hash}")
        
        # Update repository.json with new hashes
        if repository["packages"]["sha256"] != packages_hash:
            repository["packages"]["sha256"] = packages_hash
            update_timestamp_info(repository["packages"])
            print("✓ packages hash updated in repository.json")
        
        if repository["resources"]["sha256"] != resources_hash:
            repository["resources"]["sha256"] = resources_hash
            update_timestamp_info(repository["resources"])
            print("✓ resources hash updated in repository.json")
        
        # Save updated repository.json
        with io.open("repository.json", "w", encoding="utf-8") as f:
            json.dump(repository, f, indent=4)
        print("✓ repository.json updated")
        
        print("\n=== Summary ===")
        print(f"packages.json: {packages_hash}")
        print(f"resources.zip: {resources_hash}")
        print("\nAll hashes synchronized! Ready for KiCad installation.")
    else:
        print("✗ Failed to calculate packages.json hash")
else:
    print("✗ Failed to get resources.zip hash from GitHub") 