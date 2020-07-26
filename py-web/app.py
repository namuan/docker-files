import base64
import datetime
import logging
import os

from flask import Flask, render_template, request
from playhouse.flask_utils import FlaskDB, PaginatedQuery
from playhouse.sqlite_ext import *

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'db', 'docker_files_2.db')

app = Flask(__name__)
app.config.from_object(__name__)

flask_db = FlaskDB(app)
database = flask_db.database


class FileItem(flask_db.Model):
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

    @property
    def decoded_file(self):
        return base64.b64decode(self.file_content).decode("utf-8", "strict")


class FTSEntry(FTSModel):
    content = TextField()

    class Meta:
        database = database


class FTSDockerComposeEntry(FTSModel):
    content = TextField()

    class Meta:
        database = database


class FTSKubeComposeEntry(FTSModel):
    content = TextField()

    class Meta:
        database = database


def search_docker_compose(search_query):
    return (FileItem
            .select(FileItem, FTSDockerComposeEntry.rank().alias('score'))
            .join(FTSDockerComposeEntry, on=(FileItem.id == FTSDockerComposeEntry.docid))
            .where(FTSDockerComposeEntry.match(search_query))
            .order_by(FileItem.time_stamp.desc(), FTSDockerComposeEntry.rank().desc()))


def search_docker_files(search_query):
    return (FileItem
            .select(FileItem, FTSEntry.rank().alias('score'))
            .join(FTSEntry, on=(FileItem.id == FTSEntry.docid))
            .where(FTSEntry.match(search_query))
            .order_by(FileItem.time_stamp.desc(), FTSEntry.rank().desc()))


def query_for_search(search_item, file_type):
    search_items = search_item.split()
    and_search_query = " AND ".join(search_items)
    if file_type == "docker_compose":
        return search_docker_compose(and_search_query)
    else:
        return search_docker_files(and_search_query)


def query_for_default(_, file_type):
    return (FileItem
            .select()
            .where(FileItem.file_type == file_type)
            .order_by(FileItem.time_stamp.desc())
            )


query_type_mapping = {
    'search': query_for_search
}

file_type_mapping = {
    'docker_files': 'docker_files',
    'docker_compose': 'docker_compose'
}

PAGE_SIZE = 10


@app.route("/")
def index():
    page_no = request.args.get('page', type=int) or 1
    query_type = request.args.get('qt', type=str)
    query_param = request.args.get('qp', type=str) or ''
    file_type = file_type_mapping.get(request.args.get('ft', type=str), 'docker_files')

    if not query_param:
        query_type = "default"

    file_items_query = query_type_mapping.get(query_type, query_for_default)(query_param, file_type)

    paginated_query = PaginatedQuery(
        file_items_query,
        paginate_by=PAGE_SIZE,
        page=page_no)

    paginated_query_iter = paginated_query.get_object_list()

    return render_template(
        'pages/placeholder.main.html',
        page_count=paginated_query.get_page_count(),
        page=paginated_query.get_page(),
        file_with_tags=paginated_query_iter,
        qt=query_type,
        qp=query_param,
        ft=file_type
    )


@app.template_filter('highlight_search')
def highlight_search(request_args):
    query_type = request.args.get('qt', type=str)
    query_param = request.args.get('qp', type=str)
    if query_type == "search":
        re_qp = re.compile(query_param, re.IGNORECASE)
        request_args = re_qp.sub(lambda m: '<span class="highlighted">%s</span>' % m.group(0), request_args)

    return request_args


def main():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
