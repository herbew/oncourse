FROM python:3.10

	ENV PYTHONUNBUFFERED 1
    
	RUN mkdir -p /opt/oncourse
	COPY . ./opt/oncourse
	
	WORKDIR /opt/oncourse
	RUN chmod +x compose/django/docker-entrypoint.sh
	RUN pip3 install -r requirements/production.txt





