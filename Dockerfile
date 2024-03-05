FROM python:latest
LABEL authors="bill"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/backend"

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


COPY backend /usr/src/app/backend
CMD ["python", "-c", "import sys; print(sys.path)"]