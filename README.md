# WELCOME

## Getting started
1. Install VS Code and Docker Desktop
1. Install Remote Development Extension for VS Code
1. Clone repo
1. Open in VS CODE, then you should see the following notification (Click Reopen in Container):
   <img src="https://github.com/factryflow/factryflow/assets/45033225/b6118dce-22ce-46c0-af51-6087535b6a7e" width="500">



## Development setup

1. Duplicate **```.env.template```** and rename it **```.env```** and add the secrets.
2. Then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select ```Dev Containers: Rebuild Container```
3. Then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select ```Developer: Reload Window``` this will ensure that the extensions and formatters work properly. This only needs to be done after a container rebuild.

1. Run ```make migrations``` in terminal to create new migratrions.
1. Run ```make migrate``` in terminal to migrate changes in the database.
2. Run ```make sync_roles``` in terminal to add user roles in the database.
3. Run ```make dev``` in terminal to run django.


## Production

1. Duplicate ```.env.template``` and rename it to ```.env```, then add the necessary secrets. Ensure that the value of the ```DJANGO_ENV``` environment variable is set to ```production```.
1. Run ```docker compose up --build``` in terminal to build the container and to run the server


SQLite database is set up for development purposes, while PostgreSQL is used for the production environment.


