# WELCOME

## Getting started
1. Install VS Code and Docker Desktop
1. Install Remote Development Extension for VS Code
1. Clone repo
1. Open in VS CODE, then you should see the following notification (Click Reopen in Container):
   <img src="https://github.com/factryflow/factryflow/assets/45033225/b6118dce-22ce-46c0-af51-6087535b6a7e" width="500">

1. Duplicate **```.env.template```** and rename it **```.env```** and add the secrets.
1. Then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select ```Dev Containers: Rebuild Container```
1. Then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and select ```Developer: Reload Window``` this will ensure that the extensions and formatters work properly. This only needs to be done after a container rebuild.

1. Run ```make migrate``` in terminal to migrate changes in the database.
1. Run ```make sync_roles``` in terminal to add user roles in the database.
2. Run ```make dev``` in terminal to run django.
