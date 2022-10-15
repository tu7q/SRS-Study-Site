FROM redis:latest

# create and set /opt/djangoapp as the working directory
RUN mkdir -p /opt/app/web
WORKDIR /opt/app

# copy entrypoint and make it executable
COPY ./services/celery_broker/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Change to non-root privilege
USER redis

