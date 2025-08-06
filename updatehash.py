import os
import io
import json
import hashlib
from datetime import datetime

#os.chdir(os.path.dirname(__file__))

READ_SIZE = 65536

def update(json, file):
    hash = hashlib.sha256()

    with io.open(file, "rb") as f:
        data = f.read(READ_SIZE)
        while data:
            hash.update(data)
            data = f.read(READ_SIZE)

    print(file, hash.hexdigest())

    mtime = os.path.getmtime(file)
    dt = datetime.fromtimestamp(mtime)
    sha = hash.hexdigest()

    if "sha256" not in json or json["sha256"] != sha:
        json["sha256"] = sha
        json["update_timestamp"] = int(mtime)
        json["update_time_utc"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(int(mtime), dt.strftime("%Y-%m-%d %H:%M:%S"))


with io.open("repository.json", "r", encoding="utf-8") as f:
    repository = json.load(f)

update(repository["packages"], "packages.json")
update(repository["resources"], "resources.zip")

with io.open("repository.json", "w", encoding="utf-8") as f:
    json.dump(repository, f, indent=4) 