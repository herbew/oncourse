#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Ubuntu 20.04
#|==============================================================================

sudo apt install build-essential checkinstall
sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libpq-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

INSTALL DATABASE
--------------------
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'

sudo apt update
sudo apt install postgresql-10

sudo -u postgres psql -c "CREATE USER uoncourse WITH ENCRYPTED PASSWORD 'PwDoncourseSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_oncourse;"

sudo -u postgres psql db_oncourse -c "GRANT ALL ON ALL TABLES IN SCHEMA public to uoncourse;"
sudo -u postgres psql db_oncourse -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to uoncourse;"
sudo -u postgres psql db_oncourse -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to uoncourse;"

INSTALL MONGODB
--------------------
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

sudo wget --quiet -O - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
sudo apt install gnupg
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install -y mongodb-org
sudo apt install mongodb-org=4.4.4 mongodb-org-server=4.4.4 mongodb-org-shell=4.4.4 mongodb-org-mongos=4.4.4 mongodb-org-tools=4.4.4
ps --no-headers -o comm 1
sudo systemctl start mongod.service
sudo systemctl daemon-reload

sudo systemctl status mongod
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod


IF ANY ERROR ONLY
-------------------
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock
sudo systemctl restart mongod


mongo <<EOF
use db_oncourse_trails;
db.createUser(
  {
    user: "trail_oncourse",
    pwd: "PWDuoncourseSatu23",
    roles: [{ role: "readWrite", db: "db_oncourse_trails" },]
  },
);
use db_oncourse_django_message;
db.createUser(
  {
    user: "django_messages_oncourse",
    pwd: "PWDuoncourseSatu23",
    roles: [{ role: "readWrite", db: "db_oncourse_django_messages" },]
  },
);
use db_trace_oncourse
db.createUser(
  {
    user: "uoncourse",
    pwd: "PWDuoncourseSatu23",
    roles: [{ role: "readWrite", db: "db_trace_oncourse" },]
  }
);

EOF


use db_oncourse_trails
db.dropDatabase();

use db_oncourse_django_message
db.dropDatabase();

use db_trace_oncourse
db.dropDatabase();


db.dropUser("trail_oncourse");
db.dropUser("django_messages_oncourse");
db.dropUser("uoncourse");

true
show users;


sudo apt install language-pack-id
sudo dpkg-reconfigure locales

sudo apt install -y python3 python3-pip 
sudo apt install -y python3-venv

python3 -m pip install --user pipenv

-----------------------------------------------------------------------
https://github.com/
herbew@gmail.com
#!Kevinvania!!23
----------------------------------------------------------------------

git clone https://github.com/herbew/oncourse.git
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



# link with absolute path
sudo ln -s /home/herbew/oncourse /opt/oncourse
cd /opt
sudo python3 -m venv envoncourse
  
source /opt/envoncourse/bin/activate


sudo apt install dos2unix -y 
cd /opt/oncourse

dos2unix utility/install_os_dependencies.sh
dos2unix utility/install_python_dependencies.sh
sudo ./utility/install_os_dependencies.sh install

sudo su

source envoncourse/bin/activate
cd oncourse

sudo -H pip3 install virtualenv
./utility/install_python_dependencies.sh
pip install -r requirements/production.txt
_________________________________________
DATABASE_URL=postgres://uoncourse:PwDoncourseSatu1Dua3@127.0.0.1/db_oncourse

DJANGO_ADMIN_URL=admin/
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=#6kuxzt=%fb(+npb18f%l$b$t2+nkh*t48*2$l&r4-h-zyprn6

DJANGO_EMAIL_BACKEND=anymail.backends.mailjet.EmailBackend
DJANGO_SERVER_EMAIL=
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_DEBUG=True

DJANGO_MAILGUN_API_KEY=
DJANGO_MAILGUN_SERVER_NAME=

