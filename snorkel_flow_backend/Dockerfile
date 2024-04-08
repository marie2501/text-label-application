# Python image
FROM python:3.9-slim
# working dict and give rights to swlite
WORKDIR /app
# install all dep
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora
# copy code
COPY . .

# create superuser
ARG DJANGO_SUPERUSER_USERNAME=admin
ARG DJANGO_SUPERUSER_EMAIL=admin@example.com
ARG DJANGO_SUPERUSER_PASSWORD=admin_password

RUN python manage.py migrate && \
    echo "from django.contrib.auth.models import User; \
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | \
    python manage.py shell

EXPOSE 8080

# webserver
RUN pip install gunicorn
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "snorkel_flow_backend.wsgi:application"]

#--platform=linux/amd64