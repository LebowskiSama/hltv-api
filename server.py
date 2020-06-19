from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from scrape import fetchLive, fetchUpcoming

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route('/live')
@cross_origin()
def serveLive():
    live = fetchLive()
    return(jsonify({"live": live}))

@app.route('/upcoming')
@cross_origin()
def serveUpcoming():
    upcoming = fetchUpcoming()
    return(jsonify({"upcoming": upcoming}))