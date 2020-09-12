import sys
from getpass import getpass
import re
from datetime import datetime
import requests
from api_hackaton_safra import use_api



SCREEN_WIDTH = 70



def print_line( texto, left=False ):

    if texto == '':
        print( '|', end='' )
        for i in range( SCREEN_WIDTH ):
            print( '-', end='' )
        print( '|' )
    else:
        blank_size = SCREEN_WIDTH - len(texto)

        if blank_size >= 2:
            left_size = int(blank_size / 2)
            right_size = int(blank_size / 2)

            if left:
                left_size = 1
                right_size = blank_size - 1
            elif blank_size % 2 != 0:
                right_size += 1
        else:
            left_size = 1
            right_size = 1
        
        print( '|', end='' )
        for i in range( left_size ):
            print( ' ', end='' )
        print( texto, end='' )
        for i in range( right_size ):
            print( ' ', end='' )
        print( '|' )



def input_line( input_type, print_value='', print_error='' ):
    if input_type == 'email':
        return check_email( print_value, print_error )
    elif input_type == 'float':
        return float(check_value( print_value, print_error ))
    elif input_type == 'integer':
        return int(check_value( print_value, print_error ))
    elif input_type == 'date':
        return check_date( print_value, print_error )
    elif input_type == 'choice':
        return input( '| ' )
    elif input_type == 'password':
        return getpass( '| ' + print_value + ': ' )
    elif input_type == 'any':
        return input( '| ' + print_value + ': ' )
    elif input_type == 'cpf':
        return check_cpf( print_value, print_error )
    elif input_type == 'cep':
        return check_cep( print_value, print_error )



def check_email( print_email, print_error ):
    #regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex = '[^@]+@[^@]+\.[^@]+'
    email = ''
    while not re.search( regex,email ):
        email = input( '| ' + print_email + ': ' )
        if not re.search( regex,email ):
            print_line( print_error )
    return email



def check_value( print_valor, print_error ):
    valor = ''
    while not valor.isnumeric():
        valor = input( '| ' + print_valor + ': ' )
        if not valor.isnumeric():
            print_line( print_error )
    return valor



def check_date( print_date, print_error ):
    data = None
    valid = False
    while not valid:
        data = input( '| ' + print_date + ': ' )
        if data.find('/') != -1:
            day, month, year = data.split('/')
            try :
                datetime(int(year),int(month),int(day))
                valid = True
            except ValueError :
                print_line( print_error )
        else:
            print_line( print_error )
    return data



def check_cpf( print_cpf, print_error ):
    valido = False
    cpf = None
    while not valido:
        cpf = input( '| ' + print_cpf + ': ' ).replace('.','').replace('-','')
        if len(cpf) >= 11:
            cpf_check = cpf[:9]
            soma = 0
            for i in range(1, 10):
                soma += i * int(cpf_check[i-1])
            resto = soma % 11
            if resto == 10:
                resto = 0
            cpf_check += str( resto )
            soma = 0
            for i in range(10):
                soma += i * int(cpf_check[i])
            resto = soma % 11
            if resto == 10:
                resto = 0
            cpf_check += str( resto )
            if cpf == cpf_check:
                valido = True
            else:
                print_line( print_error )
        else:
            print_line( print_error )
    return cpf



def check_cep( print_cep, print_error ):
    status_code = 0
    while status_code != 200:
        cep = input( '| ' + print_cep + ': ' )
        url = 'http://viacep.com.br/ws/{0}/json'.format( cep )
        response = requests.get( url=url )
        status_code = response.status_code
        if status_code != 200:
            print_line( print_error )
    return response.json()



