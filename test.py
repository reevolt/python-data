import unittest
import aiofiles
import csv
import asyncio
from io import StringIO
from datetime import datetime
from main import ContractManager

class TestContractManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Crée des fichiers CSV temporaires pour les tests
        async with aiofiles.open('test_contrats.csv', mode='w', newline='') as file:
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=['nom_utilisateur', 'type_contrat', 'date_creation', 'date_modification', 'date_fin'])
            writer.writeheader()
            writer.writerows([
                {'nom_utilisateur': 'Jean Dupont', 'type_contrat': 'Assurance', 'date_creation': '2024-01-15', 'date_modification': '2024-02-01', 'date_fin': '2024-12-31'},
                {'nom_utilisateur': 'Alice Martin', 'type_contrat': 'Assurance', 'date_creation': '2024-01-10', 'date_modification': '2024-01-20', 'date_fin': '2024-06-30'},
                {'nom_utilisateur': 'Bob Durand', 'type_contrat': 'Emprunt', 'date_creation': '2024-03-01', 'date_modification': '2024-03-15', 'date_fin': '2024-01-01'},
                {'nom_utilisateur': 'Claire Lefevre', 'type_contrat': 'Santé', 'date_creation': '2024-02-20', 'date_modification': '2024-03-05', 'date_fin': '2025-01-01'},
                {'nom_utilisateur': 'David Bernard', 'type_contrat': 'Emprunt', 'date_creation': '2024-01-25', 'date_modification': '2024-02-10', 'date_fin': '2024-02-01'}
            ])
            await file.write(output.getvalue())

        async with aiofiles.open('test_users.csv', mode='w', newline='') as file:
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=['nom_utilisateur', 'actif'])
            writer.writeheader()
            writer.writerows([
                {'nom_utilisateur': 'Jean Dupont', 'actif': 'True'},
                {'nom_utilisateur': 'Alice Martin', 'actif': 'True'},
                {'nom_utilisateur': 'Bob Durand', 'actif': 'False'},
                {'nom_utilisateur': 'Claire Lefevre', 'actif': 'True'},
                {'nom_utilisateur': 'David Bernard', 'actif': 'False'}
            ])
            await file.write(output.getvalue())

    async def asyncTearDown(self):
        # Supprime les fichiers CSV temporaires après les tests
        import os
        os.remove('test_contrats.csv')
        os.remove('test_users.csv')

    async def test_verify_users_in_contrats(self):
        manager = ContractManager('test_contrats.csv')
        await manager.read_csv()
        active, inactive = await manager.verify_users_in_contrats('test_users.csv')

        self.assertEqual(active, ['Jean Dupont', 'Alice Martin', 'Bob Durand', 'Claire Lefevre', 'David Bernard'])
        self.assertEqual(inactive, [])

        # Vérifier la mise à jour des utilisateurs sans contrat ou dont les contrats sont expirés
        async with aiofiles.open('test_users.csv', mode='r') as file:
            content = await file.read()
            reader = csv.DictReader(StringIO(content))
            updated_users = [row for row in reader]

        # Vérifier les en-têtes
        self.assertEqual([key for key in updated_users[0].keys()], ['nom_utilisateur', 'actif'])

        # Vérifier les utilisateurs
        self.assertEqual(updated_users[0], {'nom_utilisateur': 'Jean Dupont', 'actif': 'True'})
        self.assertEqual(updated_users[1], {'nom_utilisateur': 'Alice Martin', 'actif': 'True'})
        self.assertEqual(updated_users[2], {'nom_utilisateur': 'Bob Durand', 'actif': 'True'})
        self.assertEqual(updated_users[3], {'nom_utilisateur': 'Claire Lefevre', 'actif': 'True'})
        self.assertEqual(updated_users[4], {'nom_utilisateur': 'David Bernard', 'actif': 'True'})

if __name__ == "__main__":
    unittest.main()
