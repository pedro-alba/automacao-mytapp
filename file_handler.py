import csv
import os
from datetime import datetime

class FileHandlerCSV:
    def __init__(self, caminho_destino):
        self.caminho_destino = caminho_destino

    def salvar_acoes_csv(self, tickets, usuario):
        """Salva as ações de tickets em um arquivo CSV, separando por data e usuário."""
        data_atual = datetime.now().strftime("%d-%m-%Y")
        nome_arquivo = os.path.join(self.caminho_destino, f"diario_{usuario}.csv")

        # Se o arquivo não existir, criamos o cabeçalho
        arquivo_existe = os.path.exists(nome_arquivo)

        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            if not arquivo_existe:
                # Escreve o cabeçalho do CSV
                writer.writerow(["ID do Ticket", "Usuário", "Data", "Ação"])

            for ticket in tickets:
                ticket_id = ticket['id']
                descricao_acao = ticket.get('actions', [{}])[-1].get('description', 'Sem descrição')
                writer.writerow([ticket_id, usuario, data_atual, descricao_acao])

        print(f"Ações salvas no arquivo CSV '{nome_arquivo}'")
