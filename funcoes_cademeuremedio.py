# import os
import datetime

import pandas as pd
import unidecode


def normaliza(termo):
    return (
        unidecode.unidecode(termo.upper()).replace(",", "").replace('.', '').replace(';', '').replace('"', '').replace(
            '"', ''))  # .strip()

#metodo de entrada
def lista_medicamentos_sus(termo):
    termo = normaliza(termo)
    dfl = dfListaRename[
        dfListaRename["remedio"].str.contains(termo)]  # dfm[dfm['PRINCIPIO ATIVO'].str.contains(termo)]
    # dfl = retira_nao_tem_no_sus(dfl)
    if (dfl.empty):
        # encontra por nome comercial
        # principios = busca_principio_por_nome_comercial(termo)
        # for principio in principios:
        #     result = dfListaRename["PRINCIPIO"].str.contains(principio[0])
        #     if not result.empty:
        #         dfl = pd.concat(dfl,result)
        if not dfl.empty:
            return dfl
    else:
        return dfl[['id', 'remedio']].head(10)

    return pd.DataFrame({"ERROR": termo + ' não encontrado.'}, index=[0])


def busca_principio_por_nome_comercial(termo):
    dfl = dfListaProdutos[dfListaProdutos['PRODUTO'].str.contains(termo)]
    return dfl['PRINCIPIO ATIVO']


def todos_remedios(termo):
    termo = normaliza(termo)
    dfl = dfListaProdutos[dfListaProdutos['PRINCIPIO ATIVO'].str.contains(termo)]
    if (dfl.empty):
        dfl = dfListaProdutos[dfListaProdutos['PRODUTO'].str.contains(termo)]
    return dfl.head(100)

def lista_por_nome_comercial(termo):
    termo = normaliza(termo)
    dfl = dfListaProdutos[dfListaProdutos['PRODUTO'].str.contains(termo)]
    if (dfl.empty):
        return pd.DataFrame(['0', termo + ' não encontrado', ''])
    dfl = retira_nao_tem_no_sus(dfl)
    if (dfl.empty):
        return pd.DataFrame(['0', termo + ' não disponivel no SUS', ''])
    else:
        return dfl.head(10)

def retira_nao_tem_no_sus(lista):
    for row in lista.iterrows():
        if not tem_no_sus(str(row[0])):
            print(str(row[0]))
            lista = lista.drop(row[0])
            #print('nao tem')
    return lista


def tem_no_sus(remedio):
    remedio = normaliza(remedio).split('0')[0]
    return not dfListaRename[dfListaRename["PRINCIPIO"].str.contains(remedio)].empty

def grava_falta_remedio (posto,remedio):
    try:
        denuncias[(posto, remedio)].insert(-1, datetime.datetime.now())
    except:
        denuncias[(posto, remedio)] = [datetime.datetime.now()]
    return len(denuncias[(posto, remedio)])


def retorna_score_posto (posto,remedio):
    try:
        score = 0
        # base para o decaimento exponencial: score += base ** (dataAtual - dataDenuncia[i])
        # ex.: dias  = 7    (uma semana)
        #      fator = 1/10
        # ou seja, o score de uma denúncia hoje, equivale ao de 10 denúncias há 7 dias
        fator = 1 / 10
        dias = 7
        BASE = fator ** (1 / dias)

        qtde_denuncias = len(denuncias[(posto, remedio)])
        for denuncia in denuncias[(posto, remedio)]:
            dias = (datetime.datetime.now() - denuncia).days
            # print (dias)
            if dias <= 30:
                score += BASE ** dias
        return score
    except:
        return 0

def ranking(qtde):
    return str(denuncias)


#port = int(os.environ.get("PORT", 7777))
# if (port == 7777):
df = pd.read_json('listaISO.json')  # , encoding='UTF8')

# else:
#    df = pd.read_json('https://raw.githubusercontent.com/vasel/hackfest/master/listaUTF8.json')  # , orient='records')  # ) #, lines=True)


dfListaProdutos = df[["PRINCIPIO ATIVO", "PRODUTO", "APRESENTACAO"]]

dfListaRename = pd.read_csv('listaRENAME.csv', names=["PRINCIPIO ATIVO", "COMPOSICAO", "COMPONENTE"])

dfListaRename['PRINCIPIO'] = dfListaRename["PRINCIPIO ATIVO"].apply(normaliza)
dfListaRename['remedio'] = dfListaRename['PRINCIPIO'] + dfListaRename["COMPOSICAO"].apply(normaliza) + dfListaRename[
    "COMPONENTE"].apply(normaliza)



dfListaRename['id'] = dfListaRename.index
dfListaRename.rename(index=str, columns={"COMPONENTE": "APRESENTACAO", "COMPOSICAO": "PRODUTO"})


denuncias=dict()
# print (lista_medicamentos('tylenol'))
#print(lista_medicamentos('CITRATO'))


