## Import files from Github

Following steps are required to update the database behind docker-files.com

Note: Restore the database if it is new remote machine

```bash
make updatedb
```

#### Run pipeline for refreshing database

Deploy latest indexing code

```bash
make -f IngestMakefile deploy
```

Start pipeline to index files

```
make -f IngestMakefile pipeline
```

### Backup database and copy to Py-Web

Download the database from remote server

```
make -f IngestMakefile dbbackup
cp ./ingest/db/docker_files_2.db ./py-web/db/docker_files_2.db
make run
```

Then make sure website is running properly before pushing

If data is corrupted then check the Rollback section

Other run the following command to push the latest database to live

```
make updatedb updateapp
```

If everything is good then commit everything to Github

Navigate back to the folder to start the process again

```
cd ingest
```

### Rollback

We will revert to the last known database from Github and re-start indexing

