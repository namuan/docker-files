import base64
import time
from json.decoder import JSONDecodeError

import requests
from dotenv import load_dotenv

from ingest.db_model import *

load_dotenv(verbose=True)

GH_TOKEN = os.getenv("GH_TOKEN")


def send_request(git_url):
    try:
        github_headers = {
            "Accept": "application/vnd.github.VERSION.raw",
            "Authorization": f"token {GH_TOKEN}"
        }
        response = requests.get(
            url=git_url,
            headers=github_headers
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        return response.text
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == '__main__':
    items = FileItem.select().where(FileItem.file_content == "")
    print("Total items: " + str(len(items)))
    for i in items:
        ignored_item = False
        print("Getting contents for " + i.file_url)
        docker_file = send_request(i.file_url)
        try:
            json_content = json.loads(docker_file)
            i.delete_instance()
            ignored_item = True
        except JSONDecodeError:
            pass

        if not ignored_item:
            i.file_content = base64.b64encode(bytes(docker_file, 'utf-8'))
            i.decoded_file_content = docker_file
            i.save()

        time.sleep(60)
