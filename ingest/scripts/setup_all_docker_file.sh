pip3 install -r requirements.txt --user
rm data/gh_page_*
bash ./scripts/start_screen.sh docker_files_pipeline 'python3.6 ingest.py --start-page 1 --end-page 30 --file-type docker_files --search-query "filename:Dockerfile FROM";python3.6 storage.py --file-type docker_files;python3.6 storage_update_file_content.py;python3.6 storage_update_search_index.py;python3.6 status_notifier.py'

