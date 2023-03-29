import requests

# Define API endpoints
AUTH_URL = "https://login.live.com/oauth20_token.srf"
CHECK_GAMERTAG_ENDPOINT = "https://xsts.auth.xboxlive.com/xsts/authorize"
CLAIM_GAMERTAG_ENDPOINT = "https://gamertag.xboxlive.com/gamertags"

# Define authentication parameters
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
SCOPE = "XboxLive.signin XboxLive.offline_access"
GRANT_TYPE = "client_credentials"

# Define gamertags to claim
gamertags_to_claim = ["GamerTag1", "GamerTag2", "GamerTag3"]

# Get OAuth token
auth_response = requests.post(AUTH_URL, data={
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": SCOPE,
    "grant_type": GRANT_TYPE
}).json()
oauth_token = auth_response["access_token"]

# Function to check if a gamertag is available
def check_gamertag(gamertag):
    headers = {"Authorization": f"Bearer {oauth_token}"}
    params = {"assertion": f"{{\"xboxLiveContext\":{{\"isHeld\":false,\"gamertag\":\"{gamertag}\"}}}}"}

    response = requests.get(CHECK_GAMERTAG_ENDPOINT, headers=headers, params=params)
    return response.status_code == 200

# Function to claim a gamertag
def claim_gamertag(gamertag):
    headers = {"Authorization": f"Bearer {oauth_token}"}
    data = {"gamertag": gamertag}

    response = requests.post(CLAIM_GAMERTAG_ENDPOINT, headers=headers, json=data)
    return response.status_code == 200

# Loop through gamertags and claim them if available
for gamertag in gamertags_to_claim:
    if check_gamertag(gamertag):
        if claim_gamertag(gamertag):
            print(f"Successfully claimed gamertag: {gamertag}")
        else:
            print(f"Failed to claim gamertag: {gamertag}")
    else:
        print(f"Gamertag not available: {gamertag}")
