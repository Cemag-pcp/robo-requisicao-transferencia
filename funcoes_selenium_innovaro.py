from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import logging


def navegador():
    
    # link1 = "http://192.168.3.141/"
    link1 = "http://devcemag.innovaro.com.br:81/sistema"
    # link1 = "http://127.0.0.1/sistema"
    nav = webdriver.Chrome('chromedriver.exe')
    nav.get(link1)

    return nav


def iframes(nav):

    """
    Função para entrar até a última camada de iframes existente
    :nav: webdriver
    """

    iframe_list = nav.find_elements(By.CLASS_NAME, 'tab-frame')

    for iframe in range(len(iframe_list)):
        try:
            nav.switch_to.default_content()
            nav.switch_to.frame(iframe_list[iframe])
            print(iframe)
        except:
            pass


def saindo_iframe(nav):

    """
    Função para sair dos iframes
    """

    nav.switch_to.default_content()


def fechar_abas(nav):

    """
    Função para fechar abas em aberto
    :nav: webdriver
    """
    
    wait = 20

    nav.switch_to.default_content()

    # Encontrar o contêiner das abas
    container_abas = nav.find_element(By.ID, 'tabs')

    # Encontrar todas as abas dentro do contêiner
    abas = container_abas.find_elements(By.XPATH, './/span[@class="process-tab-label"]')

    # Imprimir o número de abas abertas
    qt_abas_aberta = len(abas)

    count_abas = 0

    while count_abas < qt_abas_aberta:

        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'process-tab-right-active'))).click()
        time.sleep(2)    
        count_abas=+1
        time.sleep(1)
        
        abas = container_abas.find_elements(By.XPATH, './/span[@class="process-tab-label"]')
        qt_abas_aberta = len(abas)



def login(nav, login, senha):
    
    """
    Função para logar no innovaro.
    :nav: webdriver
    :login: login do innovaro
    :senha: senha innovaro
    """
        
    #logando 
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(login)
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(senha)

    time.sleep(2)

    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(Keys.ENTER)

    time.sleep(2)


def menu_innovaro(nav):
    
    """
    Função para abrir ou fechar menu no innovaro.
    :nav: webdriver
    """
    
    #abrindo menu

    try:
        nav.switch_to.default_content()
    except:
        pass

    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bt_1892603865"]/table/tbody/tr/td[2]'))).click()

    time.sleep(2)


def navegando_dentro_do_menu(nav, camada1):

    """
    Escolher o nome da opção para clicar dentro do menu
    """

    WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@title="/Menu/{camada1}"]'))).click()


def navegando_segunda_camada(nav, camada1, camada2):

    """
    Navegar dentro da segunda camada do menu exemplo: Estoque/Requisição
    """

    WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@title="/Menu/{camada1}/{camada2}"]'))).click()


def navegando_terceira_camada(nav, camada3):

    """
    Navegar dentro da terceira camada do menu exemplo: Transferência de simples de recursos
    """

    WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='webguiTreeNodeLabel' and normalize-space()='{camada3}']"))).click()


def buscando_depositos_origem(recurso):

    df = pd.read_csv('lista_pesos.csv')

    df['codigo_peca'] = df['nome_peca'].apply(lambda x: x.split()[0])

    nome_deposito = pd.DataFrame()

    nome_deposito['nome_mp'] = df['Nome'].apply(lambda x: x.split()[0]).drop_duplicates()

    nome_deposito['deposito'] = nome_deposito['nome_mp'].apply(lambda x: 'Corte e estamparia' if x in ['BOBINA', 'CHAPA'] else 'Usinagem')

    peso_mp = float(df[df['codigo_peca'] == recurso][['Qtd.']].values.tolist()[0][0])
    codigo_mp = df[df['codigo_peca'] == recurso][['Código']].values.tolist()[0][0]
    mp = df[df['codigo_peca'] == recurso][['Código']].values.tolist()[0][0].split()[0]
    nome_mp = df[df['codigo_peca'] == recurso][['Nome']].values.tolist()[0][0].split()[0]
    nome_deposito_string = nome_deposito[nome_deposito['nome_mp'] == nome_mp][['deposito']].values.tolist()[0][0]

    return nome_deposito_string,peso_mp,codigo_mp


