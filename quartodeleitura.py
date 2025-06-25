import random
import os
import json

ARQUIVO_USUARIOS = 'usuarios.json'

# lista com os livros disponíveis
livros_infantis = ['A lua cheia de...', 'O colecionador de infinitos', 'Chapeuzinho vermelho', 'Ainda uma flor resta', 'O gato da árvore de desejos']
livros_adolescentes = ['O Pequeno Príncipe', 'Jogos Vorazes', 'Harry Potter e a Pedra Filosofal', 'Fazendo Meu Filme', 'A Seleção']
livros_jovens = ['Dom Casmurro', 'Um Estudo em Vermelho', '1984', 'A Menina que Roubava Livros', 'Bem-vindos à livraria Hyunam-dong']

# lista com os Estados válidos
estados_validos = ['AM', 'PA', 'AC', 'RO', 'RR', 'AP', 
                   'MT', 'MS', 'GO', 'TO', 'DF', 
                   'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA',
                   'MG', 'ES', 'RJ', 'SP',
                   'PR', 'SC', 'RS']

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='UTF-8') as arquivo:
            return json.load(arquivo)
    return {"usuarios: {}"}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def carregar_dados_usuario(email):
    dados = carregar_usuarios()
    return dados['usuarios'].get(email, None)

usuario_logado = None

def cadastro():
    usuarios = carregar_usuarios()['usuarios']
    # nome
    while True:
        nome = input('Qual é o seu nome? ').title().strip()
        if all(n.isalpha() or n.isspace() for n in nome):
            break
        else: 
            print('Nome inválido. Utilize apenas letras.')
    # idade
    while True:
        idade = input('Qual é a sua idade? ')
        if idade.isdigit():
            break
        else:
            print('Idade inválida. Utilize apenas números')
    # Estado
    while True:
        estado = input('Em que estado você mora? ').upper()
        if estado in estados_validos:
            break
        else:
            print('Estado inválido. Insira apenas a sigla do estado (ex.: PE).')
    # Cidade
    while True:
        cidade = input('Em que cidade você vive? ').title()
        if all(c.isalpha() or c.isspace() for c in cidade):
            break
        else: 
            print('Cidade inválida. Utilize apenas letras.')
    # email
    while True:
        email = input('Digite seu email: ').strip().lower()
        if email in usuarios:
            print('Esse email já está sendo utilizado. Tente novamente.')
        elif '@' not in email:
            print('Email inválido. Motivo: não possui @.')
        elif ' ' in email:
            print('Email inválido. Motivo: contém espaços.')
        elif not (email.endswith('gmail.com') or email.endswith('ufrpe.br')):
            print('Email inválido. Motivo: domínio inválido, utilize apenas "gmail.com" ou "ufrpe.br".')
        else:
            break
    # senha
    while True:
        senha = input('Digite sua senha: ')
        if len(senha) == 6 and senha.isdigit():
            break
        else:
            print('Senha inválida. Motivo: a senha deve ter seis números.')
    ### PREFERÊNCIAS
    # livros digitais
    while True:
        livros_digitais = input('Quantos livros, no formato digital, você leu esse ano? ')
        if livros_digitais.isdigit():
            break
        else:
            print('Erro. Digite apenas números')
    # livros digitais
    while True:
        livros_fisicos = input('Quantos livros, no formato físico, você leu esse ano? ')
        if livros_fisicos.isdigit():
            break
        else:
            print('Erro. Digite apenas números.')
    # preferências
    while True:
        preferencia = input('Você prefere ler livros no formato digital ou físico? ')
        if preferencia == 'digital' or 'físico' or 'fisico':
            break
        else:
            print('Erro. Digite apenas "digital" ou "físico".')
    # horas de estudo
    while True: 
        h_livros_estudos = input('Quantas horas, por semana, você dedica a leitura de livros com fins acadêmicos? ')
        if h_livros_estudos.isdigit():
            break
        else:
            print('Erro. Digite apenas números.')
    # horas de diversão
    while True:
        h_livros_entretenimento = input('Quantas horas, por semana, você dedica a leitura de livros por entretenimento? ')
        if h_livros_entretenimento.isdigit():
            break
        else:
            print('Erro. Digite apenas números.')

    usuarios[email] = {
        'nome': nome,
        'idade': idade,
        'senha': senha,
        'estado': estado,
        'cidade': cidade, 
        'livrosDigitais': livros_digitais,
        'livrosFisicos': livros_fisicos, 
        'preferência': preferencia, 
        'horasEstudo': h_livros_estudos, 
        'horasEntretenimento': h_livros_entretenimento
    }

    salvar_usuarios({"usuarios": usuarios})
    print("Usuário cadastrado com sucesso!")

