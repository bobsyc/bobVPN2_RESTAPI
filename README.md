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