DJANGO_EMAIL_HOST=
DJANGO_EMAIL_PORT=
DJANGO_EMAIL_USER=
DJANGO_EMAIL_PASSWORD=

MAILJET_API_KEY=
MAILJET_SECRET_KEY=

REDIS_URL=redis://localhost:6379
REDISTOGO_URL=redis://localhost:6379
IP_MONGODB=localhost
IP_REDIS=localhost
	
____________________________________________________________________________


 python3 ./manage.py migrate sites
 python3 ./manage.py makemigrations users
 python3 ./manage.py migrate users
 
 python3 ./manage.py makemigrations workbooks
 python3 ./manage.py migrate workbooks
 
 python3 ./manage.py makemigrations masters
 python3 ./manage.py makemigrations academics
 python3 ./manage.py makemigrations

 python3 ./manage.py migrate
 
 python3 ./manage.py update_translation_fields users
 
 python3 ./manage.py collectstatic --noinput
 python3 ./manage.py shell -c "from oncourse.apps.users.models import User; User.objects.create_superuser('herbew', 'herbew@gmail.com', 'password')"
 python3 ./manage.py shell -c "from oncourse.apps.users.models import User; user = User.objects.get(username='herbew'); user.types='001'; user.save()"
 
 
#Redis
sudo apt install redis-server redis
 
 
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl restart redis
sudo systemctl daemon-reload
sudo systemctl status redis

#Gunicorn

assume absolute path of the source /home/herbew/oncourse/
vi /home/herbew/oncourse/config/systemd/gunicorn/gunicorn.service
user as herbew
____________:

User=herbew
WorkingDirectory=/home/herbew/oncourse
ExecStart=/home/herbew/envoncourse/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/herbew/herbew.sock config.wsgi:application

____________

IF LIVE:
sudo cp -f config/systemd/gunicorn/gunicorn.service /etc/systemd/system/gunicorn.service

IF LOCAL:
sudo cp -f config/systemd/gunicorn/local-gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl status gunicorn

#RQWorker
assume absolute path of the source /home/herbew/oncourse/
user as herbew
____________:

User=herbew
WorkingDirectory=/home/herbew/oncourse
ExecStart=/home/herbew/envoncourse/bin/python3 /home/herbew/oncourse/manage.py rqworker high default low

____________

IF LIVE:
sudo cp -f config/systemd/rqworker/rqworker.service /etc/systemd/system/rqworker.service

IF LOCAL:
sudo cp -f config/systemd/rqworker/local-rqworker.service /etc/systemd/system/rqworker.service

sudo systemctl enable rqworker
sudo systemctl start rqworker
sudo systemctl restart rqworker
sudo systemctl daemon-reload
sudo systemctl status rqworker

#HTTPS--Cerbot
sudo apt install certbot python3-certbot-nginx

IF ANY ERROR
------------
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

sudo ln -s /snap/bin/certbot /usr/bin/certbot


#NGINX
assume absolute path of the source /home/herbew/oncourse/
user as herbew
vi /home/herbew/oncourse/config/nginx/local-nginx.conf

sudo apt install nginx

sudo cp -f config/nginx/local-nginx.conf /etc/nginx/sites-available/oncourse
sudo ln -s /etc/nginx/sites-available/oncourse /etc/nginx/sites-enabled/

sudo chown -R www-data:www-data /var/log/nginx;
sudo chmod -R 755 /var/log/nginx;

#Test--
sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful


sudo service nginx configtest

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl daemon-reload
sudo systemctl status nginx


sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart rqworker

http://192.168.0.121:8080/en-us/master/document/list/

#ONLY change 
sudo vi /etc/nginx/sites-available/oncourse
server {

          access_log /var/log/nginx/access.log combined;
      add_header Cache-Control no-cache;

          listen 80;
          server_name  192.168.0.121;

       ...

sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart rqworker


sudo apt install redis-server

source envoncourse/bin/activate
cd oncourse
python3 ./manage.py oncourse_chotot 0