def login():
    global usuario_logado
    
    usuarios = carregar_usuarios()['usuarios']
    print('Bom te ver de volta!')
    email = input('Qual é seu email? ')
    senha = input('Qual é sua senha? ')
    
    usuario = carregar_dados_usuario(email)

    if (email in usuarios and usuarios[email]['senha'] == senha):
        print(f'Olá {usuarios[email]['nome']}.')
        usuario_logado = usuario
    else:
        print('Email ou senha inválidos. Tente novamente.')

def deletar_conta():
    dados = carregar_usuarios()
    usuarios = dados['usuarios']

    while True:
        email = input('Digite o seu email (digite "s" para sair): ').lower().strip()
        if email in usuarios:
            confirmacao = input(f'Tem certeza que deseja deletar sua conta? (s/n)? ')
            
            if confirmacao == 's':
                senha = input('Confirme sua senha: ')
                
                if senha == usuarios[email]['senha']:
                    del usuarios[email]
                    salvar_usuarios(dados)
                    print('Dados deletados com sucesso.')
                    break
                
                else:
                    print('Senha incorreta. Tente novamente.')
            
            elif confirmacao == 'n':
                print('Ok! Voltando para o menu.')
                break
            
            else:
                print('Opção inválida. Tente novamente.')

        elif email == 's':
            print('Ok! Saindo.')
            break
        else:
            print('Email não encontrado. Tente novamente.')
    return
     
def ver_dados():
    global usuario_logado
    
    email = usuario_logado.get('email')
    nome = usuario_logado.get('nome')
    idade = usuario_logado.get('idade')
    senha = usuario_logado.get('senha')
    estado = usuario_logado.get('estado')
    cidade = usuario_logado.get('cidade')

    while True:
        print(f'\nAqui estão os dados vinculados à {email}: ')
        print(f'Nome: {nome}')
        print(f'Idade: {idade}')
        print(f'Senha: {senha}')
        print(f'Estado: {estado}')
        print(f'Cidade: {cidade}')
        sair = input('Pressione a tecla Enter para sair')
        if sair == '':
            break
        else:
            print('Email não encontrado. Tente novamente.')

