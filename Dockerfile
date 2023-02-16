FROM python:3.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py


# FROM python:3.8-slim-buster
# RUN apt-get update && apt-get install -y \
#     wget \
#     unzip \
#     && rm -rf /var/lib/apt/lists/*

# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i google-chrome-stable_current_amd64.deb
# RUN apt-get install -y --no-install-recommends xvfb
# RUN rm google-chrome-stable_current_amd64.deb

# RUN wget -q https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
# RUN unzip chromedriver_linux64.zip
# RUN mv chromedriver /usr/bin/chromedriver
# RUN chmod +x /usr/bin/chromedriver
# RUN rm chromedriver_linux64.zip

# RUN pip install selenium

