# https REST API for hosting on bobVPN servers to generate openvpn config files

from fastapi import FastAPI, HTTPException, status, Security
from fastapi.responses import FileResponse
from fastapi.security import APIKeyQuery
import os, subprocess

app = FastAPI()

# CONSTANTS
API_KEY = "BOBVPNISTHEBEST" 
configFolderPath = "~/ovpn-client-configs"
# END CONSTANTS

api_key_query = APIKeyQuery(name="api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
) -> str:
    if api_key_query in API_KEY:
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
)

def generate_openvpn_config(client_name: str):
    subprocess.run(["./generate_config.sh", client_name])


@app.post("/generate_config")
async def generate_config(client_name: str, api_key: str = Security(get_api_key)):
    config_file_path = f"{configFolderPath}/{client_name}.ovpn"
    if not os.path.exists(config_file_path):
        generate_openvpn_config(client_name)
    
    return FileResponse(config_file_path, filename=f"{configFolderPath}/{client_name}.ovpn")

