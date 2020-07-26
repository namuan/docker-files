import logging
from json.decoder import JSONDecodeError

from ingest.db_model import *

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# def items_with_no_tags():
#     return (
#         FileItem
#             .select(FileItem.file_url, FileItem.decoded_file_content)
#             .join(FileItemTags, JOIN.LEFT_OUTER)
#             .where(FileItemTags.tag.is_null(False))
#     )


# def multiple_queries_n_plus_1():
#     ids = ['c5f4f14f9a5f17cd29e14c3c71d29166f9fe13d4', '132fa12de05447b41a07ac6e7b1ba8480646d312', '1675eae96e2cf170465c34e0fbc5a975b20b3021']
#     file_items = (FileItem.select().where(FileItem.file_sha << ids))
#     file_item_tags = (FileItemTags.select(FileItemTags, Tag).join(Tag).where(FileItemTags.file_item in file_items))
#     return prefetch(file_items, file_item_tags)

if __name__ == '__main__':
    file_sha = "3076680a729d416541968486ee52e94dde858ee9"
    for fi in FileItem.select():
        try:
            j = json.loads(fi.decoded_file_content)
            print(fi.id)
            print(fi.decoded_file_content)
        except JSONDecodeError:
            pass

    # db_item = FileItem.get(FileItem.file_sha == file_sha)
    # print(db_item.decoded_file_content)
