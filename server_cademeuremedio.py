import os

from flask import Flask
from flask_cors import CORS, cross_origin

import funcoes_cademeuremedio

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def helloWorld():
    return "Funções: <br>" \
           "/lista/{termo}<br>" \
           "/denuncia/{cod_posto}/{ean_medicamento}<br>" \
           "/score/{cod_posto}/{ean_medicamento}<br>" \
           "/ranking/{qtde}<br> "


@app.route('/lista/<termo>')
@cross_origin()
def lista(termo):
    return funcoes_cademeuremedio.lista_medicamentos_sus(termo).to_json(orient='records')
    # return "Hello lista!"


@app.route('/denuncia/<cod_posto>/<cod_medicamento>')
@cross_origin()
def denuncia(cod_posto, cod_medicamento):
    return str(funcoes_cademeuremedio.grava_falta_remedio(cod_posto, cod_medicamento))
    # teste.lista_medicamentos(termo).to_json(orient='split')


@app.route('/denuncia_municipio/<cod_posto>/<cod_medicamento>/<municipio>')
@cross_origin()
def denuncia_municipio(cod_posto, cod_medicamento, municipio):
    return str(funcoes_cademeuremedio.grava_falta_remedio_municipio(cod_posto, cod_medicamento, municipio))
    # teste.lista_medicamentos(termo).to_json(orient='split')


@app.route('/estabelecimentos/latitude/<latitude>/longitude/<longitude>/raio/<raio>')
@cross_origin()
def estabelecimentos(latitude, longitude, raio):
    return str(funcoes_cademeuremedio.retorna_estabelecimentosf(latitude, longitude, raio))
    # teste.lista_medicamentos(termo).to_json(orient='split')
    # return "Hello lista!"


@app.route('/denuncia_uf/<uf>/')
@cross_origin()
def denuncias_uf(uf):
    return str(funcoes_cademeuremedio.retorna_denuncias_uf(uf))
    # teste.lista_medicamentos(termo).to_json(orient='split')
    # return "Hello lista!"


# @app.route('/score/<cod_posto>/<ean_medicamento>')
# @cross_origin()
# def score(cod_posto,ean_medicamento):
#     return str(funcoes_cademeuremedio.retorna_score_posto(cod_posto, ean_medicamento))
#     #teste.lista_medicamentos(termo).to_json(orient='split')
#     #return "Hello lista!"


@app.route('/score/<cod_posto>/<ean_medicamento>/<municipio>')
@cross_origin()
def score(cod_posto, ean_medicamento, municipio):
    return str(funcoes_cademeuremedio.score_posto(cod_posto, ean_medicamento, municipio))
    # teste.lista_medicamentos(termo).to_json(orient='split')
    #return "Hello lista!"

@app.route('/ranking/<qtde>')
@cross_origin()
def ranking(qtde):
    return funcoes_cademeuremedio.ranking(qtde)


@app.route('/todos_remedios/<termo>')
@cross_origin()
def todos_remedios(termo):
    return funcoes_cademeuremedio.todos_remedios(termo).to_json(orient='split')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    app.run(host='0.0.0.0', port=port, debug=True)
