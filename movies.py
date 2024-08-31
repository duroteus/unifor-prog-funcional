MENSAGEM_MENU = "\nDigite:\n [a] para adicionar um filme,\n [l] para ver seus filmes,\n [b] para buscar um filme pelo título,\n [d] para buscar filmes por diretor,\n [e] para excluir um filme pelo ID,\n [s] para sair: "
filmes = []
proximo_id = 1 

# Função de alta ordem
def processar_filme(funcao):
    return funcao()

def adicionar_filme():
    global proximo_id
    
    try:
        titulo = input("Digite o título do filme: ").strip().title()
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("O título deve ser um texto não vazio.")
        
        diretor = input("Digite o nome do diretor: ").strip().title()
        if not isinstance(diretor, str) or not diretor.strip():
            raise ValueError("O nome do diretor deve ser um texto não vazio.")
                
        ano = input("Digite o ano de lançamento: ").strip()
        if not ano.isdigit():
            raise ValueError("O ano de lançamento deve ser um número.")
        
        for filme in filmes:
            if filme['titulo'] == titulo and filme['diretor'] == diretor and filme['ano'] == int(ano):
                print(f"Erro: O filme '{titulo}' dirigido por '{diretor}' em {ano} já está cadastrado.")
                return

        filmes.append({
            'id': proximo_id,
            'titulo': titulo,
            'diretor': diretor,
            'ano': int(ano) 
        })
        print("Filme adicionado com sucesso!")
        proximo_id += 1
    
    except ValueError as e:
        print(f"Erro ao adicionar filme: {e}")


def mostrar_filmes():
    # List comprehension
    filmes_formatados = [f"ID: {filme['id']},\n Título: {filme['titulo']},\n Diretor: {filme['diretor']},\n Ano: {filme['ano']}" for filme in filmes]
    for filme_formatado in filmes_formatados:
        print(filme_formatado)

def buscar_filme():
    titulo_busca = input("Digite o título do filme que você está procurando: ")

    # Função lambda para filtrar o filme pelo título
    filmes_encontrados = list(filter(lambda filme: filme['titulo'].lower() == titulo_busca.lower(), filmes))
    
    if filmes_encontrados:
        imprimir_filme(filmes_encontrados[0])
    else:
        print(f"Filme '{titulo_busca}' não encontrado.")

def imprimir_filme(filme):
    print(f"ID: {filme['id']}\n")
    print(f"Título: {filme['titulo']}\n")
    print(f"Diretor: {filme['diretor']}\n")
    print(f"Ano de lançamento: {filme['ano']}")

# Closure que gera uma função para encontrar filmes baseados no diretor
def buscar_por_diretor_closure(nome_diretor):
    def buscar_filme_por_diretor():
        filmes_encontrados = [filme for filme in filmes if filme['diretor'].lower() == nome_diretor.lower()]
        if filmes_encontrados:
            for filme in filmes_encontrados:
                imprimir_filme(filme)
        else:
            print(f"Nenhum filme encontrado para o diretor '{nome_diretor}'")
    return buscar_filme_por_diretor

def excluir_filme():
    if not filmes:
        print("Não há filmes cadastrados para excluir.")
        return

    mostrar_filmes()
    try:
        id_exclusao = int(input("Selecione o ID do filme que deseja excluir: "))
        filme_a_excluir = next((filme for filme in filmes if filme['id'] == id_exclusao), None)
        
        if filme_a_excluir:
            filmes.remove(filme_a_excluir)
            print(f"Filme com ID {id_exclusao} excluído com sucesso.")
        else:
            print(f"Nenhum filme encontrado com o ID {id_exclusao}.")
    
    except ValueError:
        print("Por favor, insira um ID válido.")

opcoes_usuario = {
    "a": lambda: processar_filme(adicionar_filme),  # Usando função de alta ordem aqui
    "l": lambda: processar_filme(mostrar_filmes),
    "b": lambda: processar_filme(buscar_filme),
    "d": lambda: processar_filme(buscar_por_diretor_closure(input("Digite o nome do diretor: "))),
    "e": lambda: processar_filme(excluir_filme),
}

def menu():
    selecao = input(MENSAGEM_MENU)
    while selecao != 's':
        if selecao in opcoes_usuario:
            funcao_selecionada = opcoes_usuario[selecao]
            funcao_selecionada()
        else:
            print('Comando desconhecido. Por favor, tente novamente.')

        selecao = input(MENSAGEM_MENU)

menu()
