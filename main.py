import pandas as pd
import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='url for a github repo.')
    parser.add_argument('URL',nargs='?', type=str, help='GitHub URL')
    args = parser.parse_args()

    # handy links for testing
    star_url =  "https://github.com/sunfounder/SunFounder_PiCar-V"
    starless_url = "https://github.com/SimeonKraev/UnInspired"
    headers={"Accept": "application/vnd.github.v3.star+json"}

    url = "https://github.com/sunfounder/SunFounder_PiCar-V"#args.URL

    user = url.split("/")[-2]
    repo = url.split("/")[-1]

    data = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{user}/{repo}/stargazers?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        page_data = response.json()
        if not page_data:
            break
        data.extend(page_data)
        page += 1
        print("page_data", page_data)


    usr_info = ["starred_at", "login", "id", "node_id", "url", "followers_url", "subscriptions_url",
                     "organizations_url", "repos_url", "type", "site_admin"]

    data_rows = []
    for starred_user in data:
        temp_dict = {"starred_at": starred_user.get("starred_at")}
        user_info = starred_user.get("user", {})
        for key in usr_info:
            if key in user_info:
                temp_dict.update({key: user_info[key]})

        data_rows.append(temp_dict)

    dataset = pd.DataFrame(data_rows)
    print(dataset)
    dataset.to_csv('stargazers_dataset.csv', index=False)

if __name__ == "__main__":
    main()