### How I deployed on my Ubuntu server


**Set up NGINX + Firewall rules**
1. `apt install nginx`
2. `vim /etc/nginx/sites-enabled/fastapi_nginx`

```
server {
        listen 80;
        server_name MYSERVERIP;
        location / {
                proxy_pass http://127.0.0.1:8003;
        }
}
```           

3. `sudo ufw allow 'Nginx HTTP'`
4. `sudo ufw enable`
5. `sudo service nginx restart`

**Prep the config database directory**
1. `mkdir ~/ovpn-client-configs/`

**Start the API service**
1. `sudo chmod +x ./generate_config`
2. `uvicorn bobvpnAPI:app --port 8003`

## API Reference

### Generate Config [POST]

Generates an OpenVPN config file for a client.

- **URL**: `/generate_config`
- **Method**: `POST`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer {api-key}`
- **Parameters**:
  - `client_name` (string): The name of the client for whom to generate the config file.
- **Response**:
  - **200 OK**:
    - Content-Type: application/octet-stream
    - Body: The generated OpenVPN config file.
  - **401 Unauthorized**:
    - Body: Invalid or missing API Key.

#### Example

```http
POST /generate_config HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer BOBVPNISTHEBEST

{
  "client_name": "john_doe"
}

Response:
```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="john_doe.ovpn"

<contents of the generated OpenVPN config file>
```

or

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Invalid or missing API Key"
}
```
