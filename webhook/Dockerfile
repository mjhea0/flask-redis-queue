FROM python:3.10-alpine

RUN pip install pip --upgrade
RUN pip install Flask==2.0.3

# Copy project
COPY . .

EXPOSE 8888
CMD ["python3", "-u", "app.py", "-h", "0.0.0.0"]