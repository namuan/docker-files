import argparse
from pathlib import Path

from ingest.db_model import *
from peewee import IntegrityError


def save_data(file_item):
    print(f"Saving {file_item}")
    try:
        file_item.save(force_insert=True)
    except IntegrityError as e:
        print(f"Found duplicate file sha: {file_item.file_sha}")
        print(e)


def get_file_item(item, file_type):
    return FileItem(
        file_name=item.get("name"),
        file_path=item.get("path"),
        download_link="",
        html_link=item.get("html_url"),
        repo_name=item.get("repository").get("full_name"),
        repo_desc=item.get("repository").get("description"),
        repo_html_link=item.get("repository").get("html_url"),
        file_url=item.get("url"),  # To retrieve download_url
        file_sha=item.get("sha"),
        file_type=file_type
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file-type",
        required=True,
        type=str,
        help='File type. eg: docker_files, docker_compose'
    )
    return parser.parse_args()


file_type_to_name_mapping = {
    'docker_files': 'Dockerfile',
    'docker_compose': 'docker-compose.yml'
}

if __name__ == '__main__':
    args = parse_args()
    p = Path(".")
    gh_page_files = p.glob(f"./data/gh_page_{args.file_type}_*.json")

    item_name_in_result = file_type_to_name_mapping.get(args.file_type, 'NoResultLookup')

    for gh_page_file in gh_page_files:
        with gh_page_file.open() as f:
            page_json = json.load(f)

        print("Processing " + str(gh_page_file))
        docker_files = [
            get_file_item(item, args.file_type)
            for item in page_json['items']
            if item.get("name") == item_name_in_result
        ]

        for file_item in docker_files:
            save_data(file_item)
