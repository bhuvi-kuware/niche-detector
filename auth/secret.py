from google.oauth2 import id_token
from google.auth.transport import requests

_CLIENT_ID = "380632208728-u3sci89kmmpshkp5c79hifpu850ga2i5.apps.googleusercontent.com"
_PROJECT_ID = "numeric-nova-409411"
class Secret: 

    def __init__(self,token):
        #Get ID from token
        self.id = self.validate_token_get_id(token)
        self.client = secretmanager.SecretManagerServiceClient()

    def validate_token_get_id(self, token): 
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), _CLIENT_ID)
            userid = idinfo['sub']
        except ValueError:
            pass

    def client_secrets_version(self):
        if self.does_secret_exist() is False:
            parent = f"projects/{_PROJECT_ID}"
            # Create the secret.
            self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": self.id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )

        parent = client.secret_path(_PROJECT_ID, self.id)
        payload_bytes = payload.encode("UTF-8")
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload_bytes)

        # Add the secret version.
        response = client.add_secret_version(
            request={
                "parent": parent,
                "payload": {
                    "data": payload_bytes,
                    "data_crc32c": int(crc32c.hexdigest(), 16),
                },
            }
        )

    def does_secret_exist(self):
        return False