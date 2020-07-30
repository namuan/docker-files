## Import files from Github

Following steps are required to update the database behind docker-files.com

#### Run pipeline for refreshing database

Deploy latest indexing code

```bash
make -f IngestMakefile deploy
```

Update Docker files

```
make -f IngestMakefile dfpipeline
```

Update Docker compose files

```
make -f IngestMakefile dcpipeline
```

### Backup database and copy to Py-Web

Download the database from remote server

```
make -f IngestMakefile dbbackup
cp db/docker_files_2.db ../py-web/db/docker_files_2.db
cd ../py-web
make run
```

Then make sure website is running properly before pushing

If data is corrupted then check the Rollback section

Other run the following command to push the latest database to live

```
make updateapp
```

If everything is good then commit everything to Github

Back to the ingest folder to start again

```
cd ../ingest
```

### Rollback

We will revert to the last known database from Github and re-start indexing

