FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt /app/
RUN pip install --upgrade pip  && \
        pip install -Ur requirements.txt  && \
        pip install gunicorn[gevent] && \
        pip cache purge
ADD . /app/
