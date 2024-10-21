import requests

class TicketHandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def obter_tickets_por_ids(self, ticket_ids):
        """Busca tickets pela API do Movidesk, com base nos IDs fornecidos."""
        ids_lista = [ticket_id.strip() for ticket_id in ticket_ids.split(',')]
        filtro = ' or '.join([f"id eq {ticket_id}" for ticket_id in ids_lista])

        params = {
            'token': self.api_key,
            '$select': 'id,subject,status,createdDate,actions',
            '$expand': 'actions($select=id,type,description,createdDate),clients($expand=organization($select=businessName))',
            '$filter': filtro
        }

        try:
            response = requests.get('https://api.movidesk.com/public/v1/tickets', params=params)
            if response.status_code == 200:
                tickets = response.json()
                print(f"{len(tickets)} tickets encontrados.")
                return tickets
            else:
                print(f"Erro: {response.status_code} - {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Erro na conexão: {e}")
            return []
