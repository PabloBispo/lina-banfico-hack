from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
cur = conn.cursor()


db_columns = [
    'id',
    'name',
    'aplicacao_minima',
    'taxa_adm',
    'cotizacao_resgate',
    'liquidacao_resgate',
    'risco',
    'classe_risco',
    'rentabilidade_mes',
    'rentabilidade_ano',
    'rentabilidade_12m',
    'cnpj',
    'classificacao_cvm',
    'patrimonio_liquido',
    'pl_medio_12m',
    'taxa_adm_percent',
    'class_lyze',
    'inicio_fundo',
    'benchmark',
    'custodiante']



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
    return {column: new_data[i] for i, column in enumerate(db_columns)}


@app.errorhandler(404) 
def not_found(e): 
    return jsonify({
            "message": "Route not found",
        }), 404
  


# A welcome message to test our server
@app.route('/fundos-investimento')
def index():
    limit = request.args.get('limit')
    if not limit:
        limit = 100
    try:
        cur.execute(f"""SELECT * from fundos_investimento limit {limit}""")
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

