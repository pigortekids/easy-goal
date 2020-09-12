import os
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import json

# cria uma chamada padrao de API
def api_request( host, end_point, request_type, headers, body=None, correct_response=None, error_response='Error' ):
    retur = False
    url = host + end_point

    response = None
    if request_type == 'GET':
        response = requests.get( url=url, data=body, headers=headers )
    elif request_type == 'POST':
        response = requests.post( url=url, data=body, headers=headers )
    
    status_code = response.status_code
    output = None
    try:
        output = response.json()
    except ValueError:
        output = response.text
    
    if status_code == 200:
        """
        if correct_response != None:
            print( '{0} -> {1}'.format( datetime.now(), correct_response ) )
        if output != None and output != '':
            print( '{0} -> {1}'.format( datetime.now(), output ) )
        """
        retur = True
    else:
        print( '{0} -> {1} {2}'.format( datetime.now(), error_response, status_code ) )
        print( '{0} -> Erro com descricao "{1}"'.format( datetime.now(), output ) )
    
    return retur, output

def use_api( accountId, tipo_chamada_api, infos=None ):
    # pega diretorio do script
    script_folder = os.path.dirname(os.path.realpath(__file__)) + '\\'

    # leitura do arquivo com token e data de expiracao
    with open( script_folder + 'token.txt', 'r' ) as f:
        auth_token = f.readline().replace('\n', '')
        horario_exp_str = f.readline()

    # transforma a data em string para datetime
    horario_exp = datetime.strptime(horario_exp_str, '%Y-%m-%d %H:%M:%S.%f')

    # caso o token expirou, renova o token
    if horario_exp <= datetime.now():
        auth = HTTPBasicAuth('e33b611a81204f318a15d5728b998661', '31591ad2-1cbd-44e9-a01c-1bbcc0985544')
        url = 'https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token'
        body = 'grant_type=client_credentials&scope=urn:opc:resource:consumer::all'
        headers = {'Content-Type':'application/x-www-form-urlencoded'}

        response = requests.post( url=url, auth=auth, data=body, headers=headers )

        if response.status_code == 200:
            auth_token = response.json()['access_token']
            expiracao = response.json()['expires_in']
            with open( script_folder + 'token.txt', 'w' ) as f:
                f.write( auth_token + '\n' )
                f.write( str(datetime.now() + timedelta( seconds=expiracao )) )
            #print( '{0} -> Token atualizado'.format( datetime.now() ) )
        else:
            print( '{0} -> Erro com codigo {1}'.format( datetime.now(), response.status_code ) )
            print( '{0} -> Erro com descricao "{1}"'.format( datetime.now(), response.json() ) )

    # variaveis
    host = 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/'
    headers = {'Authorization': 'Bearer ' + auth_token}

    #confere se a API esta funcionando
    end_point = 'health'
    working = api_request( host=host, end_point=end_point, request_type='GET', headers=headers, error_response='API fora do ar' )[0]
    if working:

        # conta
        if tipo_chamada_api == 'conta':
            end_point = 'open-banking/v1/accounts/{0}'.format( accountId )
            response = api_request( host=host, end_point=end_point, request_type='GET', headers=headers, correct_response='CONTA' )
            return response[1]['Data']['Account'][0]

        # saldo
        if tipo_chamada_api == 'saldo':
            end_point = 'open-banking/v1/accounts/{0}/balances'.format( accountId )
            response = api_request( host=host, end_point=end_point, request_type='GET', headers=headers, correct_response='SALDO' )
            return response[1]['Data']['Balance'][0]['Amount']['Amount']

        # extrato
        if tipo_chamada_api == 'extrato':
            end_point = 'open-banking/v1/accounts/{0}/transactions'.format( accountId )
            response = api_request( host=host, end_point=end_point, request_type='GET', headers=headers, correct_response='EXTRATO' )
            return response[1]['data']['transaction']

        # transferencia
        if tipo_chamada_api == 'trans':
            end_point = 'accounts/v1/accounts/{0}/transfers'.format( accountId )
            api_request( host=host, end_point=end_point, request_type='GET', headers=headers, correct_response='TRANSFERENCIA' )

        # opt in (erro 415)
        if tipo_chamada_api == 'opt_in':
            end_point = 'accounts/v1/optin'
            response = api_request( host=host, end_point=end_point, request_type='POST', headers=headers, body=infos, correct_response='TRANSFERENCIA' )
            return response

        # morning calls
        if tipo_chamada_api == 'calls':
            filtro = 'fromData=2020-07-09&2020-07-14&playlist=morningCalls&channel=safra'
            end_point = '/media/v1/youtube?{0}'.format( filtro )
            api_request( host=host, end_point=end_point, request_type='GET', headers=headers, correct_response='OPT IN' )