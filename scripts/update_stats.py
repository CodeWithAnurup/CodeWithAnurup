import re
import urllib.request
import json
import os

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Use GITHUB_TOKEN if available to avoid any API rate limits in workflow
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', f'token {token}')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

def main():
    username = "CodeWithAnurup"
    
    # 1. Fetch followers count
    user_data = fetch_json(f"https://api.github.com/users/{username}")
    followers = user_data.get("followers", 1)
    
    # 2. Fetch repos to calculate total stars
    repos_data = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100")
    stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    
    # 3. Read README.md
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 4. Replace followers badge
    # Target: https://img.shields.io/badge/followers-NUM-FCA311
    # or: https://img.shields.io/github/followers/CodeWithAnurup
    followers_pattern = r"https://img\.shields\.io/(github/followers/CodeWithAnurup|badge/followers-\d+-FCA311)"
    new_followers_badge = f"https://img.shields.io/badge/followers-{followers}-FCA311"
    content = re.sub(followers_pattern, new_followers_badge, content)
    
    # 5. Replace stars badge
    # Target: https://img.shields.io/badge/stars-NUM-E040FB
    # or: https://img.shields.io/github/stars/CodeWithAnurup
    stars_pattern = r"https://img\.shields\.io/(github/stars/CodeWithAnurup|badge/stars-\d+-E040FB)"
    new_stars_badge = f"https://img.shields.io/badge/stars-{stars}-E040FB"
    content = re.sub(stars_pattern, new_stars_badge, content)
    
    # 6. Save README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Stats updated: Followers = {followers}, Stars = {stars}")

if __name__ == "__main__":
    main()
