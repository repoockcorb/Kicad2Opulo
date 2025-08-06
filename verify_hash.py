import urllib.request
import hashlib
import json

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

# URLs from your repository
packages_url = "https://raw.githubusercontent.com/repoockcorb/Kicad2Opulo/main/packages.json"
resources_url = "https://raw.githubusercontent.com/repoockcorb/Kicad2Opulo/main/resources.zip"

print("Downloading and calculating hashes from GitHub...")
print(f"Packages URL: {packages_url}")
print(f"Resources URL: {resources_url}")

# Calculate hashes from GitHub
packages_hash = calculate_hash_from_url(packages_url)
resources_hash = calculate_hash_from_url(resources_url)

print(f"\nGitHub packages.json hash: {packages_hash}")
print(f"GitHub resources.zip hash: {resources_hash}")

# Read current repository.json
with open("repository.json", "r") as f:
    repo_data = json.load(f)

print(f"\nCurrent repository.json packages hash: {repo_data['packages']['sha256']}")
print(f"Current repository.json resources hash: {repo_data['resources']['sha256']}")

# Check if hashes match
if packages_hash == repo_data['packages']['sha256']:
    print("✓ Packages hash matches!")
else:
    print("✗ Packages hash mismatch!")
    print(f"  Expected: {repo_data['packages']['sha256']}")
    print(f"  Actual:   {packages_hash}")

if resources_hash == repo_data['resources']['sha256']:
    print("✓ Resources hash matches!")
else:
    print("✗ Resources hash mismatch!")
    print(f"  Expected: {repo_data['resources']['sha256']}")
    print(f"  Actual:   {resources_hash}") 