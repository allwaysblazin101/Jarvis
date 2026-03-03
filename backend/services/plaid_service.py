import os
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid import ApiClient, Configuration
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

load_dotenv()

class PlaidService:
    def __init__(self):
        env = os.getenv("PLAID_ENV", "sandbox")
        client_id = os.getenv("PLAID_CLIENT_ID")
        secret = os.getenv("PLAID_SECRET")
        self.access_token = os.getenv("PLAID_ACCESS_TOKEN")

        configuration = Configuration(
            host=f"https://{env}.plaid.com",
            api_key={
                'clientId': client_id,
                'secret': secret,
            }
        )
        self.api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(self.api_client)

    def get_balances(self):
        if not self.access_token:
            return {"error": "No access token set in .env"}

        try:
            request = AccountsBalanceGetRequest(access_token=self.access_token)
            response = self.client.accounts_balance_get(request)
            accounts = response['accounts']
            balances = {}
            for acc in accounts:
                name = acc['name']
                current = acc['balances']['current']
                available = acc['balances'].get('available', current)
                balances[name] = {"current": current, "available": available}
            return balances
        except Exception as e:
            return {"error": str(e)}
