FROM python:3.10

RUN mkdir /vk_bot_farm

WORKDIR /vk_bot_farm

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1

COPY requirments.txt .

RUN pip install --no-cache-dir --upgrade -r requirments.txt

COPY . .