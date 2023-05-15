FROM --platform=linux/x86_64 python:3.11-slim


# Change working directory
WORKDIR /app/


# Copy project files
COPY ./ ./


# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile


CMD sleep 3 \
    && python manage.py migrate \
    && python manage.py runserver 0.0.0.0:80

