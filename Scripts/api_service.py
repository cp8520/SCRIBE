import requests
from cryptography.fernet import Fernet

class ApiService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.authsvcendpoint = "https://reqres.in/api/login"  # Reqres endpoint
        self.key = Fernet.generate_key()  # Generate a new key for encryption
        self.cipher = Fernet(self.key)     # Create a cipher object

    def update_endpoint(api_service, new_endpoint):
        api_service.authsvcendpoint = new_endpoint
        print(f"Endpoint updated to: {api_service.authsvcendpoint}")

    def signed_in_check(self, e, username=None, password=None):
        u = username if username else "NA"
        p = "not blank" if password else "NA"

        if self.token:
            print(f"Attempting to do something with the data received\nusername saved: {self.username}\npassword saved: {self.password}")
            user_email = self.username  # Use the saved username as email
            user_details = self.make_authorized_request(email=user_email)
            # Update your UI with user_details here if applicable
        else:        
            print(f"Sign in attempted, username is {u} and password was {p}")
            self.username = u
            self.password = password
            self.authenticate()

    def authenticate(self):
        payload = {
            "email": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(self.authsvcendpoint, json=payload)
            if response.status_code == 200:
                token = response.json().get('token')
                self.token = self.cipher.encrypt(token.encode()).decode()  # Encrypt the token
                print(f"Authentication successful! Token (encrypted): {self.token}")
                self.get_headers()
            else:
                print(f"Failed to authenticate: {response.status_code} {response.text}")
        except Exception as ex:
            print(f"An error occurred during authentication: {ex}")

    def get_decrypted_token(self):
        if self.token:
            return self.cipher.decrypt(self.token.encode()).decode()  # Decrypt the token
        return None

    def get_headers(self):
        """Returns headers with the authentication token."""
        token = self.get_decrypted_token()
        if token:
            # print(f'Bearer decrypted {token}')
            return {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        
        else:
            return {
                'Content-Type': 'application/json'
            }

    def make_authorized_request(self, email=None, endpoint="https://reqres.in/api/users"):
        """Example of making a request with an authenticated token."""
        headers = self.get_headers()
        url = endpoint
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json().get('data', [])  # Get the user data list
                if email:
                    # Filter the users by email
                    user = next((user for user in data if user['email'] == email), None)
                    if user:
                        user_details = (
                            f"ID: {user['id']}, "
                            f"Email: {user['email']}, "
                            f"First Name: {user['first_name']}, "
                            f"Last Name: {user['last_name']}, "
                            f"Avatar: {user['avatar']}"
                        )
                        print(user_details)
                        return user_details
                    else:
                        print(f"No user found with email: {email}")
                        return None
                else:
                    print("Email not provided for filtering.")
                    return None
            else:
                print(f"Failed to retrieve data: {response.status_code} {response.text}")
                return None
        except Exception as ex:
            print(f"An error occurred during the request: {ex}")
            return None
