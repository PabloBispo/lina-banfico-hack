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
    cur.execute(f"""SELECT (html) from html_data""")
    data = cur.fetchone()
    if data:
        data = data[0]
    return data, 200