import base64
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

GH_TOKEN = os.getenv("GH_TOKEN")

from ingest.db_model import *

old_db_path = os.path.join(APP_DIR, '..', 'db', 'docker_files.db')

old_db = SqliteDatabase(old_db_path)
old_db.connect()


class OldFileItem(Model):
    file_sha = CharField(primary_key=True)
    file_name = CharField()
    file_path = CharField()
    download_link = CharField()
    html_link = CharField()
    repo_name = CharField()
    repo_desc = CharField(null=True, default="")
    repo_html_link = CharField()
    file_url = CharField()  # To retrieve download_url
    file_content = TextField(null=True, default="")
    decoded_file_content = TextField(null=True, default="")
    time_stamp = DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        database = old_db
        table_name = 'fileitem'


def update_new_db(item):
    existing_fileitem = FileItem.update(
        file_content=item.file_content,
        decoded_file_content=item.decoded_file_content
    ).where(FileItem.file_sha == item.file_sha)
    existing_fileitem.execute()


if __name__ == '__main__':
    items = OldFileItem.select().where(OldFileItem.file_content != "")
    print("Total items: " + str(len(items)))
    for i in items:
        print("Getting contents for " + i.file_url)
        update_new_db(i)