def atualizar_dados():
    dados = carregar_usuarios()
    usuarios = dados['usuarios']
    email = input('Digite seu email: ').lower().strip()
    if email in usuarios:
        senha = input('Digite sua senha: ')
        if usuarios[email]['senha'] == senha:
            while True:
                print(' --------------------------------- ')
                print('| Qual dado você deseja atualizar: |')
                print('| [1] Nome                         |')
                print('| [2] Idade                        |')
                print('| [3] Senha                        |')
                print('| [4] Estado                       |')
                print('| [5] Cidade                       |')
                print('| [6] Voltar                       |')
                print(' ---------------------------------- ')
                opcao = input('Escolha uma opção de 1 a 6: ')

                if opcao == '1':
                    novo_nome = input('Novo nome: ').title().strip()
                    if all(n.isalpha() or n.isspace() for n in novo_nome):
                        usuarios[email]["nome"] = novo_nome
                        salvar_usuarios(dados)
                        print('Dados atualizados com sucesso!')
                    else: 
                        print('Nome inválido. Utilize apenas letras.')

                elif opcao == '2':
                    nova_idade = input('Nova idade: ')
                    if nova_idade.isdigit():
                        usuarios[email]["idade"] = nova_idade
                        salvar_usuarios(dados)
                        print('Dados atualizados com sucesso!')
                    else:
                        print('Idade inválida. Utilize apenas números')

                elif opcao == '3':
                    nova_senha = input('Nova senha: ')
                    if len(nova_senha) == 6 and nova_senha.isdigit():
                        usuarios[email]["senha"] = nova_senha
                        salvar_usuarios(dados)
                        print('Dados atualizados com sucesso!')
                    else:
                        print('Senha inválida. A senha deve ter seis números.')

                elif opcao == '4':
                    novo_estado = input('Novo estado: ').upper()
                    if novo_estado in estados_validos:
                        usuarios[email]["estado"] = novo_estado
                        salvar_usuarios(dados)
                        print('Dados atualizados com sucesso!')
                    else:
                        print('Estado inválido. Digite apenas a sigla (ex.: PE)')

                elif opcao == '5':
                    nova_cidade = input('Nova cidade: ').title()
                    if all(c.isalpha() or c.isspace() for c in novo_nome):
                        usuarios[email]["cidade"] = nova_cidade
                        salvar_usuarios(dados)
                        print('Dados atualizados com sucesso!')
                    else:
                        print('Cidade inválida. Utilize apenas letras.')

                elif opcao == '6':
                    break
                
                else:
                    print('Opção inválida. Tente novamente.')
        else:
            print('Senha incorreta. Tente novamente.')
    else:
        print('Email não encontrado. Tente novamente')

# introdução
def menu_inicial():
    print('Bem-vindo ao Quarto de Leitura!')
    while True:
        opcao = input('Você tem uma conta? (s/n ou digite "sair" para sair) ').lower()
        if opcao == 'n':
            print('Então vamos criar uma conta para você!')
            cadastro()

        elif opcao == 's':
            login()
            menu_principal()
        elif opcao == 'sair':
            print('Até a próxima. Saindo...')
            break
        else:
            print('Opção inválida. Digite apenas "s", "n" ou "sair"')

def configuracoes():
    while True:
        print(' =-=-=-=-=-=-= Configurações =-=-=-=-=-=-= ')
        print('| [1] Ver dados                           |')
        print('| [2] Atualizar dados                     |')
        print('| [3] Deletar conta                       |')
        print('| [4] Voltar                              |')
        print(' -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ')
        opcao = input('Escolha uma das opções: ')

        if opcao == '1':
            ver_dados()

        elif opcao == '2':
            atualizar_dados()

        elif opcao == '3':
            deletar_conta()

        elif opcao == '4':
            limpar_terminal()
            break

        else: 
            print('Opção inválida. Digite apenas números de 1 a 4')

def estimativa_leitura():
    '''Faz estimativa baseada nos livros lidos pelo usuário'''
    global usuario_logado
    
    if not usuario_logado:
        print("Erro. Usuário não encontrado.")
        return
    
    livros_digitais = usuario_logado.get("livrosDigitais", 0)
    livros_fisicos = usuario_logado.get("livrosFisicos", 0)

    livros_digitais = int(livros_digitais)
    livros_fisicos = int(livros_fisicos)

    total_livros = livros_digitais + livros_fisicos
    while True: 
        if total_livros == 0:
            print('Você não leu nenhum livro esse ano.')
            sair = input('Pressione a tecla Enter para sair')
            if sair == '':
                break
        elif total_livros == 1:
            print(f'\nAo total você leu, nesse ano, {total_livros} livro.')
            print(f'Se você continuar nesse ritmo, nos próximos cinco anos você lerá {total_livros * 5} livros.\n')
            sair = input('Pressione a tecla Enter para sair')
            if sair == '':
                break
        else:
            print(f'\nParabéns, ao total você leu, nesse ano, {total_livros} livros.') 
            print(f'Se você continuar nesse ritmo, nos próximos cinco anos você lerá {total_livros * 5} livros.')
            sair = input('Pressione a tecla Enter para sair')
            if sair == '':
                break

