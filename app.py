import sys
from getpass import getpass
import re
from datetime import datetime, timedelta
import requests
from api_hackaton_safra import use_api


SCREEN_WIDTH = 70


# Funções de formatação
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



#Funções de validação
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
                data = datetime(int(year),int(month),int(day))
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



#Funções das telas
def login():

    print_line( 'Tela de Inicial' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para login', left=True )
        print_line( '2 para cadastrar', left=True )
        print_line( '3 para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3']:

            exit_screen = True
            global screen
            if choice == '1':
                exit_screen = False
                print_line( '  ' )
                account_id_input = input_line( 'any', 'Insira sua conta' )
                password = input_line( 'password', 'Insira sua senha' )

                if account_id_input in ( '00711234511', '00711234522', '00711234533', 'teste' ) and password == '1':
                    global account_id
                    account_id = '00711234533'
                    exit_screen = True
                    screen = 'detalhes'
                else:
                    print_line( 'Usuário ou senha incorreto' )
            elif choice == '2':
                screen = 'termos'
            elif choice == '3':
                global exit_app
                exit_app = True
        else:
            print_line( 'Escolha inválida' )




def termos():

    print_line( 'Termos' )
    print_line( 'LGPD' )
    for i in range( 4 ):
        print_line( 'bla bla bla bla bla bla' )
    print_line( 'Termos de uso' )
    for i in range( 4 ):
        print_line( 'bla bla bla bla bla bla' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para Aceito', left=True )
        print_line( '2 para Não aceito', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            if choice == '1':
                global screen
                screen = 'cadastro'
            elif choice == '2':
                global exit_app
                exit_app = True
        else:
            print_line( 'Escolha inválida' )



def cadastro():

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

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para cadastrar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            if choice == '1':
                #infos = {"Name": name, "Email": email, "Phone": telefone}
                #resposta = use_api( account_id, 'opt_in', infos )
                #print_line( resposta )
                screen = 'perfil'
            elif choice == '2':
                screen = 'termos'
        else:
            print_line( 'Escolha inválida' )


def perfil():

    print_line( 'Perfil' )
    print_line( 'Nos ajude a te conhecer' )
    print_line( 'um pouco melhor' )

    exit_question = False
    while not exit_question:

        print_line( '  ' )
        print_line( 'Você que paga todas as suas contas?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'nao':
            exit_question = True
        else:
            print_line( 'Escolha inválida' )
    
    exit_question = False
    while not exit_question:
        print_line( '  ' )
        print_line( 'Você tem o costume de guardar dinheiro?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'nao':
            exit_question = True
        else:
            print_line( 'Escolha inválida' )
        
    exit_question = False
    while not exit_question:
        print_line( '  ' )
        print_line( 'Você já esteve no vermelho?' )
        print_line( '1.sim      2.não' )
        choice = input_line( 'choice' )
        if choice == '1' or choice.lower() == 'sim' or choice == '2' or choice.lower().replace('ã','a') == 'nao':
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

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'objetivo'
            elif choice == '2':
                screen = 'cadastro'
        else:
            print_line( 'Escolha inválida' )


def objetivo():

    print_line( 'Objetivo' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Nos diga qual seu objetivo' )
    valor_objetivo = input_line( 'float', 'Nos informe o valor que pretende alncançar em R$', 'Valor inválido' )
    future_date = False
    while not future_date:
        data = input_line( 'date', 'Quando vamos celebrar essa conquista', 'Data inválida' )
        if data >= datetime.now() + timedelta(days=30):
            future_date = True
        else:
            print_line( 'Selecione uma data pelo menos 1 mês no futuro' )
    print_line( 'Qual o valor mpinimo que pretende adicionar', left = True )
    valor_minimo_mes = input_line( 'float', 'em R$ como saldo mensalmente', 'Valor inválido' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para adicionar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'brindes'
            elif choice == '2':
                screen = 'perfil'
        else:
            print_line( 'Escolha inválida' )



def brindes():

    print_line( 'Brindes' )
    print_line( '  ' )
    print_line( 'Agora nos diga qual brindes' )
    print_line( 'você gostaria de ganhar?' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para adicionar restaurante', left=True )
        print_line( '2 para adicionar mercado', left=True )
        print_line( '3 para adicionar bar', left=True )
        print_line( '4 para adicionar viagem', left=True )
        print_line( '5 para adicionar gasolina', left=True )
        print_line( '6 para adicionar crédito de celular', left=True )
        print_line( '7 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            exit_screen = True
            global screen
            if int(choice) < 7:
                screen = 'primeiro_saldo'
            elif choice == '7':
                screen = 'objetivo'
        else:
            print_line( 'Escolha inválida' )



def primeiro_saldo():

    print_line( 'Adicionar Saldo' )
    print_line( '  ' )
    print_line( 'Agora que nos conhecemos melhor,' )
    print_line( 'adicione seu primeiro saldo para' )
    print_line( 'iniciar sua jornada Easy Goal' )
    chave = input_line( 'any', 'Chave Pix' )
    valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para adicionar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'detalhes'
                print_line( 'Valor de R$ {0:.2f} adicionado com sucesso'.format( valor ) )
            elif choice == '2':
                screen = 'brindes'
        else:
            print_line( 'Escolha inválida' )



def detalhes():

    print_line( 'Principal - Detalhes' )
    print_line( '  ' )
    nome = use_api( account_id, 'conta' )['Nickname']
    print_line( 'Olá {0}'.format( nome ) )
    saldo = float(use_api( account_id, 'saldo' ))
    print_line( 'R$ {0:,.2f}'.format( saldo ) )
    print_line( 'de R$ 100.000,00' )
    print_line( 'faltam R$ {0:,.2f}'.format( 100000 - saldo ) )
    print_line( '{0:.1f}%'.format( saldo / 1000 ) )
    print_line( '...' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 Extrato', left=True )
        print_line( '2 Desafios', left=True )
        print_line( '3 Rendimento', left=True )
        print_line( '4 Resgate', left=True )
        print_line( '5 Adicionar saldo', left=True )
        print_line( '6 Compartilhar objetivo', left=True )
        print_line( '7 Loja de pontos', left=True )
        print_line( '8 Indique um amigo', left=True )
        print_line( '9 Investimentos', left=True )
        print_line( '10 Reportar erro', left=True )
        print_line( '11 Sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'extrato'
            elif choice == '2':
                screen = 'desafios'
            elif choice == '3':
                screen = 'rendimentos'
            elif choice == '4':
                screen = 'resgatar_saldo'
            elif choice == '5':
                screen = 'adicionar_saldo'
            elif choice == '6':
                screen = 'compartilhar_objetivo'
            elif choice == '7':
                screen = 'loja_pontos'
            elif choice == '8':
                screen = 'indique_amigo'
            elif choice == '9':
                screen = 'investimentos'
            elif choice == '10':
                screen = 'reportar_erro'
            elif choice == '11':
                global exit_app
                exit_app = True
        else:
            print_line( 'Escolha inválida' )



def rendimentos():

    print_line( 'Rendimentos' )
    print_line( '  ' )
    print_line( 'Historico' )
    print_line( 'Investimento      Valor      Rentabilidade' )
    print_line( '   CDB         R$  1.020,00       2,0 % ' )
    print_line( '   LCI         R$  5.190,00       3,0 % ' )
    print_line( '  Fundos       R$  9.780,00      -2,0 % ' )
    print_line( '...' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para Extrato', left=True )
        print_line( '2 para Desafios', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'extrato'
            elif choice == '2':
                screen = 'desafios'
            elif choice == '3':
                screen = 'detalhes'
        else:
            print_line( 'Escolha inválida' )



def resgatar_saldo():

    print_line( 'Resgatar Saldo' )
    print_line( '  ' )
    chave = input_line( 'any', 'Chave Pix' )
    valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para resgatar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            screen = 'detalhes'
            if choice == '1':
                print_line( 'Valor de R$ {0:.2f} resgatado com sucesso'.format( valor ) )
        else:
            print_line( 'Escolha inválida' )



def adicionar_saldo():

    print_line( 'Adicionar Saldo' )
    print_line( '  ' )
    chave = input_line( 'any', 'Chave Pix' )
    valor = input_line( 'float', 'Valor em R$', 'Valor inválido' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para adicionar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            screen = 'detalhes'
            if choice == '1':
                print_line( 'Valor de R$ {0:.2f} adicionado com sucesso'.format( valor ) )
        else:
            print_line( 'Escolha inválida' )



def compartilhar_objetivo():

    print_line( 'Compartilhar objetivo' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Nome do objetivo: ' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para digitar as informações', left=True )
        print_line( '2 para QR Code', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3']:
            exit_screen = True
            global screen
            screen = 'detalhes'
            if choice == '1':
                nome = input_line( 'any', 'Nome' )
                cpf = input_line( 'cpf', 'CPF', 'CPF inválido' )
                email = input_line( 'email', 'E-mail', 'E-mail inválido' )
                print_line( '  ' )

                exit_screen = False
                while not exit_screen:

                    print_line( '1 para adicionar', left=True )
                    print_line( '2 para voltar', left=True )
                    print_line( '  ' )
                    choice = input_line( 'choice' )

                    if choice in ['1', '2']:
                        exit_screen = True
                        if choice == '1':
                            print_line( 'Valor de R$ {0:.2f} compartilhado com sucesso'.format(float(valor)) )
                    else:
                        print_line( 'Escolha inválida' )
            elif choice == '2':
                print_line( 'Scaneie o QR code ou compartilhe através das redes sociais' )
                print_line( '  ' )
                print_line( 'Enter para sair' )
                choice = input_line( 'choice' )
        else:
            print_line( 'Escolha inválida' )



def loja_pontos():

    print_line( 'Loja' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 R$ 20,00 no Ifood por 5000 moedas', left=True )
        print_line( '2 R$ 50,00 no Uber por 12000 moedas', left=True )
        print_line( '3 R$ 200,00 na CVC por 30000 moedas', left=True )
        print_line( '4 um mês de Netflix por 5000 moedas', left=True )
        print_line( '5 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3', '4', '5']:
            exit_screen = True
            global screen
            screen = 'detalhes'
            if int(choice) < 5:
                print_line( 'Compra realizada com sucesso!' )
        else:
            print_line( 'Escolha inválida' )



def indique_amigo():

    print_line( 'Indique a um amigo' )
    print_line( '  ' )
    objetivo = input_line( 'any', 'Nome do objetivo' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para digitar as informações', left=True )
        print_line( '2 para QR Code', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3']:
            exit_screen = True
            global screen
            screen = 'detalhes'
            if choice == '1':
                nome = input_line( 'any', 'Nome' )
                cpf = input_line( 'cpf', 'CPF', 'CPF inválido' )
                email = input_line( 'email', 'E-mail', 'E-mail inválido' )

                exit_screen = False
                while not exit_screen:

                    print_line( '  ' )
                    print_line( '1 para adicionar', left=True )
                    print_line( '2 para voltar', left=True )
                    print_line( '  ' )
                    choice = input_line( 'choice' )

                    if choice in ['1', '2']:
                        exit_screen = True
                        if choice == '1':
                            print_line( 'Solicitação enviada para {0} no e-mail {1}'.format(nome, email) )
                    else:
                        print_line( 'Escolha inválida' )
            elif choice == '2':
                print_line( 'Scaneie o QR code ou compartilhe através das redes sociais' )
                print_line( '  ' )
                print_line( 'Enter para sair' )
                choice = input_line( 'choice' )
        else:
            print_line( 'Escolha inválida' )



def investimentos():

    print_line( 'Investimento' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para investir', left=True )
        print_line( '2 para quiz', left=True )
        print_line( '3 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3']:
            exit_screen = True
            global screen
            if choice == '1':

                exit_screen = False
                while not exit_screen:

                    print_line( '  ' )
                    print_line( '1 Fundos', left=True )
                    print_line( '2 Renda fixa', left=True )
                    print_line( '3 Renda variável', left=True )
                    print_line( '4 COE', left=True )
                    print_line( '5 Ofertas públicas', left=True )
                    print_line( '6 Tesouro direto', left=True )
                    print_line( '7 Previdência', left=True )
                    print_line( '8 para voltar', left=True )
                    print_line( '  ' )
                    choice = input_line( 'choice' )

                    if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                        exit_screen = True
                        screen = 'detalhes'
                        if choice == '1':
                            print_line( 'Seu dinheiro foi investido em Fundos' )
                        elif choice == '2':
                            print_line( 'Seu dinheiro foi investido em Renda fixa' )
                        elif choice == '3':
                            print_line( 'Seu dinheiro foi investido em Renda variável' )
                        elif choice == '4':
                            print_line( 'Seu dinheiro foi investido em COE' )
                        elif choice == '5':
                            print_line( 'Seu dinheiro foi investido em Ofertas públicas' )
                        elif choice == '6':
                            print_line( 'Seu dinheiro foi investido em Tesouro direto' )
                        elif choice == '7':
                            print_line( 'Seu dinheiro foi investido em Previdência' )
                    else:
                        print_line( 'Escolha inválida' )

            elif choice == '2':
                screen = 'quiz'
            elif choice == '3':
                screen = 'detalhes'
        else:
            print_line( 'Escolha inválida' )



def quiz():

    print_line( 'Quiz' )
    print_line( '  ' )
    print_line( 'Quando é a Alíquota sobre o' )
    print_line( 'imposto de Renda do CDB retido' )
    print_line( 'na fonte no prazo de até 180 dias?' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para 20 %', left=True )
        print_line( '2 para 22,5 %', left=True )
        print_line( '3 para 23 %', left=True )
        print_line( '4 para 15 %', left=True )
        print_line( '5 para sair', left=True )
        choice = input_line( 'choice' )

        if choice in ['1', '2', '3', '4', '5']:
            exit_screen = True
            global screen
            screen = 'investimentos'
            if int(choice) < 5:
                if choice == '2':
                    print_line( 'Acertou !!!', left=True )
                else:
                    print_line( 'Não foi dessa vez :(', left=True )
                print_line( '  ' )
                print_line( 'Enter para sair', left=True )
                print_line( '  ' )
                choice = input_line( 'choice' )
        else:
            print_line( 'Escolha inválida' )



def reportar_erro():

    print_line( 'Reportar erro' )
    print_line( '  ' )
    chave = input_line( 'any', 'Em qual lugar você encontrou o problema' )
    valor = input_line( 'any', 'Descreva sobre o problema:' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para enviar', left=True )
        print_line( '2 para voltar', left=True )
        print_line( '  ' )
        choice = input_line( 'choice' )

        if choice in ['1', '2']:
            exit_screen = True
            global screen
            screen = 'detalhes'
        else:
            print_line( 'Escolha inválida' )



def extrato():

    print_line( 'Principal - Extrato' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( 'Historico' )
        print_line( 'Valor           Motivo            Data' )
        extrato = use_api( account_id, 'extrato' )
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

        if choice in ['1', '2', '3']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'detalhes'
            elif choice == '2':
                screen = 'desafios'
            elif choice == '3':
                global exit_app
                exit_app = True
        else:
            print_line( 'Escolha inválida' )



def desafios():

    print_line( 'Principal - Desafios' )
    print_line( '  ' )
    print_line( 'Metas atingidas' )
    print_line( '10% - 100 pontos - 10/04/2020' )
    print_line( '20% - 120 pontos - 12/05/2020' )
    print_line( '30% - 150 pontos - 19/06/2020' )
    print_line( '...' )
    print_line( '  ' )
    print_line( 'Medalhas' )
    print_line( '...' )

    exit_screen = False
    while not exit_screen:

        print_line( '  ' )
        print_line( '1 para Detalhes', left=True )
        print_line( '2 para Extrato', left=True )
        print_line( '3 para Leaderboard', left=True )
        print_line( '4 para sair', left=True )
        print_line( '  ' )
        choice = input_line( 'choice', left=True )

        if choice in ['1', '2', '3', '4']:
            exit_screen = True
            global screen
            if choice == '1':
                screen = 'detalhes'
            elif choice == '2':
                screen = 'depositos'
            elif choice == '3':
                screen = 'ranking'
            elif choice == '4':
                global exit_app
                exit_app = True
        else:
            print_line( 'Escolha inválida' )



def ranking():

    print_line( 'Ranking' )
    print_line( '  ' )
    print_line( 'Pessoa     Objetivos      Medalhas       Pontos' )
    print_line( 'Igão       Viagem NY    50 medalhas  100.000 pontos' )
    print_line( 'Thamires     Carro      42 medalhas   91.000 pontos' )
    print_line( 'Lucas        Casa       40 medalhas   85.000 pontos' )
    print_line( 'Lucas       Viagem      35 medalhas   80.000 pontos' )
    print_line( 'Mikael     Apartamento  34 medalhas   76.000 pontos' )
    print_line( '...' )
    print_line( '  ' )
    print_line( 'Enter para sair', left=True )
    print_line( '  ' )
    choice = input_line( 'choice' )
    global screen
    screen = 'desafios'



# Main
if __name__ == '__main__':
    exit_app = False
    screen = 'login'
    account_id = ''
    while not exit_app:
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get( screen )
        if not method:
            print_line( 'Tela ainda não configurada' )
            exit_app = True
        print_line( '' )
        method()
        print_line( '' )