cd github_ingest
pip3.6 install -r requirements.txt --user
bash ./scripts/start_screen.sh docker_files_stage_3 'python3.6 storage_update_file_content.py'