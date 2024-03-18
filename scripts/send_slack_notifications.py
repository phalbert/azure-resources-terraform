import logging
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortClient:
    def __init__(self, client_id: str, client_secret: str):
        self.api_url = "https://api.getport.io"
        self.access_token = self.get_token(client_id, client_secret)
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "port-message-service",
        }

    def get_token(self, client_id, client_secret):
        credentials = {"clientId": client_id, "clientSecret": client_secret}
        token_response = requests.post(
            f"{self.api_url}/v1/auth/access_token", json=credentials
        )
        token_response.raise_for_status()
        return token_response.json()["accessToken"]

    def search_entities(self, query):
        search_req = requests.post(
            f"{self.api_url}/v1/entities/search",
            json=query,
            headers=self.headers,
            params={},
        )
        search_req.raise_for_status()
        return search_req.json()["entities"]


def send_notification(entity, message, api):
    title = entity["title"]
    slack_webhook = entity["properties"].get("slack")

    if slack_webhook:
        payload = {
            # "text": f"Hello {title}! {message}. {api} team.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Hi _*{title.lower()}*_ team! :wave: We've made an update to the *{api}*:",
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":white_large_square: *Details* \n{message}.",
                    },
                },
            ],
        }
        requests.post(slack_webhook, json=payload)
    else:
        print(f"No Slack webhook found for: {title}")


if __name__ == "__main__":
    port_client_id = os.environ.get("PORT_CLIENT_ID")
    port_client_secret = os.environ.get("PORT_CLIENT_SECRET")
    message = os.environ.get("MESSAGE")
    sending_api = os.environ.get("SENDING_API")

    print("Initializing Port client", port_client_id, port_client_secret)
    port_client = PortClient(port_client_id, port_client_secret)

    logger.info(f"Fetching entities for query: sending_api {sending_api},")
    search_query = {
        "combinator": "and",
        "rules": [
            {"property": "$blueprint", "operator": "=", "value": "service"},
            {
                "blueprint": "api",
                "operator": "relatedTo",
                "value": sending_api,
            },
        ],
    }

    entities = port_client.search_entities(search_query)

    print(f"Found {len(entities)} entities for {sending_api}")

    for entity in entities:
        print(f"Sending notification to {entity['title']}")
        send_notification(entity, message, sending_api)
