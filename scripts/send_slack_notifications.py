import json
import sys
import requests

def send_notification(entity, message, api):
    title = entity['title']
    slack_webhook = entity['properties'].get('slack') 

    if slack_webhook:
        payload = {
            "text": f"Hello {title}! {message}. {api} team.",
        }
        requests.post(slack_webhook, json=payload)
    else:
        print(f"No Slack webhook found for: {title}")

if __name__ == "__main__":
    entities_file = sys.argv[1]
    message = sys.argv[2]
    api = sys.argv[3]

    print(f"Sending notification to entities in {entities_file} with message: {message}")
    
    with open(entities_file) as f:
        entities = json.load(f)

    for entity in entities:
        send_notification(entity, message, api)
