import sys
import logging
import argparse
import unittest
from flask import Flask, request, jsonify
from src.methods.funcs import GitHubStargazers

# Create a Flask app
app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/star-history', methods=['GET'])
def star_history():
    """Get the star history for a GitHub repository."""
    url = request.args.get('url')
    if url is not None:
        stargazers = GitHubStargazers(url, save_data=False)
        stargazers.process_stargazers()
        star_data = stargazers.fetch_star_history()
        return jsonify(star_data)
    else:
        return jsonify({"error": "URL parameter is missing"}), 400

def main():
    parser = argparse.ArgumentParser(description='url for a github repo.')
    parser.add_argument('URL', nargs='?', type=str, help='GitHub URL')
    parser.add_argument('sava_data', nargs='?', type=bool, help='storage flag')
    args = parser.parse_args()

    if args.URL is not None:
        url = args.URL
    else:
        logging.error("Something went wrong with the provided URL.")
        exit(1)

    # bool, if True, save dataset
    save_data_flag = args.sava_data if args.sava_data is not None else False

    stargazers = GitHubStargazers(url, save_data=save_data_flag)
    stargazers.process_stargazers()
    stargazers.plot_stars()

if __name__ == "__main__":
    unittest.main(module='tests.tests', exit=False)
    if len(sys.argv) > 1:
        main()
    else:
        app.run(debug=True)
