from funcoes_selenium_innovaro import *
import pandas as pd
import gspread
import numpy as np
import psycopg2.extras
import psycopg2  # pip install psycopg2
import datetime
from datetime import datetime, timedelta
import logging
import time

logging.basicConfig(level=logging.INFO, filename="programa.log", format="%(asctime)s - %(levelname)s - %(message)s")

DB_HOST = "database-2.cdcogkfzajf0.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "15512332"

def dados_requisicao():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = pd.read_sql_query("SELECT * FROM requisicao.requisicoes WHERE resposta_rpa ISNULL", conn)

    data['data_requisicao'] = data['data_requisicao'] - timedelta(hours=3)
    data['observacao'] = data['observacao'].fillna('')

    return data

def dados_transformar():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = pd.read_sql_query("SELECT * FROM transferencia.transferencias WHERE resposta_rpa ISNULL", conn)

    data['data_hora'] = data['data_hora'] - timedelta(hours=3)

    return data

def listar(nav, classe):
    
    lista_menu = nav.find_elements(By.CLASS_NAME, classe)
    
    elementos_menu = []

    for x in range (len(lista_menu)):
        a = lista_menu[x].text
        elementos_menu.append(a)

    test_lista = pd.DataFrame(elementos_menu)
    test_lista = test_lista.loc[test_lista[0] != ""].reset_index()

    return(lista_menu, test_lista)

def input_base_requisicao(mensagem,chave):

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("UPDATE requisicao.requisicoes SET resposta_rpa = %s WHERE id = %s", (mensagem, int(chave)))

    conn.commit()
    cur.close()
    conn.close()

def input_base_transferencia(mensagem,chave):

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("UPDATE transferencia.transferencias SET resposta_rpa = %s WHERE id = %s", (mensagem, int(chave)))

    conn.commit()
    cur.close()
    conn.close()

while True:

    time.sleep(10)

    dados_requisitar = dados_requisicao()
    dados_transferir = dados_transformar()

    if len(dados_requisitar) > 0 or len(dados_transferir) > 0:

        try:
            nav = navegador()

            logging.info("Iniciando selenium")

            #Logando
            login(nav, "luan araujo", "luanaraujo123")
            
            #Abrindo menu
            menu_innovaro(nav)

            #Clicando em Estoque
            lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
            time.sleep(1.5)
            click_producao = test_list.loc[test_list[0] == 'Estoque'].reset_index(drop=True)['index'][0]
            
            lista_menu[click_producao].click() ##clicando em producao

            logging.info("Navegando para o Estoque")

            time.sleep(1.5)

            lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
            time.sleep(1.5)
            click_producao = test_list.loc[test_list[0] == 'Requisição'].reset_index(drop=True)['index'][0]
            
            lista_menu[click_producao].click() ##clicando em producao

            logging.info("Navegando para o Requisição")

            time.sleep(1.5)

            lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
            time.sleep(1.5)
            click_producao = test_list.loc[test_list[0] == 'Transferência'].reset_index(drop=True)['index'][0]
            
            lista_menu[click_producao].click() ##clicando em producao

            logging.info("Navegando para Transferência")

            time.sleep(1.5)

            menu_innovaro(nav)

            # lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
            # time.sleep(1.5)
            # click_producao = test_list.loc[test_list[0] == 'Requisições'].reset_index(drop=True)['index'][0]
            
            # lista_menu[click_producao].click() ##clicando em producao

            time.sleep(2)

            if len(dados_requisitar) > 0:

                logging.info("Requisitando..")

                for i in range(len(dados_requisitar)):

                    menu_innovaro(nav)

                    lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
                    time.sleep(1.5)
                    click_producao = test_list.loc[test_list[0] == 'Requisições'].reset_index(drop=True)['index'][0]
                    
                    lista_menu[click_producao].click() ##clicando em producao

                    parametros = {'funcionario':dados_requisitar['funcionario'][i].split()[0],
                                'ccusto':dados_requisitar['ccusto'][i].split('- ')[1],
                                'classe':dados_requisitar['classe'][i],
                                'item':dados_requisitar['item'][i].split()[i],
                                'quantidade':dados_requisitar['quantidade'][i],
                                'data':dados_requisitar['data_requisicao'][i].strftime("%d/%m/%Y"),
                                'observacao':dados_requisitar['observacao'][i],
                                'id': dados_requisitar['id'][i]
                                }
                    try:
                        erro = requisitando(nav,parametros)

                        if erro == '':
                            mensagem = 'Requisitado!'
                            input_base_requisicao(mensagem,parametros['id'])
                            logging.info(f"Item: {dados_requisitar['item'][i].split()[i]} requisitado na quantidade: {dados_requisitar['quantidade'][i]}")

                        else:
                            input_base_requisicao(erro,parametros['id'])
                            logging.info(f"Item: {dados_requisitar['item'][i].split()[i]} com erro na quantidade: {dados_requisitar['quantidade'][i]} + erro: {erro}")

                    except:
                        logging.error("Erro no processo de requisição")
                        continue

                    
                    time.sleep(1.5)
                    fechar_abas(nav)

                    time.sleep(1)
                
            if len(dados_transferir) > 0:

                logging.info("Transferindo..")

                for i in range(len(dados_transferir)):

                    menu_innovaro(nav)

                    lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
                    time.sleep(1.5)
                    click_producao = test_list.loc[test_list[0] == 'Solicitação de transferência entre depósitos'].reset_index(drop=True)['index'][0]
                    
                    lista_menu[click_producao].click() ##clicando em producao

                    time.sleep(3)
                    
                    parametros = {#'funcionario':dados_transferir['funcionario'][i].split()[0],
                                'funcionario':dados_transferir['funcionario'][i],  
                                'deposito_origem':dados_transferir['deposito_origem'][i],
                                'recurso':dados_transferir['recurso'][i].split()[0],
                                'quantidade':dados_transferir['quantidade'][i],
                                'data':dados_transferir['data_hora'][i].strftime("%d/%m/%Y"),
                                'id': dados_transferir['id'][i] 
                                }
                    
                    time.sleep(2)

                    erro = transferindo(nav,parametros)
                    try:
                        
                        if erro == '':
                            mensagem = 'Transferido!'
                            input_base_transferencia(mensagem,parametros['id'])
                            logging.info(f"Item: {dados_transferir['recurso'][i].split()[0]} requisitado na quantidade: {dados_transferir['quantidade'][i]}")

                        else:
                            input_base_transferencia(erro,parametros['id'])
                            logging.info(f"Item: {dados_transferir['recurso'][i].split()[0]} com erro na quantidade: {dados_transferir['quantidade'][i]} + erro: {erro}")
                    
                    except:
                        logging.error("Erro no processo de transferência")
                        continue

                    time.sleep(5)
                    
                    print('fechando abas')
                    fechar_abas(nav)
                    
                    time.sleep(1.5)

            nav.close()

        except:
            logging.error("Erro no processo de Requisição ou Tranferência")
            nav.close()

