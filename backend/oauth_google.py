from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import sys

# Define the scopes we need
# - gmail.readonly: read messages
# - gmail.modify:   trash, archive (remove INBOX label), mark read/unread, etc.
# - calendar:       if you still need it (optional)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'   # remove this line if you don't need calendar
]

# Path to your downloaded client secrets file from Google Cloud Console
CLIENT_SECRETS_FILE = "secrets/credentials.json"

def main():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES
        )

        # Use OOB (out-of-band) flow – still works for many personal accounts in 2026,
        # but deprecated; if it fails, switch to 'http://127.0.0.1'
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            prompt='consent',           # force consent screen every time
            access_type='offline'       # get refresh token
        )

        print("\nOpen this URL in your iPhone browser (Safari):\n")
        print(auth_url)
        print("\nAfter consenting, Google will show a code on the page.")
        print("Copy it exactly (no spaces or extra characters).\n")

        code = input("Paste the code Google gives you: ").strip()

        if not code:
            print("No code entered. Exiting.")
            sys.exit(1)

        # Exchange code for tokens
        flow.fetch_token(code=code)

        # Save credentials
        with open("secrets/token.pickle", "wb") as token_file:
            pickle.dump(flow.credentials, token_file)

        print("\n✅ Token saved successfully!")
        print("You can now run jarvis_operator.py – trash should work.")

    except Exception as e:
        print("\nError during authorization:")
        print(e)
        print("\nCommon fixes:")
        print("- Make sure CLIENT_SECRETS_FILE exists and has correct client_id/secret")
        print("- Check that your Google Cloud OAuth client allows this redirect_uri")
        print("- If 'invalid_grant' or 'malformed auth code': paste code immediately, no extra spaces")
        print("- If blocked: try adding your email as test user in Google Cloud Console → OAuth consent screen")

if __name__ == "__main__":
    main()