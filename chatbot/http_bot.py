import requests

class HTTPBot:

    def reply(self,message):

        url="https://api.affiliateplus.xyz/api/chatbot"

        params={
            "message":message,
            "botname":"TestBot",
            "ownername":"User"
        }

        r=requests.get(url,params=params)

        data=r.json()

        return data["message"]