import os
import requests

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

svg_content = f"""<svg width="400" height="200" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="200" fill="#0D1117" rx="10"/>
    <text x="20" y="30" fill="#C9D1D9" font-family="Arial" font-size="16" font-weight="bold">Custom Top Languages</text>
"""

y_pos = 60
for name, info in sorted_langs:
    percent = (info['size'] / total_size) * 100
    svg_content += f"""
    <circle cx="25" cy="{y_pos - 4}" r="5" fill="{info['color']}"/>
    <text x="40" y="{y_pos}" fill="#C9D1D9" font-family="Arial" font-size="14">{name} - {percent:.1f}%</text>
    """
    y_pos += 25

svg_content += "</svg>"

# 4. Save the SVG
with open("custom-stats.svg", "w") as f:
    f.write(svg_content)
