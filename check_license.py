import urllib.request
import json

# Download the packages.json from GitHub
url = "https://raw.githubusercontent.com/repoockcorb/Kicad2Opulo/main/packages.json"

try:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        data = json.loads(content.decode('utf-8'))
        
        print("GitHub packages.json content:")
        print(json.dumps(data, indent=2))
        
        # Check the license specifically
        if 'packages' in data and len(data['packages']) > 0:
            package = data['packages'][0]
            print(f"\nLicense value: '{package.get('license', 'NOT FOUND')}'")
            
except Exception as e:
    print(f"Error: {e}") 