def transformando_linha_1(nav,parametros):

    # parametros = {'deposito':'carpintaria','recurso':'453407','etapa':'169543','quantidade':'-53'}

    deposito = parametros['deposito'] 
    recurso = parametros['recurso'] 
    etapa =  parametros['etapa'] 
    quantidade =  parametros['quantidade'] 

    quantidade = quantidade * -1

    time.sleep(3)

    saindo_iframe(nav)
    iframes(nav)    

    wait = 20

    time.sleep(1)
    #Clicando em insert
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/thead/tr[1]/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div'))).click()
    
    time.sleep(1)
    #Classe
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[3]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Data Movimentação
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[5]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Hora
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[6]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Depósito
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[7]/div/input'))).send_keys(deposito)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[7]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Recurso
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[9]/div/input'))).send_keys(recurso)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[9]/div/input'))).send_keys(Keys.TAB)

    time.sleep(3)
    #Desmontagem
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[11]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Lote
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[12]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Lote Vinculador
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[14]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Etapa
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[16]/div/input'))).send_keys(etapa)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[16]/div/input'))).send_keys(Keys.TAB)
    
    saindo_iframe(nav)
    
    etapaInput = ''

    try:
        etapaInput = WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="errorMessageBox"]/div[2]/table/tbody/tr[1]/td[2]/div/div'))).text
    except:
        pass

    if etapaInput != '':
        
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[2]/table/tbody/tr[2]/td/div/button'))).click()

        return etapaInput

    iframes(nav)

    time.sleep(1)
    #Pessoa   
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[18]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Tipo de documento
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[20]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Número de documento
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[22]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Quantidade
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[23]/div/input'))).send_keys(quantidade)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[23]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Custo Mat
    custo_mat = float(WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[24]/div/input'))).get_attribute("value"))
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]/td[24]/div/input'))).send_keys(Keys.INSERT)

    return custo_mat


def transformando_linha_2(nav,parametros,custo_mat):
    
    #iframes(nav)

    recurso = parametros['recurso']

    try:
        nome_deposito,peso_mp,codigo_mp= buscando_depositos_origem(recurso)
    except:
        return 'Não está na lista de peso'
    
    quantidade = parametros['quantidade']
    peso_total = abs(float(quantidade)*peso_mp)
    
    time.sleep(3)   
    
    wait = 20

    time.sleep(1)
    #Classe
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[3]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Data Movimentação
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[5]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Hora
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[6]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Depósito
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[7]/div/input'))).send_keys(nome_deposito)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[7]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Recurso
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[9]/div/input'))).send_keys(codigo_mp)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[9]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Desmontagem
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[11]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Lote
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[12]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Lote Vinculador
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[14]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Etapa
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[16]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Pessoa
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[18]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Tipo de documento
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[20]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #número de documento
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[22]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Quantidade
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[23]/div/input'))).send_keys(Keys.CONTROL + 'A')
    time.sleep(2)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[23]/div/input'))).send_keys(Keys.DELETE)
    time.sleep(2)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[23]/div/input'))).send_keys(abs(peso_total))
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[23]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Custo Mat
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[24]/div/input'))).send_keys(Keys.CONTROL + 'A')
    time.sleep(2)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[24]/div/input'))).send_keys(Keys.DELETE)
    time.sleep(2)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[24]/div/input'))).send_keys(abs(custo_mat))
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[24]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Custo MOD
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[25]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Custo GGF
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[26]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Custo contábil
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[27]/div/input'))).send_keys(Keys.CONTROL + 'A')
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[27]/div/input'))).send_keys(Keys.DELETE) 
    time.sleep(2)   
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[27]/div/input'))).send_keys(abs(custo_mat))
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[27]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #Unimov
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[28]/div/input'))).send_keys(Keys.INSERT)

    time.sleep(1)
    #Classe
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="2"]/td[3]/div/input'))).send_keys(Keys.ESCAPE)
    
    saindo_iframe(nav)

    time.sleep(1)
    #Sim
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="answers_0"]'))).click()

    time.sleep(2)

    # Esperar até que a classe do botão seja "hover" (ou outro estado desejado)
    botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span[2]')))
    botao.click()
    WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))

    # Agora, o botão está no estado "hover" e você pode clicar nele
    botao.click()

    time.sleep(3)

    #Sim
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/table/tbody/tr/td[2]/div/div[2]'))).click()

    time.sleep(2)

    erro = ''
    
    try:

        time.sleep(1)
        erro_element = WebDriverWait(nav, wait).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[2]/table/tbody/tr[1]/td[2]/div/div/span[1]'))
        )

        # Se o elemento for um campo de entrada, use .get_attribute("value")
        # Se for um elemento de texto (por exemplo, <span>), use .text
        erro = erro_element.get_attribute("value") if erro_element.tag_name == 'input' else erro_element.text

        WebDriverWait(nav, wait).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm"]'))
        ).click()
        

    except:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm"]'))).click()

    
    return erro


