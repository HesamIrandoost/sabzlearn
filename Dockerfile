# FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1


# WORKDIR /app

# COPY requirements.txt /app/

# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt

# COPY ./core /app/
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# کپی requirements و نصب پکیج‌ها
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

# کپی کل پروژه
COPY . /app/

# بررسی ساختار
RUN ls -la /app/
RUN ls -la /app/core/