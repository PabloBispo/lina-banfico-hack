from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
cur = conn.cursor()



@app.errorhandler(404) 
def not_found(e): 
    return jsonify({
            "message": "Route not found",
        }), 404
  


@app.route("/")
def home():
    return '''<h1>Wellcome to UAG</h1>'''