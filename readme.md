1. install docker 
2. install docker-compose
3. git clone repo
4. cd to folder
5. virtualenv
6. source venv/bin/activate
7. pip install -r requirements.txt
8. echo -e "AIRFLOW_UID=$(id -u)" > .env
9. docker compose up airflow-init
10. docker compose up
