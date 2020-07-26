export PROJECTNAME=dfiles

.SILENT: ;               # no need for @


clean: ## Cleans all cached files
	find . -type d -name '__pycache__' | xargs rm -rf

initserver: ## Initialize the server and check for pre-requisites
	echo "Checking dependencies on server"
	ssh imon@${PROJECTNAME} -C 'mkdir -vp ./github_ingest/db;mkdir -vp ./github_ingest/data'
	ssh imon@${PROJECTNAME} -C 'python3.6 --version'

deploy: clean ## Copies any changed file to the server
	rsync -avzr \
		.env \
		admin.py \
		ingest.py \
		storage.py \
		storage_update_file_content.py \
		storage_update_search_index.py \
		status_notifier.py \
		README.md \
		requirements.txt \
		ingest \
		scripts \
		imon@${PROJECTNAME}:./github_ingest

backup: ## Copies the remote json files locally
	echo "Restoring json files"; \
	scp imon@${PROJECTNAME}:'./github_ingest/data/gh_page_*.json' ./data/;

dbrestore: ## Restore local database to remote
	echo "Restoring local db files"; \
	scp ./db/*.db imon@${PROJECTNAME}:'./github_ingest/db/';

dbbackup: ## Copies the remote database locally
	echo "Backup database files"; \
	scp imon@${PROJECTNAME}:'./github_ingest/db/*.db' ./db/;

dfpipeline: deploy ## Run all stages to process Dockerfiles
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_all_docker_file.sh"'

dcpipeline: deploy ## Run all stages to process Dockerfiles
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_all_docker_compose.sh"'

stageone: deploy ## Download Pages from GH for a search query
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_app.sh"'

stagetwo: deploy ## Populate DB from GH Pages
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_stage2.sh"'

stagethree: deploy ## Download Sourcecode for each file reference
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_stage3.sh"'

stagefour: deploy ## Update search index
	ssh imon@${PROJECTNAME} -C 'bash -l -c "./github_ingest/scripts/setup_stage4.sh"'

ssh: ## SSH into the target VM
	ssh imon@${PROJECTNAME}

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in Docker-files ingest:"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo
