import pandas as pd
import requests
import argparse
import logging

def main():
    parser = argparse.ArgumentParser(description='url for a github repo.')
    parser.add_argument('URL',nargs='?', type=str, help='GitHub URL')
    args = parser.parse_args()

    # handy links for testing
    star_url =  "https://github.com/sunfounder/SunFounder_PiCar-V"
    starless_url = "https://github.com/SimeonKraev/UnInspired"
    
    base_url = f"https://api.github.com/repos/{user}/{repo}/stargazers"
    headers={"Accept": "application/vnd.github.v3.star+json"}
    params = {"per_page": 100}

    url = "https://github.com/sunfounder/SunFounder_PiCar-V"#args.URL

    user = url.split("/")[-2]
    repo = url.split("/")[-1]

    list_stargazers = []
    page = 1
    with requests.Session() as session:
        session.headers.update(headers)

        while True:
            params['page'] = page 
            response = session.get(base_url, params=params)

            if response.status_code == 403 and 'rate limit' in response.text.lower():
                logging.error("Rate limit reached. Please try again later.")
                break
            try:
                page_data = response.json()
                if not page_data:
                    break
                list_stargazers.extend(page_data)
                page += 1
            except ValueError as e:
                logging.error(f"Failed because: {e}.")
                exit(1)


    usr_info = ["starred_at", "login", "id", "node_id", "url", "followers_url", "subscriptions_url",
                     "organizations_url", "repos_url", "type", "site_admin"]

    data_rows = []
    for starred_user in list_stargazers:
        temp_dict = {"starred_at": starred_user.get("starred_at")}
        user_info = starred_user.get("user", {})
        temp_dict.update({key: value for key, value in user_info.items() if key in usr_info})
        data_rows.append(temp_dict)

    dataset = pd.DataFrame(data_rows)
    print(dataset)
    dataset.to_csv('stargazers_dataset.csv', index=False)

if __name__ == "__main__":
    main()