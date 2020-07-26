## Import files from Github

#### Initialise server and Deploy code

```
make initserver
make deploy
```

#### Run pipeline for refreshing database

Switch to the correct python version

```
pyenv global 3.7.2
```

Output: Updates the database file with updated entries.
IMPORTANT: If on a new remote machine then remember to dbrestore database from local machine (dropbox)

```
make dfpipeline # Update Docker files

or

make dcpipeline # Update Docker compose files
```

### Backup database and copy to Py-Web

Download the database from remote server

```
make dbbackup
cp db/docker_files_2.db ../py-web/db/docker_files_2.db
cd ../py-web
make run
```

Then make sure website is running properly before pushing

If data is corrupted then check the Rollback section

Other run the following command to push the latest database to live

```
make stagetwo restart
```

If everything is good then copy the database to dropbox

```
cp db/docker_files_2.db ./infra/certs/docker_files_2.db
```

Back to the ingest folder to start again

```
cd ../ingest
```

### Rollback

We will revert to the last known database from dropbox and check the ingestion process again

```
cd ../ingest
cp ../py-web/infra/certs/docker_files_2.db db/docker_files_2.db
make dbrestore
```


