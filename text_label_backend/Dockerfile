# Python image
FROM python:3.9

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app
# install all dep
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

# copy code
COPY . .
#
## create superuser
#ARG DJANGO_SUPERUSER_USERNAME=admin
#ARG DJANGO_SUPERUSER_EMAIL=admin@example.com
#ARG DJANGO_SUPERUSER_PASSWORD=admin_password
#
#RUN python manage.py makemigrations && \
#    python manage.py migrate && \
#    echo "from django.contrib.auth.models import User; \
#    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | \
#    python manage.py shell

EXPOSE 8080

# webserver
RUN python manage.py collectstatic --noinput
RUN pip install gunicorn

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "text_label_backend.wsgi:application"]

#--platform=linux/amd64