from getpass import getpass
from api_hackaton_safra import use_api

def login():
    exit_screen = False
    while not exit_screen:

        print( '\nTela de Inicial' )
        print( '1 para login' )
        print( 'enter para sair' )
        escolha = input()

        if escolha == '1':
            account_id = input( 'Insira sua conta: ' )
            password = getpass( 'Insira sua senha: ' )

            if account_id in ( '00711234511', '00711234522', '00711234533', 'teste' ) and password == '1':
                termos()
            else:
                print( 'Usuário ou senha incorreto' )
        else:
            exit()



def termos():

    exit_screen = False
    while not exit_screen:

        print( '\nTermos' )
        print( 'bla bla bla bla bla' )
        print( '1 para aceitar' )
        print( '2 para negar' )
        escolha = input()

        if escolha == '1':
            cadastro()
        elif escolha == '2':
            exit()
        else:
            print( 'escolha inválida' )



def cadastro():

    print( '\nCadastro' )
    name = input( 'Nome: ' )
    name = input( 'E-mail: ' )
    name = input( 'Telefone: ' )

    exit_screen = False
    while not exit_screen:

        print( '1 para cadastrar' )
        print( '2 para voltar' )
        escolha = input()

        if escolha == '1':
            informacoes = {"Name": "Igão", "Email": "bongi90@hotmail.com", "Phone": "+5511991353333"}
            resposta = use_api( '00711234533', 'opt_in', informacoes )
            print( resposta )
            perfil()
        elif escolha == '2':
            termos()
        else:
            print( 'escolha inválida' )



def perfil():

    print( '\nPerfil' )
    name = input( 'pergunta 1: ' )

    exit_screen = False
    while not exit_screen:

        print( '1 para avancar' )
        print( '2 para voltar' )
        escolha = input()

        if escolha == '1':
            objetivo()
        elif escolha == '2':
            cadastro()
        else:
            print( 'escolha inválida' )



def objetivo():

    print( '\nObjetivo' )
    name = input( 'informe seu objetivo: ' )

    exit_screen = False
    while not exit_screen:

        print( '1 para avancar' )
        print( '2 para voltar' )
        escolha = input()

        if escolha == '1':
            detalhes()
        elif escolha == '2':
            perfil()
        else:
            print( 'escolha inválida' )



def detalhes():

    exit_screen = False
    while not exit_screen:

        print( '\nPrincipal - Detalhes' )
        nome = use_api( '00711234533', 'conta' )['Account']['Name']
        print( 'Olá {0}'.format( nome ) )
        saldo = float(use_api( '00711234533', 'saldo' ))
        print( 'R$ {0:,.2f}'.format( saldo ) )
        print( 'de R$ 100.000,00' )
        print( 'faltam R$ {0:,.2f}'.format( 100000 - saldo ) )
        print( '{0:.1f}%'.format( saldo / 1000 ) )
        print( '...' )
        print( '1 para Depósitos' )
        print( '2 para Desafios' )
        print( '3 para Adicionar saldo' )
        print( '4 Solicitar crédito' )
        print( '5 para sair' )
        escolha = input()

        if escolha == '1':
            depositos()
        elif escolha == '2':
            desafios()
        elif escolha == '3':
            print('Depositos')
        elif escolha == '4':
            print('Depositos')
        elif escolha == '5':
            exit()
        else:
            print( 'escolha inválida' )



def depositos():

    exit_screen = False
    while not exit_screen:

        print( '\nPrincipal - Depósitos' )
        print( 'Historico' )
        print( 'Valor     Motivo         Data' )
        extrato = use_api( '00711234533', 'extrato' )
        for lines in extrato:
            valor = float(lines['amount']['amount'])
            tipo_transacao = lines['creditDebitIndicator']
            if tipo_transacao == 'Debit':
                print( '- R$ {0:,.2f} '.format( valor ), end='' )
            elif tipo_transacao == 'Credit':
                print( '+ R$ {0:,.2f} '.format( valor ), end='' )
            print( lines['transactionInformation'], end='' )
            print( '  {0}'.format(lines['valueDateTime']) )
        print( '...' )
        print( '1 para Detalhes' )
        print( '2 para Desafios' )
        print( '3 para sair' )
        escolha = input()

        if escolha == '1':
            detalhes()
        elif escolha == '2':
            desafios()
        elif escolha == '3':
            exit()
        else:
            print( 'escolha inválida' )



def desafios():

    exit_screen = False
    while not exit_screen:

        print( '\nPrincipal - Desafios' )
        print( 'Metas atingidas' )
        print( '10% - 100 pontos' )
        print( '...' )
        print( '1 para Detalhes' )
        print( '2 para Depósitos' )
        print( '3 para Leaderboard' )
        print( '4 para sair' )
        escolha = input()

        if escolha == '1':
            detalhes()
        elif escolha == '2':
            depositos()
        elif escolha == '3':
            leaderboard()
        elif escolha == '4':
            exit()
        else:
            print( 'escolha inválida' )



def leaderboard():

    exit_screen = False
    while not exit_screen:

        print( '\nLeaderboard' )
        print( 'Pessoa Objetivos Medalhas   Pontos' )
        print( 'Igão A Viagem NY 8 medalhas 100.000 pontos' )
        print( '...' )
        print( '1 para sair' )
        escolha = input()

        if escolha == '1':
            exit_screen = True
        else:
            print( 'escolha inválida' )



if __name__ == '__main__':
    login()