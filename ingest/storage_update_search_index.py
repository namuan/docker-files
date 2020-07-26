from ingest.db_model import *


def update_fts_entry(df_item):
    exists = (FTSEntry
              .select(FTSEntry.docid)
              .where(FTSEntry.docid == df_item.id)
              .exists())
    print("Search entry exists:" + str(exists))
    if not exists:
        FTSEntry.insert({
            FTSEntry.docid: df_item.id,
            FTSEntry.content: df_item.decoded_file_content}).execute()


def update_fts_docker_compose_entry(dc_item):
    exists = (FTSDockerComposeEntry
              .select(FTSDockerComposeEntry.docid)
              .where(FTSDockerComposeEntry.docid == dc_item.id)
              .exists())
    print("Search entry exists:" + str(exists))
    if not exists:
        FTSDockerComposeEntry.insert({
            FTSDockerComposeEntry.docid: dc_item.id,
            FTSDockerComposeEntry.content: dc_item.decoded_file_content}).execute()


if __name__ == '__main__':
    items = FileItem.select().where(FileItem.file_content != "")
    print("Total items: " + str(len(items)))
    for i in items:
        print("File type: " + i.file_type + ", contents for " + i.file_url)
        if i.file_type == "docker_files":
            update_fts_entry(i)
        elif i.file_type == "docker_compose":
            update_fts_docker_compose_entry(i)
        else:
            raise Exception("Unsupported file type")
