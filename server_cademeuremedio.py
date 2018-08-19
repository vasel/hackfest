import os

import requests
from flask import Flask
from flask_cors import CORS, cross_origin

import funcoes_cademeuremedio

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def helloWorld():
    return "<a>/Funções: <br>" \
           "/lista/{termo}<br>" \
           "/denuncia/{cod_posto}/{ean_medicamento}<br>" \
           "/score/{cod_posto}/{ean_medicamento}<br>" \
           "/ranking/{qtde}<br></a>"


@app.route('/lista/<termo>')
# @app.doc(params={'termo': 'nome do remédio para buscar'})
@cross_origin()
def lista(termo):
    return funcoes_cademeuremedio.lista_medicamentos_sus(termo).to_json(orient='records')
    #return "Hello lista!"


@app.route('/denuncia/<cod_posto>/<cod_medicamento>')
@cross_origin()
def denuncia(cod_posto, cod_medicamento):
    return str(funcoes_cademeuremedio.grava_falta_remedio(cod_posto, cod_medicamento))


@app.route('/denuncia_passado/<cod_posto>/<cod_medicamento>/<dias>')
@cross_origin()
def denuncia_passado(cod_posto, cod_medicamento, dias):
    return str(funcoes_cademeuremedio.grava_falta_remedio_passado(cod_posto, cod_medicamento, dias))


@app.route('/score/<cod_posto>/<cod_medicamento>')
@cross_origin()
def score(cod_posto, cod_medicamento):
    return str(funcoes_cademeuremedio.score_posto(cod_posto, cod_medicamento))
    #teste.lista_medicamentos(termo).to_json(orient='split')
    #return "Hello lista!"

@app.route('/ranking/<qtde>')
@cross_origin()
def ranking(qtde):
    return funcoes_cademeuremedio.ranking(qtde)


@app.route('/todos_remedios/<termo>')
@cross_origin()
def todos_remedios(termo):
    return funcoes_cademeuremedio.todos_remedios(termo).to_json(orient='split')


@app.route('/gera_dados/<qtde>')
@cross_origin()
def gera_dados(qtde):
    return funcoes_cademeuremedio.gera_dados(qtde)


@app.route('/estabelecimentos/latitude/<latitude>/longitude/<longitude>/raio/<raio>')
@cross_origin()
def estabelecimentos(latitude, longitude, raio):
    r = requests.get(
        'http://mobile-aceite.tcu.gov.br/mapa-da-saude/rest/estabelecimentos/latitude/' + latitude + '/longitude/' + longitude + '/raio/' + raio + '?categoria=POSTO%20DE%20SA%C3%9ADE')
    # r = requests.get('http://mobile-aceite.tcu.gov.br/mapa-da-saude/rest/estabelecimentos/latitude/-27.5926371/longitude/-48.5576378/raio/50?categoria=POSTO%20DE%20SA%C3%9ADE')
    return r.text


#http://mobile-aceite.tcu.gov.br/mapa-da-saude/rest/estabelecimentos/latitude/27/longitude/-28/raio/30


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    app.run(host='0.0.0.0', port=port, debug=True)