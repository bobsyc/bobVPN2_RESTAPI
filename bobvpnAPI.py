# https REST API for hosting on bobVPN servers to generate openvpn config files

from fastapi import FastAPI, HTTPException, status, Security
from fastapi.responses import FileResponse
from fastapi.security import APIKeyQuery
import os, subprocess

app = FastAPI()

# CONSTANTS
API_KEY = "BOBVPNISTHEBEST" 
configFolderPath = os.path.expanduser("~/ovpn-client-configs")
# END CONSTANTS

api_key_query = APIKeyQuery(name="api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
) -> str:
    # Verify the provided API key against the predefined API_KEY constant
    if api_key_query in API_KEY:
        return api_key_query
    # If the API key is invalid or missing, raise an HTTP 401 Unauthorized exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
)

@app.post("/generate_config")
async def generate_config(client_name: str, api_key: str = Security(get_api_key)):
    # Define the file path for the generated OpenVPN config file based on the client name
    config_file_path = f"{configFolderPath}/{client_name}.ovpn"
    if not os.path.exists(config_file_path):
        # If the config file does not exist, run the script to generate it
        subprocess.run(["./generate_config.sh", client_name, configFolderPath], check=True)
    
    # Return the generated config file as a FileResponse
    return FileResponse(config_file_path)
