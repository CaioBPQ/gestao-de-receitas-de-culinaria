from db import insert_receita, list_receitas, get_receita, update_receita, delete_receita

# lista todas as receitas
# lista receitas por dificuldade
# lista receitas por categorias
# lista receitas por tempo de preparação


# dificuldades ( muito fácil, fácil, moderado, difícil, muito difícil)
# categoria ( entrada, sopa, carne, peixe , marisco, massa, molho e tempero, salada e sobremesa)
# medida ( quilograma, decigrama, grama, litro, decilitro, milillitro e unidade)]

dificuldades = ["muito fácil", "fácil", "moderado", "difícil", "muito difícil"]
categorias = ["entrada", "sopa", "carne", "peixe", "marisco", "massa", "molho e tempero", "salada", "sobremesa"]
medidas = ["quilograma", "decigrama", "grama", "litro", "decilitro", "mililitro", "unidade"]

def menu_inicial():
    print("Bem-vindo ao Gerneciador de Receitas!")
    print("Escolha uma opção:")
    print("1. novas receitas")
    print("2. consultar receitas")
    print("3. gerir receitas")
    print("4. sair")
    
    escolha = input("Digite o número da opção desejada: ")
    return escolha
    
def novas_receitas():
        print("Opção para adicionar novas receitas selecionada.")
        print("_" * 40)

        nome_receita = input("Digite o nome da receita: ")
        print("_" * 40)

        dificuldades_receitas = input (f"escolha a dificuldade:\n{dificuldades}:\n")
        if dificuldades_receitas not in dificuldades:
            print(f"Dificuldade inválida. tente novamente")
            while dificuldades_receitas not in dificuldades:
                dificuldades_receitas = input (f"escolha a dificuldade:\n{dificuldades}:\n")
        print("_" * 40)

        tempo_preparacao = input("Digite o tempo de preparação (em minutos): ")
        print("_" * 40)

        categoria_receita = input (f"qual categoria seu prato representa:\n{categorias}:\n")
        if categoria_receita not in categorias:
            print(f"categotria inválida. tente novamente")
            while categoria_receita not in categorias:
                categoria_receita = input (f"escolha a categoria:\n{categorias}:\n")
        print("_" * 40)

        numero_de_pessosas = input("Digite o número de pessoas que a receita serve: ")
        print("_" * 40)

        preparacao = input("Digite o modo de preparação da receita: ")
        print("_" * 40)

        quantos_ingredientes = input("Digite o número de ingredientes necessários: ")
        ingredientes = []
        if quantos_ingredientes.isdigit():
          for i in range(int(quantos_ingredientes)):
            ingrediente = input(f"Digite o nome do ingrediente {i+1}: ")
            quantidade = input(f"Digite a quantidade do ingrediente {i+1}: ")
            if quantidade.replace('.','',1).isdigit() == False:
                print(f"Quantidade inválida. tente novamente")
                while quantidade.replace('.','',1).isdigit() == False:
                    quantidade = input(f"Digite a quantidade do ingrediente {i+1}: ")
            unidade = input(f"Digite a unidade de medida do ingrediente {i+1} (ex:{medidas}): ")
            if unidade not in medidas:
                print(f"Unidade inválida. tente novamente")
                while unidade not in medidas:
                    unidade = input(f"Digite a unidade de medida do ingrediente {i+1} (ex:{medidas}): ")
            
            ingredientes.append({
                "nome": ingrediente,
                "quantidade": quantidade,
                "unidade": unidade
            })
            print(f"Ingrediente {i+1}: {quantidade} {unidade} de {ingrediente}")
        print("_" * 40)
        receita = {
            "nome": nome_receita,
            "dificuldade": dificuldades_receitas,
            "tempo_preparacao": tempo_preparacao,
            "categoria": categoria_receita,
            "numero_de_pessoas": numero_de_pessosas,
            "preparacao": preparacao,
            "ingredientes": ingredientes
        }
        try:
            receita_id = insert_receita(receita)
            print(f"Receita adicionada com sucesso! ID: {receita_id}")
        except Exception as e:
            print(f"Erro ao adicionar receita: {e}")
        print("_" * 40)

