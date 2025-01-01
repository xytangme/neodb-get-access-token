import requests
from urllib.parse import urlencode

class NeoDBAuth:
    def __init__(self, client_id, client_secret, redirect_uri=None, base_url="https://neodb.social"):
        """
        Initialize with the credentials you get after registering your application
        
        Args:
            client_id (str): Your application's client ID
            client_secret (str): Your application's client secret
            redirect_uri (str, optional): The callback URL or None to use OOB flow
            base_url (str, optional): Base URL for NeoDB API (default: https://neodb.social)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri or "urn:ietf:wg:oauth:2.0:oob"
        self.base_url = base_url
    
    def create_application(self, client_name, website=None):
        """
        Create a new application and get credentials
        
        Args:
            client_name (str): Name of your application
            website (str, optional): Your application's website
            
        Returns:
            dict: Application credentials including client_id and client_secret
        """
        url = f"{self.base_url}/api/v1/apps"
        data = {
            "client_name": client_name,
            "redirect_uris": self.redirect_uri,
        }
        if website:
            data["website"] = website
            
        response = requests.post(url, data=data)
        return response.json()
    
    def get_authorization_url(self):
        """
        Generate the URL where users need to go to authorize your application
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri
        }
        
        auth_url = f"{self.base_url}/oauth/authorize?{urlencode(params)}"
        return auth_url
    
    def get_access_token(self, auth_code):
        """
        Exchange the authorization code for an access token
        
        Args:
            auth_code (str): The authorization code received after user grants permission
            
        Returns:
            dict: The response containing the access token and other details
        """
        token_url = f"{self.base_url}/oauth/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(token_url, data=data)
        return response.json()
    
    def make_authenticated_request(self, access_token, endpoint):
        """
        Make an authenticated request to the API
        
        Args:
            access_token (str): The access token obtained from get_access_token
            endpoint (str): The API endpoint to call (e.g., '/api/me')
            
        Returns:
            dict: The API response
        """
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers)
        return response.json()

# Example usage:
def main():
    # Example 1: Creating a new application (using default base_url)
    neodb = NeoDBAuth(None, None)  # No credentials yet, using default base_url
    app_info = neodb.create_application("MyTestApp")
    print("New application created:")
    print(f"Client ID: {app_info['client_id']}")
    print(f"Client Secret: {app_info['client_secret']}")
    
    # Now initialize with the new credentials
    neodb = NeoDBAuth(
        client_id=app_info['client_id'],
        client_secret=app_info['client_secret']
        # No redirect_uri - will use OOB flow
    )
    
    # Get the authorization URL
    auth_url = neodb.get_authorization_url()
    print("\nPlease visit this URL to authorize the application:")
    print(auth_url)
    print("\nSince we're using OOB flow, the authorization code will be displayed on the page.")
    
    # Get the authorization code from user
    auth_code = input("\nEnter the authorization code shown: ")
    
    # Exchange the code for an access token
    token_response = neodb.get_access_token(auth_code)
    access_token = token_response['access_token']
    print("\nAccess token obtained:", access_token)
    
    # Make an authenticated API request
    user_info = neodb.make_authenticated_request(access_token, '/api/me')
    print("\nUser info:", user_info)

if __name__ == "__main__":
    main()
