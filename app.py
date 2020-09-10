import os
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth

pasta_script = os.path.dirname(os.path.realpath(__file__)) + '\\'

# leitura do arquivo com token e data de expiracao
with open( pasta_script + 'token.txt', 'r' ) as f:
    auth_token = f.readline().replace('\n', '')
    horario_exp_str = f.readline()

horario_exp = datetime.strptime(horario_exp_str, '%Y-%m-%d %H:%M:%S.%f')

# caso o token expirou, renova o token
if horario_exp <= datetime.now():
    auth = HTTPBasicAuth('e33b611a81204f318a15d5728b998661', '31591ad2-1cbd-44e9-a01c-1bbcc0985544')
    url = 'https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token'
    body = 'grant_type=client_credentials&scope=urn:opc:resource:consumer::all'
    headers = {'Content-Type':'application/x-www-form-urlencoded'}

    result = requests.post( url=url, auth=auth, data=body, headers=headers )

    if result.status_code == 200:
        auth_token = result.json()['access_token']
        expiracao = result.json()['expires_in']
        with open( pasta_script + 'token.txt', 'w' ) as f:
            f.write( auth_token + '\n' )
            f.write( str(datetime.now() + timedelta( seconds=expiracao )) )
        print( '{0} -> Token atualizado'.format( datetime.now() ) )
    else:
        print( '{0} -> Erro com codigo {1}'.format( datetime.now(), result.status_code ) )
        print( '{0} -> Erro com descricao "{1}"'.format( datetime.now(), result.json() ) )

# tenta dar opt in
auth_token = 'eyJ4NXQjUzI1NiI6IlNhWkUtSjdJdDBQWFRYNFlCaTBCeXk4WWhPVlJkSzlNNXgzREN3R2ZnbkEiLCJ4NXQiOiJVSWpBeHIyTWlzNk9JdTNMS2NsX3JPSHl3eXMiLCJraWQiOiJTSUdOSU5HX0tFWSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMzNiNjExYTgxMjA0ZjMxOGExNWQ1NzI4Yjk5ODY2MSIsImd0cCI6ImNjIiwidXNlci50ZW5hbnQubmFtZSI6ImlkY3MtOTAyYTk0NGZmNjg1NGM1ZmJlOTQ3NTBlNDhkNjZiZTUiLCJzdWJfbWFwcGluZ2F0dHIiOiJ1c2VyTmFtZSIsInByaW1UZW5hbnQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9pZGVudGl0eS5vcmFjbGVjbG91ZC5jb21cLyIsInRva190eXBlIjoiQVQiLCJjbGllbnRfaWQiOiJlMzNiNjExYTgxMjA0ZjMxOGExNWQ1NzI4Yjk5ODY2MSIsImNhX2d1aWQiOiJjYWNjdC1iOThlNGJjZDQ1MDU0YjZlOTc3NzU5OThiNmYzNmYwNiIsImF1ZCI6InVybjpvcGM6cmVzb3VyY2U6c2NvcGU6YWNjb3VudCIsInN1Yl90eXBlIjoiY2xpZW50Iiwic2NvcGUiOiJ1cm46b3BjOnJlc291cmNlOmNvbnN1bWVyOjphbGwiLCJjbGllbnRfdGVuYW50bmFtZSI6ImlkY3MtOTAyYTk0NGZmNjg1NGM1ZmJlOTQ3NTBlNDhkNjZiZTUiLCJleHAiOjE1OTk3ODAxMzcsImlhdCI6MTU5OTc3NjUzNywidGVuYW50X2lzcyI6Imh0dHBzOlwvXC9pZGNzLTkwMmE5NDRmZjY4NTRjNWZiZTk0NzUwZTQ4ZDY2YmU1LmlkZW50aXR5Lm9yYWNsZWNsb3VkLmNvbTo0NDMiLCJjbGllbnRfZ3VpZCI6ImMxNDYwZjZiODgxZTRhODBiMzNiYjNmYjhiMTIwYWI3IiwiY2xpZW50X25hbWUiOiJUaW1lIDIiLCJ0ZW5hbnQiOiJpZGNzLTkwMmE5NDRmZjY4NTRjNWZiZTk0NzUwZTQ4ZDY2YmU1IiwianRpIjoiMTFlYWYzYjQxNTliM2YwMjk3YWE4YjFkZmQ0NzA2NWEifQ.bgr49ZKsid3UZ1DWiStDMVCYglvOmtUFW41jdmyx4IqeW7rsk6UURdZqaeyqQPrfcsCfh_uYX-YQ5EoeCVqum1UDSBAPwF8iUnyjmLEFSd8-DLzY7OxvF38c_eSVw-x_qkJP28yVM3FQAdIwicdfeQN460dNXCvZKXwGeyP1o2SzCSIZWaH7fv03-z_OI--G4kLpLgrSyl5P_xCJP2sISIcqry1zFXl-nF8KOd5RDIoFUcquXN3doHi62gWwmj-sX5gDgJuur1H-H9n3LSa34GsloNwtxQDQ3KpyJR6DcTvtD5VSLosuykDIum_xDdRgCr3UDfpg3xXZKzNlhRUO7w'
headers = {'Authorization': 'Bearer ' + auth_token, 'Content-Type':'application/x-www-form-urlencoded'}
url = 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/accounts/v1/optin'
body = {"Name": "Igão", "Email": "bongi90@hotmail.com", "Phone": "+5511991353333"}

result = requests.post( url=url, data=body, headers=headers )

if result.status_code == 200:
    print( '{0} -> Deu certo com resultado {1}'.format( datetime.now(), result.json() ) )
else:
    print( '{0} -> Erro com codigo {1}'.format( datetime.now(), result.status_code ) )
    print( '{0} -> Erro com descricao "{1}"'.format( datetime.now(), result.json() ) )