FROM python:3.10
ENV PYTHONIOENCODING utf-8
#WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
USER 1000
#CMD [ "python", "./app.py" ]
CMD [ "python", "./__init__.py" ]
