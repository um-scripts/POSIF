#Flask download
#pip install Flask
#Celery Download
#pip install celery
#download redis
#pip install redis
#-----------OR
#pip install -r requirements.txt


To run Flask:
$ flask --app main run --host[HOST] --port[PORT]

To run worker thread in Celery:
$ celery -A main.celery worker -l info -n [WORKER_NAME]@%h

To run Celery Beat schedule:
$ celery -A main.celery beat

To run Redis:
$ redis-server


[Unit]
Description=Gunicorn instance to serve Flask
After=network.target
[Service]
User=group01
Group=mygroup
WorkingDirectory=/home/group01/upasana_POSIF/SRNA_PREDWeb_IF2
Environment="PATH=/home/group01/upasana_POSIF/SRNA_PREDWeb_IF2/venv/bin"
ExecStart=/home/group01/upasana_POSIF/SRNA_PREDWeb_IF2/venv/bin/gunicorn --bind 0.0.0.0:5500 wsgi:app
[Install]
WantedBy=multi-user.target