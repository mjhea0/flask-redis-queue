FROM python:3.10-alpine

RUN pip install rq-dashboard

# https://github.com/rq/rq/issues/1469
RUN pip uninstall -y click
RUN pip install click==7.1.2

EXPOSE 9181

CMD ["rq-dashboard"]
