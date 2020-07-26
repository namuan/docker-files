import datetime
import os

from playhouse.sqlite_ext import *

sys.path.append(os.getcwd())

APP_DIR = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(APP_DIR, '..', 'db', 'docker_files_2.db')

print("Loading database from " + db_path)

db = SqliteExtDatabase(db_path)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class FileItem(BaseModel):
    file_sha = CharField(unique=True)
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
    file_type = CharField(null=True, default="")

    def __str__(self):
        return f"{self.file_sha}, {self.file_name}, {self.file_path}"


class FTSEntry(FTSModel):
    content = TextField()

    class Meta:
        database = db


class FTSDockerComposeEntry(FTSModel):
    content = TextField()

    class Meta:
        database = db
