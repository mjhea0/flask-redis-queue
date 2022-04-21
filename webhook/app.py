# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import pprint
from os import environ

from flask import Flask, request

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

try:
    WEBHOOK_ENDPOINT = environ.get("WEBHOOK_ENDPOINT")
except RuntimeError:
    WEBHOOK_ENDPOINT = None

print("WEBHOOK_ENDPOINT:", WEBHOOK_ENDPOINT)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route("/", methods=["POST"])
# ‘/’ URL is bound with webhook_function() function.
def webhook_function():
    try:
        data = eval(request.data)
    except Exception:
        data = request.data
    print()
    print("Webhook received following output ...")
    print()
    pprint.pprint(data)
    print("----------" * 10)
    print()
    print()
    return data


# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    port = WEBHOOK_ENDPOINT.replace("http://webhook:", "")
    app.run(host="0.0.0.0", port=port)
