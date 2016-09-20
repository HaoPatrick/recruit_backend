Deploy
====
This project was written in Python (django 1.9.9)

## for develop
```
python3 manage.py makemigrations
python3 manage.py migrate # construct the database to the parent folder
-------------
python3 manage.py runserver 0.0.0.0:8080 # run dev server
```

## for deploy
```
# Docker + Nginx + Supervisor + Gunicorn was the recommended suit.
# Please follow the official tutorial
```
###  Posible config
#### gunicron
```
[program:gunicorn]
command=/usr/local/bin/gunicorn --bind 0.0.0.0:8001 recruit_backend.wsgi:application
directory=/home/hao/recruit
user=hao
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=/var/log/recruit/nodehook.err.log
stdout_logfile=/var/log/recruit/nodehook.out.log
```
#### Nginx
```
server {
        listen          443 ssl;
        server_name     servername;
        ssl     on;

        access_log      /var/log/nginx/default_access.log;
        error_log       /var/log/nginx/default_error.log;

        ssl_certificate /etc/nginx/ssl/haoxiangpeng.crt;
        ssl_certificate_key /etc/nginx/ssl/haoxiangpeng.key;
        ssl_protocols   TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers     HIGH:!aNULL:!MD5;
        location / {
                proxy_pass http://localhost:8001;
                proxy_set_header           Host $host;
                proxy_redirect          off;
	}
}
```

### Backup the database
```
python3 backdb.py
# use rsync to transfer the database file to another server
# please replace the server name and your ssh config
```
