from google.auth.transport import requests
from google.oauth2 import id_token


class Google(object):
    """
    Google class to fetch user information
    """

    @staticmethod
    def validate(auth_token):
        """queries the google OAuth2 api and returns user information"""
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            print(id_info)
            if id_info.get("iss") == "accounts.google.com":
                return id_info

        except:
            return "The token is either invalid or expired"
