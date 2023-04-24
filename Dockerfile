FROM python:3.8-slim-buster
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD [ "python", "app.py" ]