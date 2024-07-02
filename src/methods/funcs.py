import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt


class GitHubStargazers:
    def __init__(self, url, save_data=False):
        self.url = url
        self.save_data = save_data
        # headers and params for the request
        self.headers = {"Accept": "application/vnd.github.v3.star+json"}
        self.params = {"per_page": 100}
        # stargarzers cols we are interested in
        self.star_usr_columns = ["starred_at", "login", "type"]

    def parse_url(self):
        """Parse the URL to get the user and repo name."""
        if self.url.endswith("/"):
            self.url = self.url[:-1]

        self.user = self.url.split("/")[-2]
        self.repo = self.url.split("/")[-1]
        
        # header needed to get the timestamp of the star i.e "starred_at"
        self.url = f"https://api.github.com/repos/{self.user}/{self.repo}/stargazers"

    def get_stargazers(self):
        """Get star history data from url."""
        self.list_stargazers = []
        page = 1
        with requests.Session() as session:
            session.headers.update(self.headers)
            while True:
                self.params['page'] = page  # Update the page parameter for each request
                response = session.get(self.url, params=self.params)
                # Check for rate limiting before proceeding
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    logging.error("Rate limit reached. Please try again later.")
                    break
                try:
                    page_data = response.json()
                    if not page_data:  # with multiple pages, the last page will return an empty list
                        break
                    self.list_stargazers.extend(page_data)
                    if len(page_data) > 100: # exit the loop if the page is not full
                        page += 1
                    else:
                        break
                except ValueError as e:
                    logging.error(f"Failed because: {e}.")
                    exit(1)

        if not self.list_stargazers:
            logging.error(f"No stars found for this repo - {self.repo}.")
            exit(1)

    def aggregate_data(self):
        """Gather the column data for each starred used into a list of dicts."""
        self.data_rows = []
        for starred_user in self.list_stargazers:
            temp_dict = {"starred_at": starred_user.get("starred_at")}
            user_info = starred_user.get("user", {})
            temp_dict.update({key: value for key, value in user_info.items() if key in self.star_usr_columns})
            self.data_rows.append(temp_dict)

    def data_to_df(self):
        """Convert the data to a pandas dataframe, sort by date and save as .csv if required."""
        # create a dataframe, sort by date and save as .csv
        dataset = pd.DataFrame(self.data_rows)
        dataset['starred_at'] = pd.to_datetime(dataset['starred_at'])
        self.dataset_sorted = dataset.sort_values(by='starred_at')
        if self.save_data:
            self.dataset_sorted.to_csv(f"{self.repo}_stargazers.csv", index=False)
    
    def process_stargazers(self):
        """
        Orchestrates the fetching and processing of GitHub stargazers for a repository.
        1. Parse the repository URL.
        2. Fetch data of users who have starred the repo.
        3. Collect the cols from usr_info to a dictionary.
        4. Convert data to DataFrame and store it locally if save_data=True.
        """
        self.parse_url()
        self.get_stargazers()
        self.aggregate_data()
        self.data_to_df()
    
    def fetch_star_history(self):
        """Return the star history data as a dict."""
        return self.dataset_sorted.to_dict(orient='records')

    def plot_stars(self):
        """Plot the number of stars over time."""
        print("Plotting something")
        self.dataset_sorted.set_index('starred_at', inplace=True)
        data_resampled = self.dataset_sorted.resample('YE').size()  # Use size() for counting

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(data_resampled.index, data_resampled.values, marker='o', linestyle='-')
        plt.title(f'GitHub Stars Over Time for Repo: {self.repo}')
        plt.xlabel('Date')
        plt.ylabel('Number of Stars')
        plt.grid(True)
        plt.tight_layout()  # Adjust the layout to make room for the labels
        plt.show()  # Display the plot
