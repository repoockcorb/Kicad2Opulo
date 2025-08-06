import os
import io
import json
import hashlib
import urllib.request
from datetime import datetime

#os.chdir(os.path.dirname(__file__))

READ_SIZE = 65536

def update_from_url(json_obj, url, file_name):
    """Download file from URL and calculate SHA256 hash"""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
            hash_obj = hashlib.sha256(content)
            sha = hash_obj.hexdigest()
            
            print(f"{file_name} {sha}")
            
            # Get current timestamp
            mtime = int(datetime.now().timestamp())
            dt = datetime.fromtimestamp(mtime)
            
            if "sha256" not in json_obj or json_obj["sha256"] != sha:
                json_obj["sha256"] = sha
                json_obj["update_timestamp"] = mtime
                json_obj["update_time_utc"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                print(mtime, dt.strftime("%Y-%m-%d %H:%M:%S"))
                
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def update_local(json_obj, file):
    """Calculate hash from local file (fallback)"""
    hash_obj = hashlib.sha256()

    with io.open(file, "rb") as f:
        data = f.read(READ_SIZE)
        while data:
            hash_obj.update(data)
            data = f.read(READ_SIZE)

    print(file, hash_obj.hexdigest())

    mtime = os.path.getmtime(file)
    dt = datetime.fromtimestamp(mtime)
    sha = hash_obj.hexdigest()

    if "sha256" not in json_obj or json_obj["sha256"] != sha:
        json_obj["sha256"] = sha
        json_obj["update_timestamp"] = int(mtime)
        json_obj["update_time_utc"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(int(mtime), dt.strftime("%Y-%m-%d %H:%M:%S"))


with io.open("repository.json", "r", encoding="utf-8") as f:
    repository = json.load(f)

# Update from GitHub URLs
update_from_url(repository["packages"], repository["packages"]["url"], "packages.json")
update_from_url(repository["resources"], repository["resources"]["url"], "resources.zip")

with io.open("repository.json", "w", encoding="utf-8") as f:
    json.dump(repository, f, indent=4) 