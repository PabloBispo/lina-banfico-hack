from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
cur = conn.cursor()


def serialize(data):
    new_data = []
    for d in data:
        if not isinstance(d, str):
            try:
                new_data.append(float(d))
            except:
                new_data.append(str(d))
                continue
        else:
            new_data.append(str(d))
    return new_data


# A welcome message to test our server
@app.route('/')
def index():
    try:
        cur.execute("""SELECT * from fundos_investimento""")
        rows = cur.fetchall()
        print([serialize(r) for r in rows[:2]])
        return jsonify({
            "message": "Hackathon",
            'data': [serialize(r) for r in rows]
        })
    except Exception as e:
         return jsonify({
             'Error': str(e),
            "message": "Error",
        })

