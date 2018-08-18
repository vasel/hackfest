# import os
import datetime

import pandas as pd
import unidecode


def normaliza(termo):
    return unidecode.unidecode(termo.upper()).replace(",", "").replace('.', '')

#metodo de entrada
def lista_medicamentos(termo):
    termo = normaliza(termo)
    dfl = dfm[dfm['PRINCIPIO ATIVO'].str.contains(termo)]
    dfl = retira_nao_tem_no_sus(dfl)
    if (dfl.empty):
        return lista_por_nome_comercial(termo)
    else:
        return dfl.head(5)

def lista_por_nome_comercial(termo):
    dfl = dfm[dfm['PRODUTO'].str.contains(termo)]
    dfl = retira_nao_tem_no_sus(dfl)
    if (dfl.empty):
        return pd.DataFrame(['0', 'Remédio não encontrado ou não disponivel', ''])
    else:
        return dfl.head(5)

def retira_nao_tem_no_sus(lista):
    for row in lista.iterrows():
        #print  (row[0])
        if not tem_no_sus(str(row[0])):
            lista = lista.drop(row[0])
            #print('nao tem')
    return lista


def tem_no_sus(remedio):
    return True  # False #True

def grava_falta_remedio (posto,remedio):
    try:
        denuncias[(posto, remedio)].insert(-1, datetime.datetime.now())
    except:
        denuncias[(posto, remedio)] = [datetime.datetime.now()]
    return len(denuncias[(posto, remedio)])


def retorna_score_posto (posto,remedio):
    try:
        return len(denuncias[(posto, remedio)])
    except:
        return 0

def ranking(qtde):
    return denuncias


#port = int(os.environ.get("PORT", 7777))
# if (port == 7777):
df = pd.read_json('listaISO.json')  # , encoding='UTF8')

# else:
#    df = pd.read_json('https://raw.githubusercontent.com/vasel/hackfest/master/listaUTF8.json')  # , orient='records')  # ) #, lines=True)


dfm = df[["PRINCIPIO ATIVO", "PRODUTO", "APRESENTACAO"]]
denuncias=dict()
# print (lista_medicamentos('tylenol'))
#print(lista_medicamentos('CITRATO'))


