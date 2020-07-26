cd github_ingest
pip3.6 install -r requirements.txt --user
rm data/gh_page_*
bash ./scripts/start_screen.sh docker_files 'python3.6 ingest.py --start-page 1 --end-page 30 --file-type docker_compose --search-query "filename:docker-compose.yml"'