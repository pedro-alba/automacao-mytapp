import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados MySQL
DB_HOST = "localhost"
DB_NAME = "automacao_diario"
DB_USER = "thales"
DB_PASS = "141452"

def get_db_connection():
    """Função para conectar ao banco de dados MySQL."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Rota inicial - Página principal para escolher a data e exibir os tickets
@app.route('/')
def index():
    usuario = request.args.get('usuario', 'default_user')
    data = request.args.get('data', datetime.now().strftime("%Y-%m-%d"))
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar tickets do usuário para a data selecionada
    cursor.execute("SELECT ticket_id, acao, criticidade, blip FROM tickets_diarios WHERE usuario = %s AND data = %s", (usuario, data))
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', tickets=tickets, data=data, usuario=usuario)

# Rota para buscar tickets e salvar no banco de dados
@app.route('/buscar_tickets', methods=['POST'])
def buscar_tickets():
    ticket_ids = request.form['ticket_ids']
    comentarios = request.form['comentarios']
    criticidade = request.form['criticidade']
    blip = request.form['blip']
    usuario = request.args.get('usuario', 'default_user')

    if ticket_ids and comentarios and criticidade and blip:
        # Aqui você chama a classe TicketHandler para buscar e salvar os tickets
        ticket_handler = TicketHandler(api_key="c373bc42-3049-4411-9727-94975d2b9fc0")
        tickets = ticket_handler.obter_tickets_por_ids(ticket_ids)  # Busca tickets usando a API
        salvar_acoes_no_banco(tickets, usuario, criticidade, blip)  # Salva as ações no banco de dados

        return redirect(url_for('index', usuario=usuario))
    else:
        return "Por favor, preencha todos os campos (IDs, Comentários, Criticidade, Blip).", 400

# Função para salvar tickets no banco de dados MySQL
def salvar_acoes_no_banco(tickets, usuario, criticidade, blip):
    """Salva as ações dos tickets no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    data_atual = datetime.now().strftime("%Y-%m-%d")
    for ticket in tickets:
        ticket_id = ticket['id']
        descricao_acao = ticket.get('actions', [{}])[-1].get('description', 'Sem descrição')
        cursor.execute(
            "INSERT INTO tickets_diarios (ticket_id, usuario, data, acao, criticidade, blip) VALUES (%s, %s, %s, %s, %s, %s)",
            (ticket_id, usuario, data_atual, descricao_acao, criticidade, blip)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Ações salvas no banco de dados.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
