# TextLabel

## Description
TextLabel is an open-source web application prototype built on the SnorkelAI framework, designed to simplify and accelerate distributed text data labeling through weak supervision via label functions.
The web application consists of two main software components: a Django backend and an Angular frontend. The Django backend handles data processing, model integration, and weak supervision logic, while the Angular frontend provides a responsive and user-friendly interface for interacting with the system. 

## Installation

### Backend
The application can be built using Docker. To build the backend, navigate to the text_label_backend directory and run:

```docker build -t <repo>:<tag> .``` 

When starting the container, an .env file must be provided, which should contain the following

```
DJANGO_SECRET_KEY=<your_secret_key>
DJANGO_ALLOWED_HOSTS=<your_allowed_hosts as list localhost,1234web.de>
CORS_ALLOWED_ORIGINS=<your_allowed_origins as list>
DEBUG=<True_or_False>
```

Optionally, a superuser can be created. This will be done automatically when the container starts, provided that the following environment variables are set (and the superuser does not already exist):

```
DJANGO_SUPERUSER_USERNAME=<your_username>
DJANGO_SUPERUSER_EMAIL=<your_email>
DJANGO_SUPERUSER_PASSWORD=<your_password>
```

Note: The backend project settings require an SSL certificate. If you do not have one, you will need to modify or comment out the relevant settings in text_label_backend/text_label_backend/settings.py.

### Frontend
To build the frontend, navigate to the text-label-frontend directory and run:

```docker build -t <repo>:<tag> .``` 

Note that the URLs for backend communication are pre-configured. For custom usage, you'll need to adjust the environment variables in the text-label-frontend/src/environments folder to reflect your backend server settings.

### NGINX Configuration
For personal use, the NGINX configuration must be adjusted to reflect your specific setup. Ensure that the NGINX settings are properly configured to route traffic between the frontend and backend as needed.


## Support
If you encounter any issues, you can open a new issue on the repository or send an email to marie.braun@hhu.de for assistance.
