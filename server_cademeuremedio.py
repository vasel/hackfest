import os

from flask import Flask

import funcoes_cademeuremedio

app = Flask(__name__)

@app.route("/")
def hello():
    return "Funções: <br>" \
           "/lista/{termo}<br>" \
           "/denuncia/{cod_posto}/{ean_medicamento}<br>" \
           "/score/{cod_posto}/{ean_medicamento}<br>" \
           "/ranking/{qtde}<br> "

@app.route('/lista/<termo>')
def lista(termo):
    return funcoes_cademeuremedio.lista_medicamentos(termo).to_json(orient='split')
    #return "Hello lista!"


@app.route('/denuncia/<cod_posto>/<ean_medicamento>')
def denuncia(cod_posto,ean_medicamento):
    return str(funcoes_cademeuremedio.grava_falta_remedio(cod_posto, ean_medicamento))
    #teste.lista_medicamentos(termo).to_json(orient='split')
    #return "Hello lista!"


@app.route('/score/<cod_posto>/<ean_medicamento>')
def score(cod_posto,ean_medicamento):
    return str(funcoes_cademeuremedio.retorna_score_posto(cod_posto, ean_medicamento))
    #teste.lista_medicamentos(termo).to_json(orient='split')
    #return "Hello lista!"

@app.route('/ranking/<qtde>')
def ranking(qtde):
    return funcoes_cademeuremedio.ranking(qtde)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    app.run(host='0.0.0.0', port=port, debug=True)