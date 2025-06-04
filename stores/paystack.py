# from django.conf import settings
# import requests

class Paystack:
    PAYTACK_SECRETS_KEY = settings.PAYTACK_SECRETS_KEY

    base_url = "https://api.paystack.co/"

    def verify_payment(self, ref, *args, **kwargs)
        path = f'transaction/verify{ref}'
        headers={
            "Authorization": f"bearer {self.PAYTACK_SECRETS_KEY}"
             "Content-Type":"application/json"
        }
        url = self.base_url+path
        response = requests.get(url,headers=headers)

        if requests.status_code == 200:
            response_data = response.json()
            if response_data.get("data"):
                return True, response_data["data"]
            else:
                return False, response_data.get("message", "verification failed")
        else:
            return False, response.json().get("message", "payment verification failed")



