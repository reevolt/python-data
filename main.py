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

    async def write_csv(self, file_name, rows, fieldnames):
        """Écrire le fichier CSV de manière asynchrone."""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        output.seek(0)
        async with aiofiles.open(file_name, mode='w', newline='') as file:
            await file.write(output.getvalue())

    async def get_contracts_by_user(self, user_name):
        """Retourne tous les contrats pour un utilisateur donné."""
        contracts = [row for row in self.data if row['nom_utilisateur'] == user_name]
        return contracts

    async def get_contracts_by_type(self, contract_type):
        """Retourne tous les contrats pour un type de contrat donné."""
        contracts = [row for row in self.data if row['type_contrat'] == contract_type]
        return contracts

    async def get_contracts_created_after(self, date):
        """Retourne tous les contrats créés après une date donnée."""
        contracts = []
        date = datetime.strptime(date, '%Y-%m-%d')
        for row in self.data:
            contract_date = datetime.strptime(row['date_creation'], '%Y-%m-%d')
            if contract_date > date:
                contracts.append(row)
        return contracts

    async def get_contracts_modified_before(self, date):
        """Retourne tous les contrats modifiés avant une date donnée."""
        contracts = []
        date = datetime.strptime(date, '%Y-%m-%d')
        for row in self.data:
            contract_date = datetime.strptime(row['date_modification'], '%Y-%m-%d')
            if contract_date < date:
                contracts.append(row)
        return contracts

    async def add_days_to_date(self, date, days):
        """Ajoute un nombre de jours à une date donnée."""
        date = datetime.strptime(date, '%Y-%m-%d')
        new_date = date + timedelta(days=days)
        return new_date.strftime('%Y-%m-%d')

    # TODO
    # async def subtract_days_from_date(self, date, days):
    #     """Soustrait un nombre de jours à une date donnée."""
    #     date = datetime.strptime(date, '%Y-%m-%d')
    #     new_date = date - timedelta(days=days)
    #     return new_date.strftime('%Y-%m-%d')

    async def get_difference_in_days(self, date1, date2):
        """Retourne la différence en jours entre deux dates."""
        date1 = datetime.strptime(date1, '%Y-%m-%d')
        date2 = datetime.strptime(date2, '%Y-%m-%d')
        return (date1 - date2).days

    async def is_date_within_range(self, date, start_date, end_date):
        """Vérifie si une date se trouve dans un intervalle de dates."""
        date = datetime.strptime(date, '%Y-%m-%d')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return start_date <= date <= end_date

    async def verify_users_in_contrats(self, users_csv_file):
        """Vérifie si chaque utilisateur dans le fichier users.csv a des contrats valides dans le fichier des contrats.
        Modifie le statut à inactif si l'utilisateur n'a pas de contrat ou si tous les contrats sont expirés."""
        users = []
        async with aiofiles.open(users_csv_file, mode='r') as file:
            content = await file.read()
            reader = csv.DictReader(StringIO(content))
            users = [row for row in reader]

        user_dict = {user['nom_utilisateur']: user for user in users}
        username_end_date_dict = {}

        for row in self.data:
            user_name = row['nom_utilisateur']
            end_date = row['date_fin']
            username_end_date_dict[user_name] = end_date

        active_users = []
        inactive_users = []

        for user in users:
            user_name = user['nom_utilisateur']
            if user_name in username_end_date_dict:
                user['actif'] = 'True'
                active_users.append(user_name)
            else:
                # user n'a pas de contrats
                user['actif'] = 'False'
                inactive_users.append(user_name)

        # Écriture des modifications dans le fichier
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=['nom_utilisateur', 'actif'])
        writer.writeheader()
        writer.writerows(users)
        async with aiofiles.open(users_csv_file, mode='w', newline='') as file:
            await file.write(output.getvalue())

        return active_users, inactive_users


# Exemple d'utilisation :
async def main():
    manager = ContractManager('contrats.csv')
    await manager.read_csv()
    print(await manager.get_contracts_by_user('Jean Dupont'))
    active, inactive = await manager.verify_users_in_contrats('users.csv')
    print("Users active:", active)
    print("Users not active or not active:", inactive)


if __name__ == "__main__":
    asyncio.run(main())
