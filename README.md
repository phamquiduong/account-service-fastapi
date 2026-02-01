### Install Docker
- Windows: https://docs.docker.com/desktop/setup/install/windows-install/
- MacOS: https://orbstack.dev/download
- Linux: https://docs.docker.com/desktop/setup/install/linux/

<br>

### Preparing
- Clone `docker/.env.example` to `docker/.env`

<br>

### Start server
- Change directory to `docker` folder
- Docker compose build and up in background
    ```bash
    docker compose up --build -d
    ```

<br>

### Result
- Access to http://localhost/docs to view API document
