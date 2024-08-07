import asyncio
import csv
from datetime import datetime, timedelta
from io import StringIO

import aiofiles


class ContractManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []

    async def read_csv(self):
        """Lire le fichier CSV de manière asynchrone."""
        async with aiofiles.open(self.csv_file, mode='r') as file:
            content = await file.read()
            reader = csv.DictReader(StringIO(content))
            self.data = [row for row in reader]

    async def get_contracts_by_client(self, client_name):
        """Retourne tous les contrats pour un client donné."""
        contracts = [row for row in self.data if row['nom_client'] == client_name]
        return contracts

    # TODO
    # async def subtract_days_from_date(self, date, days):
    #     """Soustrait un nombre de jours à une date donnée."""
    #     date = datetime.strptime(date, '%Y-%m-%d')
    #     new_date = date - timedelta(days=days)
    #     return new_date.strftime('%Y-%m-%d')

    async def add_days_to_date(self, date, days):
        """Ajoute un nombre de jours à une date donnée."""
        date = datetime.strptime(date, '%Y-%m-%d')
        new_date = date + timedelta(days=days)
        return new_date.strftime('%Y-%m-%d')

    async def is_date_within_range(self, date, start_date, end_date):
        """Vérifie si une date se trouve dans un intervalle de dates."""
        date = datetime.strptime(date, '%Y-%m-%d')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return start_date <= date <= end_date

    async def verify_clients_in_contrats(self, clients_csv_file):
        """Vérifie si chaque client dans le fichier clients.csv a des contrats valides dans le fichier des contrats.
        Modifie le statut à inactif si l'utilisateur n'a pas de contrat ou si tous les contrats sont expirés."""
        clients = []
        async with aiofiles.open(clients_csv_file, mode='r') as file:
            content = await file.read()
            reader = csv.DictReader(StringIO(content))
            clients = [row for row in reader]

        client_dict = {client['nom_client']: client for client in clients}
        clientname_end_date_dict = {}

        for row in self.data:
            client_name = row['nom_client']
            end_date = row['date_fin']
            clientname_end_date_dict[client_name] = end_date

        active_clients = []
        inactive_clients = []

        # Boucle sur la liste des clients
        for client in clients:
            client_name = client['nom_client']
            if client_name in clientname_end_date_dict:
                client['actif'] = 'True'
                active_clients.append(client_name)
            else:
                # client n'a pas de contrats
                client['actif'] = 'False'
                inactive_clients.append(client_name)

        # Écriture des modifications dans le fichier
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=['nom_client', 'actif'])
        writer.writeheader()
        writer.writerows(clients)
        async with aiofiles.open(clients_csv_file, mode='w', newline='') as file:
            await file.write(output.getvalue())

        return active_clients, inactive_clients


# Exemple d'utilisation :
async def main():
    manager = ContractManager('contrats.csv')
    await manager.read_csv()
    print(await manager.get_contracts_by_client('Jean Dupont'))
    active, inactive = await manager.verify_clients_in_contrats('clients.csv')
    print("Clients active:", active)
    print("clients not active or not active:", inactive)


if __name__ == "__main__":
    asyncio.run(main())