def login():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Tela de Inicial' )
        print_line( '  ' )
        print_line( '1 para login', left=True )
        print_line( 'Enter para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            account_id = input_line( 'any', 'Insira sua conta' )
            password = input_line( 'password', 'Insira sua senha' )

            if account_id in ( '00711234511', '00711234522', '00711234533', 'teste' ) and password == '1':
                print_line( '' )
                termos()
            else:
                print_line( 'Usuário ou senha incorreto' )
        else:
            print_line( '' )
            exit()



def termos():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Termos' )
        for i in range( 8 ):
            print_line( 'bla bla bla bla' )
        print_line( '  ' )
        print_line( '1 para Aceito', left=True )
        print_line( '2 para Não aceito', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            print_line( '' )
            cadastro()
        elif choice == '2':
            print_line( '' )
            exit()
        else:
            print_line( 'Escolha inválida' )



def cadastro():

    print_line( '' )
    print_line( 'Cadastro' )
    print_line( '  ' )
    name = input_line( 'any', 'Nome completo' )
    apelido = input_line( 'any', 'Apelido' )
    cpf = input_line( 'cpf', 'CPF', 'CPF inválido' )
    email = input_line( 'email', 'E-mail', 'E-mail inválido' )
    telefone = input_line( 'any', 'Telefone' )
    infos_cep = input_line( 'cep', 'CEP', 'CEP inválido' )
    cep = infos_cep['cep']
    uf = infos_cep['uf']
    cidade = infos_cep['localidade']
    bairro = infos_cep['bairro']
    endereco = infos_cep['logradouro']
    print_line( 'UF: {0}'.format( uf ), left=True )
    print_line( 'Cidade: {0}'.format( cidade ), left=True )
    print_line( 'Bairro: {0}'.format( bairro ), left=True )
    print_line( 'Endereço: {0}'.format( endereco ), left=True )
    numero = input_line( 'integer', 'Nº', 'Número inválido' )
    complemento = input_line( 'any', 'Complemento' )
    senha1 = '1'
    senha2 = '2'
    while senha1 != senha2:
        senha1 = input_line( 'password', 'Senha' )
        senha2 = input_line( 'password', 'Confirme a senha' )
        if senha1 != senha2:
            print_line( 'Senhas não conferem' )
    print_line( '  ' )

    exit_screen = False
    while not exit_screen:

        print_line( '1 para cadastrar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            infos = {"Name": name, "Email": email, "Phone": telefone}
            #resposta = use_api( '00711234533', 'opt_in', infos )
            resposta = 'API ainda nao ta funcionando o optin'
            print_line( resposta )
            print_line( '' )
            perfil()
        elif choice == '2':
            print_line( '' )
            termos()
        else:
            print_line( 'Escolha inválida' )



def perfil():

    print_line( '' )
    print_line( 'Perfil' )
    print_line( 'Nos ajude a te conhecer' )
    print_line( 'um pouco melhor' )

    exit_question = False
    while not exit_question:
        print_line( '  ' )
        print_line( 'Você já investiu seu dinheiro alguma vez?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'não':
            exit_question = True
        else:
            print_line( 'Escolha inválida' )
    
    exit_question = False
    while not exit_question:
        print_line( '  ' )
        print_line( 'Você tem o costume de guardar dinheiro?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'não':
            exit_question = True
        else:
            print_line( 'Escolha inválida' )
        
    exit_question = False
    while not exit_question:
        print_line( '  ' )
        print_line( 'Você já esteve no vermelho?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'não':
            exit_question = True
        else:
            print_line( 'Escolha inválida' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para avançar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            print_line( '' )
            objetivo()
        elif choice == '2':
            print_line( '' )
            cadastro()
        else:
            print_line( 'Escolha inválida' )



def objetivo():

    print_line( '' )
    print_line( 'Objetivo' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Seu objetivo' )
    valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )
    data = input_line( 'date', 'Data final', 'Data inválida' )
    print_line( '  ' )

    exit_screen = False
    while not exit_screen:

        print_line( '1 para avançar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            print_line( '' )
            detalhes()
        elif choice == '2':
            print_line( '' )
            perfil()
        else:
            print_line( 'Escolha inválida' )



def detalhes():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Principal - Detalhes' )
        print_line( '  ' )
        nome = use_api( '00711234533', 'conta' )['Nickname']
        print_line( 'Olá {0}'.format( nome ) )
        saldo = float(use_api( '00711234533', 'saldo' ))
        print_line( 'R$ {0:,.2f}'.format( saldo ) )
        print_line( 'de R$ 100.000,00' )
        print_line( 'faltam R$ {0:,.2f}'.format( 100000 - saldo ) )
        print_line( '{0:.1f}%'.format( saldo / 1000 ) )
        print_line( '...' )
        print_line( '  ' )
        print_line( '1 para Extrato', left=True )
        print_line( '2 para Desafios', left=True )
        print_line( '3 para Adicionar saldo', left=True )
        print_line( '4 Solicitar crédito', left=True )
        print_line( '5 Loja de pontos', left=True )
        print_line( '6 Convidar', left=True )
        print_line( '7 Compartilhar', left=True )
        print_line( '8 para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            depositos()
        elif choice == '2':
            desafios()
        elif choice == '3':
            adicionar_saldo()
        elif choice == '4':
            print_line('nao disponibilizado ainda')
        elif choice == '5':
            print_line('nao disponibilizado ainda')
        elif choice == '6':
            convidar_pessoas()
        elif choice == '7':
            compartilhar_objetivo()
        elif choice == '8':
            exit()
        else:
            print_line( 'Escolha inválida' )



def extrato():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Principal - Extrato' )
        print_line( '  ' )
        print_line( 'Historico' )
        print_line( 'Valor           Motivo            Data' )
        extrato = use_api( '00711234533', 'extrato' )
        for lines in extrato:
            value_to_print = ''
            valor = float(lines['amount']['amount'])
            tipo_transacao = lines['creditDebitIndicator']
            if tipo_transacao == 'Debit':
                value_to_print += '-'
            elif tipo_transacao == 'Credit':
                value_to_print += '+'
            value_to_print += 'R$ {0:,.2f} '.format( valor )
            value_to_print += '  {0}'.format( lines['transactionInformation'] )
            value_to_print += '  {0}'.format(lines['valueDateTime'])
            print_line( value_to_print )
        print_line( '...' )
        print_line( '  ' )
        print_line( '1 para Detalhes', left=True )
        print_line( '2 para Desafios', left=True )
        print_line( '3 para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            detalhes()
        elif choice == '2':
            desafios()
        elif choice == '3':
            exit()
        else:
            print_line( 'Escolha inválida' )



def desafios():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Principal - Desafios' )
        print_line( '  ' )
        print_line( 'Metas atingidas' )
        print_line( '10% - 100 pontos' )
        print_line( '...' )
        print_line( '  ' )
        print_line( '1 para Detalhes', left=True )
        print_line( '2 para Extrato', left=True )
        print_line( '3 para Leaderboard', left=True )
        print_line( '4 para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice', left=True )

        if choice == '1':
            detalhes()
        elif choice == '2':
            depositos()
        elif choice == '3':
            leaderboard()
        elif choice == '4':
            exit()
        else:
            print_line( 'Escolha inválida' )



def leaderboard():

    exit_screen = False
    while not exit_screen:

        print_line( '' )
        print_line( 'Leaderboard' )
        print_line( '  ' )
        print_line( 'Pessoa   Objetivos   Medalhas     Pontos' )
        print_line( 'Igão   A Viagem NY   8 medalhas 100.000 pontos' )
        print_line( '...' )
        print_line( '  ' )
        print_line( 'Enter para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )



def adicionar_saldo():

    print_line( '' )
    print_line( 'Adicionar Saldo' )
    print_line( '  ' )
    chave = input_line( 'any', 'Chave Pix' )
    valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )
    print_line( '  ' )

    exit_screen = False
    while not exit_screen:

        print_line( '1 para adicionar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            print_line( 'Valor de R$ {0:.2f} adicionado com sucesso'.format( valor ) )
            detalhes()
        elif choice == '2':
            detalhes()
        else:
            print_line( 'Escolha inválida' )



def convidar_pessoas():

    print_line( '' )
    print_line( 'Convidar pessoas' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Nome do objetivo' )
    print_line( '  ' )

    exit_screen = False
    while not exit_screen:

        print_line( '1 para digitar as informações', left=True )
        print_line( '2 para QR Code', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            nome = input_line( 'any', 'Nome' )
            cpf = input_line( 'any', 'CPF' )
            email = input_line( 'email', 'E-mail', 'E-mail inválido' )
            print_line( '  ' )

            exit_screen = False
            while not exit_screen:

                print_line( '1 para adicionar', left=True )
                print_line( '2 para voltar', left=True )
                print_line( '  ' )
                choice = input_line( 'choice' )

                if choice == '1':
                    print_line( 'Solicitação enviada para {0} no e-mail {1}'.format(nome, email) )
                    detalhes()
                elif choice == '2':
                    exit_screen = True
                else:
                    print_line( 'Escolha inválida' )
        elif choice == '2':
            print_line( 'Scaneie o QR code ou compartilhe através das redes sociais' )
            print_line( '  ' )
            print_line( 'Enter para sair' )
            input()
            detalhes()
        elif choice == '3':
            detalhes()
        else:
            print_line( 'Escolha inválida' )



def compartilhar_objetivo():

    print_line( '' )
    print_line( 'Compartilhar objetivo' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Nome do objetivo: ' )
    print_line( '  ' )

    exit_screen = False
    while not exit_screen:

        print_line( '1 para digitar as informações', left=True )
        print_line( '2 para QR Code', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice == '1':
            chave = input_line( 'any', 'Chave Pix' )
            valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )
            print_line( '  ' )

            exit_screen = False
            while not exit_screen:

                print_line( '1 para adicionar', left=True )
                print_line( '2 para voltar', left=True )
                print_line( '  ' )
                choice = input_line( 'choice' )

                if choice == '1':
                    print_line( 'Valor de R$ {0:.2f} compartilhado com sucesso'.format(float(valor)) )
                    detalhes()
                elif choice == '2':
                    exit_screen = True
                else:
                    print_line( 'Escolha inválida' )
        elif choice == '2':
            print_line( 'Scaneie o QR code ou compartilhe através das redes sociais' )
            print_line( '  ' )
            print_line( 'Enter para sair' )
            input()
            detalhes()
        elif choice == '3':
            detalhes()
        else:
            print_line( 'Escolha inválida' )



if __name__ == '__main__':
    if len( sys.argv ) == 1:
        print('Por favor, selecione a tela que deseja iniciar como argumento')
        print('Telas:')
        print('- login')
        print('- principal')
        print('Ex: python app.py login')
    else:
        screen = sys.argv[1]
        if screen == 'login':
            login()
        elif screen == 'principal':
            #cadastro()
            #perfil()
            objetivo()
            #detalhes()
        else:
            print( 'Argumento inválido' )
            print('Por favor, selecione a tela que deseja iniciar como argumento')
            print('Telas:')
            print('- login')
            print('- principal')
            print('Ex: python app.py login')