rm data/gh_page_*
echo "Indexing docker files"
python3.6 ingest.py --start-page 1 --end-page 30 --file-type docker_files --search-query "filename:Dockerfile FROM";python3.6 storage.py --file-type docker_files;python3.6 storage_update_file_content.py;python3.6 storage_update_search_index.py

echo "Indexing docker compose files"
rm data/gh_page_*
python3.6 ingest.py --start-page 1 --end-page 30 --file-type docker_compose --search-query "filename:docker-compose.yml";python3.6 storage.py --file-type docker_compose;python3.6 storage_update_file_content.py;python3.6 storage_update_search_index.py

python3.6 status_notifier.py