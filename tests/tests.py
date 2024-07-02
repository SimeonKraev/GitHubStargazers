import os
import sys
import unittest
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from unittest.mock import patch, MagicMock
from src.methods.funcs import GitHubStargazers


class TestGitHubStargazers(unittest.TestCase):
    """Test GitHubStargazers class and /api/stargazers endpoint."""
    def setUp(self):
        """Prepare test environment for GitHubStargazers tests."""
        self.client = app.test_client()
        self.url = "https://github.com/user/repo"
        self.github_stargazers = GitHubStargazers(self.url)

    def test_01_test_health_check(self):
        """Ensure /health endpoint returns a healthy status."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_02_test_stargazers_endpoint_missing_url(self):
        """Ensure /api/stargazers endpoint rejects requests without URL parameter."""
        response = self.client.get('/star-history')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "URL parameter is missing"})

    def test_03_test_parse_url(self):
        """Check if parse_url method correctly extracts user and repository from URL."""
        self.github_stargazers.parse_url()
        self.assertEqual(self.github_stargazers.user, "user")
        self.assertEqual(self.github_stargazers.repo, "repo")
        self.assertEqual(self.github_stargazers.url, "https://api.github.com/repos/user/repo/stargazers")

    @patch('requests.Session.get')
    def test_04_test_get_stargazers(self, mock_get):
        """Ensure get_stargazers method successfully retrieves stargazers data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"starred_at": "2021-01-01T00:00:00Z", "user": {"login": "test_user", "type": "User", "site_admin": False}}]
        mock_get.return_value = mock_response

        self.github_stargazers.get_stargazers()
        self.assertEqual(len(self.github_stargazers.list_stargazers), 1)
        self.assertEqual(self.github_stargazers.list_stargazers[0]["user"]["login"], "test_user")

    def test_05_test_aggregate_data(self):
        """Test that aggregate_data method correctly compiles information about stargazers."""
        self.github_stargazers.list_stargazers = [{"starred_at": "2021-01-01T00:00:00Z", "user": {"login": "test_user", "type": "User", "site_admin": False}}]
        self.github_stargazers.aggregate_data()
        self.assertEqual(len(self.github_stargazers.data_rows), 1)
        self.assertEqual(self.github_stargazers.data_rows[0]["login"], "test_user")
        
    @patch('pandas.DataFrame.to_csv')
    def test_06_test_data_to_df(self, mock_to_csv):
        """Ensure data_to_df method correctly saves stargazers data to a DataFrame and optionally to a CSV file."""
        self.github_stargazers.data_rows = [{"starred_at": "2021-01-01T00:00:00Z", "login": "test_user", "type": "User", "site_admin": False}]
        self.github_stargazers.save_data = True
        self.github_stargazers.repo = "repo"
        self.github_stargazers.data_to_df()
        mock_to_csv.assert_called_once()
        self.assertEqual(self.github_stargazers.dataset_sorted.iloc[0]["login"], "test_user")

    @patch('matplotlib.pyplot.show')
    def test_07_test_plot_stars(self, mock_show):
        """Verify plot_stars method correctly displays a plot of stargazers over time."""
        self.github_stargazers.repo = "repo"
        self.github_stargazers.dataset_sorted = pd.DataFrame({"starred_at": pd.to_datetime(["2021-01-01", "2021-02-01"]), "login": ["user1", "user2"]})
        self.github_stargazers.plot_stars()
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()