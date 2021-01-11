from flask import Flask, request, jsonify, send_file, send_from_directory, make_response
import base64

import os
import psycopg2

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'postgres://fqmbdxwkpbcuqi:f23a13e4f3c0a435a77936acb35f3ca5f21913831079cca51ebbe8c08feee72a@ec2-54-208-233-243.compute-1.amazonaws.com:5432/ddbcde6i8m9ph3'
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


@app.route("/fazenda")
def fazenda():
    cur.execute(f"""SELECT (html) from html_data""")
    data = cur.fetchone()
    if data:
        data = data[0]
    return data, 200


@app.route("/zip_file")
def zip_file():
    return jsonify({
        "data": {
            "zip_file": base64.b64encode(open('zip/mercadolivre.zip', 'rb').read()).decode('ascii')  
        }
    })

'''
@app.route('/pdfs')
def get_pdf(id=None):
    binary_pdf = open('pdfs/6257265_65727.34222.806641.41385247.pdf', 'rb').read()
    response = make_response(binary_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % '6257265_65727.34222.806641.41385247'
    return response
    '''