import pickle
from google.oauth2.credentials import Credentials

with open("secrets/token.pickle", "rb") as f:
    creds = pickle.load(f)

print("Token scopes:", creds.scopes)
print("Has modify?", 'https://www.googleapis.com/auth/gmail.modify' in creds.scopes)