def transferindo(nav,parametros):

    funcionario = parametros['funcionario'] 
    deposito_destino =  parametros['deposito_origem'] 
    recurso = parametros['recurso']
    quantidade = parametros['quantidade']
    data = parametros['data']

    iframes(nav)
    
    wait = 20

    c=3

    #Insert
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[1]/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div'))).click()
    logging.info("Insert")

    #Classe
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[4]/div/input'))).send_keys(Keys.TAB)
    logging.info("Classe")

    #Solicitante
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[6]/div/input'))).click()
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[6]/div/input'))).send_keys(Keys.CONTROL + 'A')
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[6]/div/input'))).send_keys(Keys.DELETE)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[6]/div/input'))).send_keys('ti.cemag')
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[6]/div/input'))).send_keys(Keys.TAB)
    logging.info("Solicitante")

    #Deposito de origem
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[8]/div/input'))).send_keys('central')
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[8]/div/input'))).send_keys(Keys.TAB)
    time.sleep(1)
    logging.info("Depósito de origem")

    #Deposito de destino
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[10]/div/input'))).send_keys(deposito_destino)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[10]/div/input'))).send_keys(Keys.TAB)
    time.sleep(1)
    logging.info("Depósito de destino")

    #Recurso
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[12]/div/input'))).send_keys(recurso)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[12]/div/input'))).send_keys(Keys.TAB)
    time.sleep(1)
    logging.info("Recurso")

    #Lote
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[14]/div/input'))).send_keys(Keys.TAB)
    logging.info("Lote")

    #Campo vazio
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[16]/div/input'))).send_keys(Keys.TAB)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[17]/div/input'))).send_keys(Keys.TAB)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[19]/div/input'))).send_keys(Keys.TAB)
    logging.info("Campo vazio")

    #Quantidade
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[21]/div/input'))).send_keys(quantidade)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[' + str(c) + ']/td[21]/div/input'))).send_keys(Keys.TAB)
    logging.info("Quantidade")

    time.sleep(2)
    
    #Insert
    iframes(nav)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[22]/div/input'))).send_keys(Keys.INSERT)
    logging.info("Insert")

    #Classe
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[5]/td[4]/div/input'))).send_keys(Keys.ESCAPE)
    time.sleep(1)
    logging.info("Classe")

    #Sim
    saindo_iframe(nav)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/table/tbody/tr/td[2]/div/div[2]'))).click()
    time.sleep(1)
    logging.info("Sim")

    #Selecionando
    iframes(nav)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[1]/input'))).click()
    logging.info("Selecionando caixa")

    #Aprovar
    botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[2]/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/span[2]')))
    botao.click()
    time.sleep(1.5)
    logging.info("Botão de aprovar")

    try:
        WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
        botao.click()
        logging.info("Botão de aprovar")
    except:
        pass
    
    time.sleep(1.5)

    #Confirmando a aprovação
    saindo_iframe(nav)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[2]/table/tbody/tr[2]/td/div/button'))).click()
    time.sleep(1)
    logging.info("Confirmando aprovação")

    #Baixar
    iframes(nav)
    botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[2]/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td[3]/span[2]')))
    botao.click()
    time.sleep(1.5)
    logging.info("Botão de baixar")

    try:
        WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
        botao.click()
        logging.info("Botão de baixar")

    except:
        pass
    
    time.sleep(1.5)

    #Movimentação
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input'))).click()
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.CONTROL + 'A')
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.DELETE)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input'))).send_keys(data)
    time.sleep(2)
    logging.info("Movimentação")

    #Confirmar baixa
    # time.sleep(2)
    # botao = WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td/span[2]')))
    # time.sleep(1)
    # botao.click()
    # time.sleep(1.5)

    # try:
    #     WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
    #     botao.click()
    # except:
    #     pass

    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.ENTER)

    time.sleep(1.5)

    #Verificar se deu erro
    saindo_iframe(nav)
    erro = ''
    try:
        erro = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[2]/table/tbody/tr[1]/td[2]/div/div/span[1]'))).text
        time.sleep(0.5)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div[2]/table/tbody/tr[2]/td/div/button'))).click()
        logging.info(f"Erro: {erro}")
        return erro
    except:
        pass

    #Gravar
    time.sleep(2)
    saindo_iframe(nav)
    botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span[2]')))
    botao.click()
    time.sleep(1.5)
    logging.info("Botão de gravar")

    try:
        WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
        botao.click()
        logging.info("Botão de gravar")

    except:
        pass
    
    return erro


def requisitando(nav,parametros):

    # parametros = {'deposito':'carpintaria','recurso':'453407','etapa':'169543','quantidade':'-53'}
    # c = 0
    
    c = 0

    funcionario = parametros['funcionario'] 
    ccusto =  parametros['ccusto'] 
    item = parametros['item']
    data = parametros['data']
    quantidade = parametros['quantidade']
    observacao = parametros['observacao']
    classe = parametros['classe']

    time.sleep(3)

    saindo_iframe(nav)
    iframes(nav)    

    wait = 20

    time.sleep(1)

    if c == 0:
    #Clicando em insert
        WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/thead/tr[1]/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div'))).click()

    time.sleep(1)
    #Classe
    if c != 0:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).send_keys(Keys.TAB)
    else:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).click()
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).send_keys(Keys.CONTROL + 'A')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).send_keys(Keys.DELETE)
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).send_keys(classe)
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[3]/div/input'))).send_keys(Keys.TAB)

    time.sleep(2)
    #Requisitante
    if c != 0:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).send_keys(Keys.TAB)
    else:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).click()
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).send_keys(Keys.CONTROL + 'A')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).send_keys(Keys.DELETE)
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).send_keys('Ti.Cemag')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[5]/div/input'))).send_keys(Keys.TAB)

    time.sleep(1)
    #C Custos
    if c != 0:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).send_keys(Keys.TAB)
    else:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).click()
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).send_keys(Keys.CONTROL + 'A')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).send_keys(Keys.DELETE)
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).send_keys(ccusto)
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[7]/div/input'))).send_keys(Keys.TAB)
    
    time.sleep(1)
    #Recurso
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[9]/div/input'))).send_keys(item)
    time.sleep(0.5)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[9]/div/input'))).send_keys(Keys.TAB)
    logging.info("Recurso")

    time.sleep(2)
    #Quantidade
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[12]/div/input'))).send_keys(quantidade)
    time.sleep(1)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[12]/div/input'))).send_keys(Keys.TAB)
    logging.info("Quantidade")

    time.sleep(1)
    #Observação
    if c != 0:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).send_keys(Keys.TAB)
    else:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).click()
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).send_keys(Keys.CONTROL + 'A')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).send_keys(Keys.DELETE)
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).send_keys(observacao)
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[13]/div/textarea'))).send_keys(Keys.TAB)
    
    
    #Emissão
    if c != 0:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).send_keys(Keys.TAB)
    else:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).click()
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).send_keys(Keys.CONTROL + 'A')
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).send_keys(Keys.DELETE)
        time.sleep(1)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).send_keys(data)
        time.sleep(2)
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[14]/div/input'))).send_keys(Keys.TAB)

    
    #Insert(CONTROL + M)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[15]/div/input'))).send_keys(Keys.INSERT)
    time.sleep(1.5)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1"]/td[3]/div/input'))).send_keys(Keys.ESCAPE)
    time.sleep(1.5)
    saindo_iframe(nav)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="answers_0"]'))).click()
    logging.info("Insert")

    # else:
    #     #Insert
    #     WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{c}"]/td[15]/div/input'))).send_keys(Keys.INSERT) 

    #selecionando caixa
    iframes(nav) 
    time.sleep(1.5)
    WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[4]/td[1]/input'))).click()
    logging.info("Selecionando caixa")

    time.sleep(1)
    #APROVAR
    # # Esperar até que a classe do botão seja "hover" (ou outro estado desejado)
    # botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[2]/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/span[2]')))
    # time.sleep(0.5)
    # botao.click()
    # time.sleep(0.5)
    # WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
    # time.sleep(0.5)
    # # Agora, o botão está no estado "hover" e você pode clicar nele

    # time.sleep(0.5)
    # saindo_iframe(nav)
    # time.sleep(3)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm"]'))).click()

    # time.sleep(1)
    # iframes(nav) 
    # time.sleep(1)
    # #Baixar
    # # Esperar até que a classe do botão seja "hover" (ou outro estado desejado)
    # botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[2]/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td[3]/span[2]')))
    # time.sleep(0.5)
    # botao.click()
    # # WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
    # time.sleep(3)

    # # Agora, o botão está no estado "hover" e você pode clicar nele
    # # botao.click()   
    # # Classe Mov. deposito
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input'))).click()
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.CONTROL + 'A')
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.DELETE)
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input'))).send_keys('Movimentação de depósitos')
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.TAB)

    # try:
    #     time.sleep(1)
    #     WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[1]/input'))).click()

    #     #ok
    #     botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/table/thead/tr[2]/td[1]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/span[2]')))
    #     time.sleep(0.5)
    #     botao.click()
    # except:
    #     pass

    # #Deposito
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'))).click()
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.CONTROL + 'A')
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.DELETE)
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'))).send_keys('central')
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grdinfoBaixa"]/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.TAB)

    # #Movimentação
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input'))).click()
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.CONTROL + 'A')
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.DELETE)
    # time.sleep(1)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(data)
    # time.sleep(2)
    # WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input'))).send_keys(Keys.TAB)

    saindo_iframe(nav)
    # time.sleep(1.5)
    # #Continuar
    # # Esperar até que a classe do botão seja "hover" (ou outro estado desejado)
    # botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/span[2]')))
    # botao.click()
    # WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))

    # # Agora, o botão está no estado "hover" e você pode clicar nele
    # botao.click()

    # time.sleep(15)
    #Gravar
    # Esperar até que a classe do botão seja "hover" (ou outro estado desejado)
    botao = WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/span[2]')))
    botao.click()
    WebDriverWait(nav, wait).until(lambda nav: "hover" in botao.get_attribute("class"))
    logging.info("Botão de gravar")

    # Agora, o botão está no estado "hover" e você pode clicar nele
    botao.click()

    time.sleep(1.5)
    
    erro = ''

    try:
        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="answers_0"]'))).click()

        time.sleep(3)

        WebDriverWait(nav, wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm"]'))).click()
        logging.info("Item requisitado!")

    except:
        erro = 'Erro'
        logging.info(f"Erro na requisição {erro}")
    
    return erro

'alguma coisa'