from json.decoder import JSONDecodeError

import click

from ingest.db_model import *


@click.group()
def cli():
    pass


@cli.command(short_help='Drop Indexes tables')
def drop_indexes():
    db.drop_tables([FTSEntry, FTSDockerComposeEntry])


@cli.command(short_help='Find and purges invalid entries from FileItem table')
def purge_invalid():
    for fi in FileItem.select():
        try:
            json.loads(fi.decoded_file_content)
            print(fi.decoded_file_content)
            fi.delete_instance()
        except JSONDecodeError:
            pass


@cli.command(short_help='Rebuilds database indexes with existing data in FileItem table')
def create_tables():
    db.create_tables([FileItem, FTSEntry, FTSDockerComposeEntry], safe=True)


if __name__ == '__main__':
    cli()