def consultar_receitas():
  print("Opção para consultar receitas selecionada.")
  print("_" * 40)
  print("1. Listar todas as receitas")
  print("2. Listar receitas por dificuldade")
  print("3. Listar receitas por categoria")
  print("4. Listar receitas por tempo de preparação")
  print("5. numero de pessoas servidas pela receita")
  
  escolha_consulta = input("Digite o número da opção desejada: ")
  print("_" * 40)
  if escolha_consulta == "1":
        print("Listando todas as receitas...")
        try:
            rows = list_receitas()
            if not rows:
                print("Nenhuma receita cadastrada no banco de dados.")
            else:
                for r in rows:
                    print(f"{r['CodigoReceita']}. {r['Nome']} - {r['Categoria']} - {r['Dificuldade']} (Tempo: {r['TempoPreparacao']} min | Serve: {r['NumPessoas']})")
        except Exception as e:
            print(f"Erro ao listar receitas: {e}")
  
  elif escolha_consulta == "2":
    dificuldade_filtro = input(f"Escolha a dificuldade para filtrar:\n{dificuldades}:\n")
    print(f"Listando receitas com dificuldade: {dificuldade_filtro}...")
    
  elif escolha_consulta == "3":
    categoria_filtro = input(f"Escolha a categoria para filtrar:\n{categorias}:\n")
    print(f"Listando receitas na categoria: {categoria_filtro}...")
    
  elif escolha_consulta == "4":
    tempo_filtro = input("Digite o tempo máximo de preparação (em minutos): ")
    print(f"Listando receitas com tempo de preparação até {tempo_filtro} minutos...")
    
  elif escolha_consulta == "5":
    pessoas_filtro = input("Digite o número mínimo de pessoas que a receita deve servir: ")
    print(f"Listando receitas que servem pelo menos {pessoas_filtro} pessoas...")
    
  else:
    print("Opção inválida. Retornando ao menu principal.")
    
def gerir_receitas():
    print("Opção para gerir receitas selecionada.")
    print("_" * 40)
    print("1. Editar uma receita")
    print("2. Excluir uma receita")

    escolha_gerir = input("Digite o número da opção desejada: ")
    print("_" * 40)

    if escolha_gerir == "1":
        print("Editando uma receita...")
        try:
            rows = list_receitas()
            if not rows:
                print("Nenhuma receita para editar.")
                return
            for r in rows:
                print(f"{r['CodigoReceita']}. {r['Nome']}")
            escolha_codigo = input("Digite o CodigoReceita da receita que deseja editar: ")
            if not escolha_codigo.isdigit():
                print("Código inválido.")
                return
            receita = get_receita(int(escolha_codigo))
            if not receita:
                print("Receita não encontrada.")
                return
            oque_editar = input("O que você gostaria de editar? (nome, dificuldade, tempo_preparacao, categoria, numero_de_pessoas, preparacao): ")
            if oque_editar in ['nome', 'dificuldade', 'tempo_preparacao', 'categoria', 'numero_de_pessoas', 'preparacao']:
                novo_valor = input(f"Digite o novo valor para {oque_editar}: ")
                update_receita(receita['CodigoReceita'], oque_editar, novo_valor)
                print(f"{oque_editar} atualizado com sucesso!")
            else:
                print("Campo inválido.")
        except Exception as e:
            print(f"Erro ao editar receita: {e}")

    elif escolha_gerir == "2":
        print("Excluir uma receita...")
        try:
            rows = list_receitas()
            if not rows:
                print("Nenhuma receita para excluir.")
                return
            for r in rows:
                print(f"{r['CodigoReceita']}. {r['Nome']}")
            escolha_codigo = input("Digite o CodigoReceita da receita que deseja excluir: ")
            if not escolha_codigo.isdigit():
                print("Código inválido.")
                return
            receita = get_receita(int(escolha_codigo))
            if not receita:
                print("Receita não encontrada.")
                return
            confirmar = input(f"Tem certeza que deseja excluir '{receita['Nome']}'? (sim/não): ")
            if confirmar.lower() == "sim":
                delete_receita(receita['CodigoReceita'])
                print("Receita excluída com sucesso!")
            else:
                print("Exclusão cancelada.")
        except Exception as e:
            print(f"Erro ao excluir receita: {e}")

    else:
        print("Opção inválida. Retornando ao menu principal.")

def run():
    while True:
      escolha = menu_inicial()
      
      if escolha == "1":
          novas_receitas()
          
      elif escolha == "2":
          consultar_receitas()
          
      elif escolha == "3":
          gerir_receitas()
          
      elif escolha == "4":
          print("Saindo do Gerenciador de Receitas. Até logo!")
          break
          
      else:
          print("Opção inválida. Por favor, tente novamente.")
