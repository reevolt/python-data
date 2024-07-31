# Python practice

## How to

1. Install dependencies
2. Run the project
3. Ensure it's working

## Exercices

### Context

- We have a database containing contrats in contrats.csv and another one with clients in users.csv
- Every day, manually, this code updates the users database based on the contrats and users databases.
- If a user has a contrat in contrats.csv then he is active, inactive otherwise.
- We want to industrialize this code that is the latest version and is working.
- Before that we want to check if the code is ready to be industrialized.

### TODO

1. Focus on the main.py file
2. Can you give us a code review ?
3. Need to refactor something?
4. Feature : desactive user with ended contrat
4.1. Implement a feature that desactives a user whose contrat date has ended (compared to the present time).
4.2. How can you validate your work ?