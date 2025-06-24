import os
import json
import sqlite3
import logging
from logging import Formatter
import requests
from flask import Flask, request
from adp.adp_bp import adp_bp
from random_bp.random_bp import random_bp
from tableau.tableau_bp import tableau_bp
from pymongo import MongoClient
import psycopg2
from psycopg2 import ProgrammingError

# Azure Monitor
from azure.monitor.opentelemetry import configure_azure_monitor
# Open Telemetry
from opentelemetry.instrumentation.flask import FlaskInstrumentor
#from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor


os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING'] = "InstrumentationKey=56013065-f508-49f2-bf83-4ee08c674cb5;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=746d46f0-8f21-4d13-a11e-df7c335f5e25"
os.environ["OTEL_SERVICE_NAME"] = "local-api"
app = Flask(__name__)

configure_azure_monitor(
    # Set logger_name to the name of the logger you want to capture logging telemetry with
    # This is imperative so you do not collect logging telemetry from the SDK itself.
    logger_name="main",
    # You can specify the logging format of your collected logs by passing in a logging.Formatter
    logging_formatter=Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    enable_live_metrics=True
)

FlaskInstrumentor().instrument_app(app, enable_commenter=True)
#PsycopgInstrumentor().instrument()
#PymongoInstrumentor().instrument()
Psycopg2Instrumentor().instrument()

app.register_blueprint(adp_bp, url_prefix='/adp')
app.register_blueprint(random_bp, url_prefix="/random")
app.register_blueprint(tableau_bp, url_prefix="/tableau")
client = MongoClient("mongodb://root:example@localhost:9001")
con = sqlite3.connect("sqlite3.db")
cur = con.cursor()
#pgcon = psycopg2.connect("dbname=PGDataBaseName user=postgres password=test host=localhost")
log = logging.getLogger("main")

@app.before_request
def save_request_info():
    headers = str(request.headers)
    sql = f"INSERT INTO request(headers,method,url) VALUES('{request.headers}', '{request.method}', '{request.url}');"
    #execute_sql_2(sql)
    #execute_sql(sql)


@app.route("/v1/demographics/questions")
def hello_world():
    q = None
    with open('./questions.json', 'r') as f:
        q = json.load(f)
    return q

@app.route("/JSSResource/classes")
def classes():
    log.info("test log")
    print(request.headers)
    return [
    {
    "size": 1,
    "class": {
      "id": 1,
      "name": "Biology 101",
      "description": "string"
    }
  },
  {
    "size": 1,
    "class": {
      "id": 2,
      "name": "Q",
      "description": "string"
    }
  }
]

@app.route("/JSSResource/classes/id/<int:id>")
def class_detail(id):
    q = None
    with open("./classes.json", 'r') as f:
        q = json.load(f)
    return q

@app.route("/api/oauth/token", methods=['POST'])
def auth():
    return {
            "expires_in": 1774633785,
            "access_token": "some token"
        }

@app.route("/external")
def external():
    app.logger.info("guilherme@relyance.ai")
    resp = requests.head("http://google.com", allow_redirects=True)
    return {"status": resp.status_code}

@app.route("/external2")
def external2():
    resp = requests.get("http://localhost:9002/")
    return resp.text

@app.route("/mongocall")
def mongocall():
    db = client.admin
    collection = db["system.users"]
    app.logger.info(f"searching {collection.count_documents({})}")
    execute_sql_2("select now();")
    return {"size": collection.count_documents({})}

@app.route("/pgcall")
def pgcall():
    requests = execute_sql_2("select * from request order by time DESC limit 10;")
    return {"requests": list(requests)}
    

def execute_sql(statement):
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute(statement)
    con.commit()

def execute_sql_2(statement):
    cur = pgcon.cursor()
    cur.execute(statement)
    pgcon.commit()
    try:
        return cur.fetchall()
    except ProgrammingError:
        return []
    except Exception as ex:
        app.logger.error(f"Error getting results. Ex: {ex}", exc_info=True)
    return []



if __name__ == "__main__":
    print(app.url_map)
    print(app.name)
    #execute_sql_2("CREATE TABLE IF NOT EXISTS request(headers TEXT, method TEXT, url TEXT, time TIMESTAMP DEFAULT NOW());")
    #execute_sql("CREATE TABLE IF NOT EXISTS request(headers TEXT, method TEXT, url TEXT, time TIMESTAMP);")
    app.logger.setLevel(logging.INFO)


    app.run(debug=True)
