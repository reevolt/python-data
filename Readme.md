# Python practice

## How to

1. Install dependencies
2. Run the project
3. Ensure it's working

## Exercices

### Context

- We have a database containing contrats in contrats.csv and another one with clients in clients.csv
- Every day, manually, this code updates the clients database based on the contrats and clients databases.
- If a client has a contrat in contrats.csv then he is active, inactive otherwise.
- We want to industrialize this code that is the latest version and is working.
- Before that we want to check if the code is ready to be industrialized.

### TODO

* Focus on the main.py file
  * Give us a code review of the function `verify_clients_in_contrats`
  * Need to refactor something in this function ? 
* Can you give us a general code review of the project ?
* Need to refactor something?
* Feature : desactive client with ended contrat
  * Implement a feature that desactives a client whose contrat date has ended (compared to the present time).
  * How can you validate your work ?