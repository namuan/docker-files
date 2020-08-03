export PROJECTNAME=$(shell basename "$(PWD)")
export REMOTEDIR=${PROJECTNAME}-v2

.SILENT: ;               # no need for @

venv: ## Sets up venv
	python3 -m venv venv

requirements: ## Sets up required dependencies
	./venv/bin/pip install -r web-infra/requirements.txt
	./venv/bin/pip install -r py-web/requirements.txt
	./venv/bin/ansible-galaxy --version
	./venv/bin/ansible-playbook --version

bootstrap: ## Sets up required directory
	rsync -avzr web-infra/bootstrap.sh root-${PROJECTNAME}:./bootstrap.sh
	ssh root-${PROJECTNAME} -C "/bin/bash ./bootstrap.sh"


doplaybook: ## Start Droplet
	./venv/bin/ansible-galaxy install -r web-infra/requirements.yml
	./venv/bin/ansible-playbook -i web-infra/ansible/hosts web-infra/ansible/digitalocean_playbook.yml -l do

clean: ## Cleans all cached files
	find . -type d -name '__pycache__' | xargs rm -rf

deployapp: clean ## Deploy application
	ssh ${PROJECTNAME} -C "mkdir -vp ./${REMOTEDIR}"
	rsync -avzr \
    		./py-web/docker_files.py \
    		./py-web/app.py \
    		./py-web/requirements.txt \
    		./py-web/db \
    		./py-web/static \
    		./py-web/templates \
    		${PROJECTNAME}:./${REMOTEDIR}/

updatedb: ## Copies the database from local to remote server
	ssh ${PROJECTNAME} -C "mkdir -vp ./${REMOTEDIR}"
	rsync -avzr \
			./py-web/db \
			${PROJECTNAME}:./${REMOTEDIR}/

updateapp: ## Re-generate supervisord by looking at REMOTEDIR variable and restart nginx/supervisord
	./venv/bin/ansible-playbook web-infra/ansible/app_playbook.yml -i web-infra/ansible/hosts -l doremote

ssh: ## ssh into project server
	ssh ${PROJECTNAME}

restart: ## Restarts supervisor
	ssh ${PROJECTNAME} -C "sudo service supervisor restart"

setupplaybook: ## Setup Infrastructure on DigitalOcean
	./venv/bin/ansible-playbook web-infra/ansible/setup_playbook.yml -i web-infra/ansible/hosts -l doremote

deleteinfra: ## Deletes DigitalOcean Droplet
	doctl compute droplet delete ${PROJECTNAME}

run: ## Runs web application locally
	./venv/bin/python py-web/app.py

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo
