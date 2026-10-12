import logging
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
             use_monitor=False) 
def timer_trigger_tipo1(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('O temporizador está atrasado!')

    logging.info('Função de temporizador executada.')

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
             use_monitor=False) 
def timer_trigger_tipo2(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('O temporizador está atrasado!')

    logging.info('Função de temporizador executada.')


@app.route(route="http_trigger", auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    lastname = req.params.get('lastname')
    
    if name and lastname:
        return func.HttpResponse(f"Eai, {name} {lastname}. você conseguiu!!")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
                   use_monitor=True)
def timer_trigger_chamado(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('O temporizador de chamados está atrasado!')

    database = os.getenv("DATABASE")
    host = os.getenv("HOST")
    password = os.getenv("PASSWORD")
    user = os.getenv("USER")

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host};DATABASE={database};"
        f"UID={user};PWD={password};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )

    connection = None
    try:
        connection = pyodbc.connect(connection_string, timeout=30)
        cursor = connection.cursor()

        def consultar_dados(tabela):
            cursor.execute(f"SELECT TOP (3) * FROM [itsm].[{tabela}]")
            colunas = [coluna[0] for coluna in cursor.description]
            dados = cursor.fetchall()
            
            logging.info('CONSULTANDO DADOS DA TABELA: %s', tabela)
            logging.info('Consulta retornou %s dados(s).', len(dados))
            for dado in dados:
                logging.info('%s: %s', tabela, dict(zip(colunas, dado)))

        # SELECT DA TABELA CHAMADO
        consultar_dados("chamado") 
        logging.info("-")

        # SELECT DA TABELA ANALISTA
        consultar_dados("analista") 
        logging.info("-")

        # SELECT DA TABELA CATEGORIA
        consultar_dados("categoria") 
        logging.info("-")

        # SELECT DA TABELA CHAMADO_SLA
        consultar_dados("chamado_sla")
        logging.info("-")

        # SELECT DA TABELA chamado_status_historico
        consultar_dados("chamado_status_historico")
        logging.info("-")

        # SELECT DA TABELA cliente_organizacao
        consultar_dados("cliente_organizacao")
        logging.info("-")

        # SELECT DA TABELA csat_avaliacao
        consultar_dados("csat_avaliacao")
        logging.info("-")

        # SELECT DA TABELA fila
        consultar_dados("fila")
        logging.info("-")
        
        # SELECT DA TABELA sla
        consultar_dados("sla")
        logging.info("-")

        # SELECT DA TABELA solicitante
        consultar_dados("solicitante")
        logging.info("-")

    except Exception:
        logging.exception('Erro ao consultar os chamados.')
        raise
    finally:
        if connection is not None:
            connection.close()