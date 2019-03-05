# Alerts bot

Bot intended to track stock symbols and rise alarms when RSI reaches desired values.

## Build


### requirements

- qemu-user-static package installed.
- `{"experimental": true}` in `/etc/docker/daemon.json`


### commands

- amd64:
    ```bash
    docker build -t alerts-bot:latest .
    ```

- arm64:
    ```bash
    docker build --platform arm64  -t alerts-bot:arm64v8-latest -f Dockerfile.arm64 .
    ```
