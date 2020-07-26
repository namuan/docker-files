import os
import time
import argparse
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

GH_TOKEN = os.getenv("GH_TOKEN")


def send_request(page_no, search_query):
    try:
        github_headers = {
            "Authorization": f"token {GH_TOKEN}"
        }
        response = requests.get(
            url="https://api.github.com/search/code",
            params={
                "order": "desc",
                "q": search_query,
                "sort": "indexed",
                "page": f"{page_no}",
                "per_page": "30",
            },
            headers=github_headers
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        return response.text
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return None


def orchestrate(start_page, end_page, file_type, search_query):
    print(f"Search for {file_type} with query {search_query} from page {start_page} to {end_page}")
    page_no = start_page
    while page_no <= end_page:
        page_file = Path(f"./data/gh_page_{file_type}_{page_no}.json")
        if page_file.exists():
            print(f"{page_file} exists")
        else:
            print(f"{page_file} does not exist. Fetching it from Github")
            page_results = send_request(page_no, search_query)
            with page_file.open(mode='w') as f:
                f.write(page_results)
            time.sleep(60)

        page_no += 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-page",
        required=True,
        type=int,
        help="Starting Page number",
    )
    parser.add_argument(
        "--end-page",
        required=True,
        type=int,
        help="Last Page number",
    )
    parser.add_argument(
        "--file-type",
        required=True,
        type=str,
        help='File type. eg: docker_file, docker_compose, kube_compose'
    )
    parser.add_argument(
        "--search-query",
        required=True,
        type=str,
        help='Full search query in quotes. eg: filename:Dockerfile FROM'
    )
    parser.add_argument("--verbose", action="store_true", default=False)
    return parser.parse_args()


if __name__ == '__main__':
    "filename:Dockerfile FROM"
    args = parse_args()
    orchestrate(args.start_page, args.end_page, args.file_type, args.search_query)
