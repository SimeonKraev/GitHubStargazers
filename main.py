import requests

star_url =  "https://github.com/sunfounder/SunFounder_PiCar-V"
starless_url = "https://github.com/SimeonKraev/UnInspired"

url = star_url

user = url.split("/")[-2]
repo = url.split("/")[-1]

url = f"https://api.github.com/repos/{user}/{repo}/stargazers"
response = requests.get(url)
page_data = response.json()

print("page_data", page_data)
