import os
import requests
import base64

# 1. Fetch data from GitHub GraphQL API
token = os.getenv('GH_TOKEN')
headers = {"Authorization": f"Bearer {token}"}
query = """
query {
  user(login: "Theophilus-Nueva") {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      nodes {
        languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
}
"""

response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
data = response.json()

# 2. Process language totals
langs = {}
total_size = 0

for repo in data['data']['user']['repositories']['nodes']:
    for edge in repo['languages']['edges']:
        name = edge['node']['name']
        color = edge['node']['color']
        size = edge['size']
        
        if name not in langs:
            langs[name] = {'size': 0, 'color': color}
        langs[name]['size'] += size
        total_size += size

sorted_langs = sorted(langs.items(), key=lambda x: x[1]['size'], reverse=True)[:5]

# 3. Map Languages to Devicon URLs
icon_map = {
    "JavaScript": "javascript/javascript-original.svg",
    "C#": "csharp/csharp-original.svg",
    "CSS": "css3/css3-original.svg",
    "Python": "python/python-original.svg",
    "HTML": "html5/html5-original.svg",
    "PHP": "php/php-original.svg",
    "Java": "java/java-original.svg",
    "TypeScript": "typescript/typescript-original.svg",
    "C++": "cplusplus/cplusplus-original.svg"
}

# 4. Generate the SVG 
svg_content = f"""<svg width="350" height="230" viewBox="0 0 350 230" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="350" height="230" fill="#0D1117" rx="10" stroke="#30363D" stroke-width="1"/>
    <text x="25" y="35" fill="#FFFFFF" font-family="Arial" font-size="16" font-weight="bold">Custom Top Languages</text>
"""

y_pos = 70
for name, info in sorted_langs:
    percent = (info['size'] / total_size) * 100
    
    # Check for icon, otherwise fallback to colored circle
    if name in icon_map:
        icon_url = f"https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/{icon_map[name]}"
        try:
            icon_resp = requests.get(icon_url)
            b64_icon = base64.b64encode(icon_resp.content).decode('utf-8')
            svg_content += f"""
            <image href="data:image/svg+xml;base64,{b64_icon}" x="25" y="{y_pos - 15