def calcular_horas_estudo():
    global usuario_logado
    
    if not usuario_logado:
        print("Erro. Usuário não encontrado.")
        return

    h_livros_estudos = usuario_logado.get('horasEstudo', 0)
    h_livros_estudos = int(h_livros_estudos)
    dias_estudos =  h_livros_estudos * 52 // 24

    print(f'\nEsse ano você dedicará, em média, {h_livros_estudos * 52} horas aos estudos.')
    print(f'Isso significa que você vai passar, aproximadamente, {dias_estudos} dias inteiros estudando.')
    sair = input('Pressione a tecla Enter para sair')
    if sair == '':
       return

def calcular_horas_entretenimento():
    global usuario_logado
    
    if not usuario_logado:
        print("Erro. Usuário não encontrado.")
        return
    
    h_livros_entretenimento = usuario_logado.get('horasEntretenimento', 0)
    h_livros_entretenimento = int(h_livros_entretenimento)
    dias_leitura = h_livros_entretenimento * 52 // 24 

    print(f'Esse ano você também dedicará, em média, {h_livros_entretenimento * 52} horas à leitura.')
    print(f'Isso significa que você vai passar, aproximadamente, {dias_leitura} dias lendo.')
    sair = input('Pressione a tecla Enter para sair')
    if sair == '':
        return

def media_leitura():
    global usuario_logado

    if not usuario_logado:
        print("Erro. Usuário não encontrado.")
        return
    
    h_livros_estudos = usuario_logado.get('horasEstudo', 0)
    h_livros_entretenimento = usuario_logado.get('horasEntretenimento', 0)
    h_livros_estudos = int(h_livros_estudos)
    h_livros_entretenimento = int(h_livros_entretenimento)
    total_horas = (h_livros_entretenimento + h_livros_estudos) / 7

    print(f'Você leu, aproximadamente, {total_horas} horas por dia nessa semana. ')
    sair = input('Pressione a tecla Enter para sair')
    if sair == '':
        return

def recomendacao_livros():
    '''Recomenda um livro baseado na idade do usuário'''
    global usuario_logado

    if not usuario_logado:
        print("Erro. Usuário não encontrado.")
        return
    idade = usuario_logado.get('idade', 0)
    idade = int(idade)

    if idade <= 12:
        recomendacao = random.choice(livros_infantis)
        print(f'Baseado na sua idade, nós recomendamos o livro "{recomendacao}".')
        sair = input('Pressione a tecla Enter para sair')
        if sair == '':
            return
    elif 13 <= idade < 16:
        recomendacao = random.choice(livros_adolescentes)        
        print(f'Baseado na sua idade, nós recomendamos o livro "{recomendacao}".')
        sair = input('Pressione a tecla Enter para sair')
        if sair == '':
            return
    else:
        recomendacao = random.choice(livros_jovens)
        print(f'Baseado na sua idade, nós recomendamos o livro "{recomendacao}".')
        sair = input('Pressione a tecla Enter para sair')
        if sair == '':
            return

def menu_principal():
    while True:
        print(' ------------------------- Página inicial ------------------------- ')
        print('| [1] Quantos livros será que você vai ler nos próximos 5 anos?    |')
        print('| [2] Quantas horas por ano você lê por estudo?                    |')
        print('| [3] Quantas horas por ano você lê por diversão?                  |')
        print('| [4] Qual a sua média de leitura semanal?                         |')
        print('| [5] Sem ideia do que ler? Clica aqui!                            |')
        print('| [6] Configurações                                                |')
        print('| [7] Sair.                                                        |')
        print(' ------------------------------------------------------------------ ')
        opcao = input('Escolha uma das opções: ')

        if opcao == '1':
            estimativa_leitura()

        elif opcao == '2':
            calcular_horas_estudo()

        elif opcao == '3':
            calcular_horas_entretenimento()
        
        elif opcao == '4':
            media_leitura()
        
        elif opcao == '5':
            recomendacao_livros()

        elif opcao == '6':
            configuracoes()

        elif opcao == '7':
            limpar_terminal()
            print('Até a próxima! Saindo...')
            break 
        
        else:
            print('Opção inválida. Digite apenas números de 1 a 7.')

if __name__ == '__main__':
    menu_inicial()