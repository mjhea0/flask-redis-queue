# base image
FROM ubuntu:20.04

# Set location
ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

# Update and install python, pip
RUN apt-get update -y
RUN apt-get install tzdata
RUN apt-get install -y python3-pip python3-dev build-essential curl
RUN apt-get update -y
RUN apt upgrade -y
RUN apt-get install -y wkhtmltopdf

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update
RUN apt-get -y install tesseract-ocr
# pytesseract using pip forgot to install binaries.
# Ref: https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror
# Ref: https://docs.ropensci.org/tesseract/
RUN apt-get install -y libtesseract-dev libleptonica-dev tesseract-ocr-eng
RUN cd /usr/share/tesseract-ocr/4.00/tessdata/
RUN apt install wget
RUN wget https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata
RUN cd /usr/share/tesseract-ocr/4.00/tessdata/
RUN wget https://github.com/tesseract-ocr/tessdata/blob/main/osd.traineddata

CMD /bin/bash

# LABEL about the custom image
LABEL maintainer="vaibhav.hiwase@gmail.com"
LABEL version="0.1"
LABEL description="This is custom Docker Image."

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install some requirements (not a part of this project)
RUN pip3 install pip --upgrade
RUN pip3 install pillow==8.3.2
RUN pip3 install pytesseract==0.3.8
RUN pip3 install spacy==3.2.4
RUN python3 -m spacy download en_core_web_sm

# Add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# Install depedencies
RUN pip3 install -r requirements.txt


# Copy project
COPY . /usr/src/app

EXPOSE 5000
CMD ["python3", "-u", "manage.py", "run", "-h", "0.0.0.0"]