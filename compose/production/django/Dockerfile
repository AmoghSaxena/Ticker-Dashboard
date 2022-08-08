
FROM python:3.9

ENV PYTHONUNBUFFERED 1

# RUN apk update \
#   # psycopg2 dependencies
#   && apk add --virtual build-deps gcc python3-dev musl-dev \
#   # && apk add-dev \
#   # Pillow dependencies
#   && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
#   # CFFI dependencies
#   && apk add libffi-dev py-cffi

# RUN addgroup -S django \
#     && adduser -S -G django django
# RUN addgroup django \
#     && adduser --system --group django

RUN apt  update
    # && apt install net-tools iptoute2 pyhton3.9 command-not-found python3-pip python-is-python openssh-server mariadb-server -y


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/production.txt 
    

# COPY ./compose/production/django/entrypoint /entrypoint
# # RUN sed -i 's/\r$//g' /entrypoint
# RUN chmod +x /entrypoint
# RUN chown django /entrypoint

COPY ./compose/production/django/copyadmin /copyadmin
RUN sed -i 's/\r$//g' /copyadmin
RUN chmod +x /copyadmin
# RUN /copyadmin

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# COPY ./compose/local/django/celery/flower/start /start-flower
# RUN sed -i 's/\r$//g' /start-flower
# RUN chmod +x /start-flower

# RUN chown django /start
COPY . /app

# RUN chown -R django /app
RUN cp /app/AdminFiles/* /usr/local/lib/python3.9/site-packages/admin_volt/templates/admin/
# USER django

WORKDIR /app

# RUN python /app/manage.py makemigrations
# RUN python /app/manage.py migrate

# ENTRYPOINT ["/entrypoint"]
