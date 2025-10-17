from flask import Flask, render_template, request, redirect, url_for, flash
import os, sys

# Garantir que a raiz do projeto esteja no sys.path quando o script for executado diretamente
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from python import db

app = Flask(__name__)
app.secret_key = 'troque_esta_chave_para_producao'

@app.route('/')
def index():
    try:
        receitas = db.list_receitas()
    except Exception as e:
        flash(f'Erro ao listar receitas: {e}', 'danger')
        receitas = []
    return render_template('list.html', receitas=receitas)


@app.route('/consultar')
def consultar():
    dificuldade = request.args.get('dificuldade')
    categoria = request.args.get('categoria')
    tempo_max = request.args.get('tempo_max')
    pessoas_min = request.args.get('pessoas_min')
    try:
        rows = db.list_receitas()
        # aplicar filtros simples
        def ok(r):
            if dificuldade and r['Dificuldade'] != dificuldade:
                return False
            if categoria and r['Categoria'] != categoria:
                return False
            if tempo_max and int(r['TempoPreparacao']) > int(tempo_max):
                return False
            if pessoas_min and int(r['NumPessoas']) < int(pessoas_min):
                return False
            return True
        receitas = [r for r in rows if ok(r)]
    except Exception as e:
        flash(f'Erro ao consultar: {e}', 'danger')
        receitas = []
    return render_template('consult.html', receitas=receitas)


@app.route('/gerir')
def gerir():
    try:
        receitas = db.list_receitas()
    except Exception as e:
        flash(f'Erro ao listar receitas: {e}', 'danger')
        receitas = []
    return render_template('gerir.html', receitas=receitas)

@app.route('/nova', methods=['GET', 'POST'])
def nova():
    if request.method == 'POST':
        nome = request.form.get('nome')
        dificuldade = request.form.get('dificuldade')
        tempo = request.form.get('tempo_preparacao')
        categoria = request.form.get('categoria')
        num = request.form.get('numero_de_pessoas')
        preparacao = request.form.get('preparacao')
        ingredientes_raw = request.form.get('ingredientes')
        ingredientes = []
        # ingredientes esperados no formato: nome|quantidade|unidade por linha
        if ingredientes_raw:
            for line in ingredientes_raw.splitlines():
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 3:
                    ingredientes.append({'nome': parts[0], 'quantidade': parts[1], 'unidade': parts[2]})

        receita = {
            'nome': nome,
            'dificuldade': dificuldade,
            'tempo_preparacao': tempo,
            'categoria': categoria,
            'numero_de_pessoas': num,
            'preparacao': preparacao,
            'ingredientes': ingredientes
        }
        try:
            db.insert_receita(receita)
            flash('Receita criada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao criar receita: {e}', 'danger')

    return render_template('form.html')


@app.route('/editar/<int:codigo>', methods=['GET', 'POST'])
def editar(codigo):
    if request.method == 'POST':
        nome = request.form.get('nome')
        dificuldade = request.form.get('dificuldade')
        tempo = request.form.get('tempo_preparacao')
        categoria = request.form.get('categoria')
        num = request.form.get('numero_de_pessoas')
        preparacao = request.form.get('preparacao')
        ingredientes_raw = request.form.get('ingredientes')
        ingredientes = []
        if ingredientes_raw:
            for line in ingredientes_raw.splitlines():
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 3:
                    ingredientes.append({'nome': parts[0], 'quantidade': parts[1], 'unidade': parts[2]})

        receita = {
            'nome': nome,
            'dificuldade': dificuldade,
            'tempo_preparacao': tempo,
            'categoria': categoria,
            'numero_de_pessoas': num,
            'preparacao': preparacao,
            'ingredientes': ingredientes
        }
        try:
            db.update_receita_full(codigo, receita)
            flash('Receita atualizada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao atualizar receita: {e}', 'danger')

    # GET: carregar receita e preencher o form
    receita = db.get_receita(codigo)
    if not receita:
        flash('Receita não encontrada', 'danger')
        return redirect(url_for('index'))
    # transformar ingredientes em texto para o textarea
    linhas = []
    for ing in receita.get('ingredientes', []):
        linhas.append(f"{ing['Ingrediente']}|{ing['Quantidade']}|{ing['Medida']}")
    ingredientes_text = "\n".join(linhas)
    return render_template('edit.html', receita=receita, ingredientes_text=ingredientes_text)


@app.route('/excluir/<int:codigo>', methods=['POST'])
def excluir(codigo):
    try:
        db.delete_receita(codigo)
        flash('Receita excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir receita: {e}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
