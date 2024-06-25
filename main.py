import requests

star_url =  "https://github.com/sunfounder/SunFounder_PiCar-V"
starless_url = "https://github.com/SimeonKraev/UnInspired"
headers={"Accept": "application/vnd.github.v3.star+json"}

url = star_url

user = url.split("/")[-2]
repo = url.split("/")[-1]

page = 1
while True:
    url = f"https://api.github.com/repos/{user}/{repo}/stargazers?page={page}&per_page=100"
    response = requests.get(url, headers=headers)
    page_data = response.json()
    if not page_data:
        break
    page += 1
    print("page_data", page_data)
