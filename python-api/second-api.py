from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/hit")
def hit():
    service=request.args.get("service")
    method=request.args.get("method", "GET")
    response = requests.request(method, url=service)
    return {"status": response.status_code}

if __name__=="__main__":
    app.run(port=5003)
