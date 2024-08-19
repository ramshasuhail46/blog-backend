import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve the values from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET_ID")

# Encode the credentials
credential = f"{CLIENT_ID}:{SECRET}"
encoded_credential = base64.b64encode(
    credential.encode("utf-8")).decode("utf-8")

print(encoded_credential)
