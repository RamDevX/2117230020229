import requests
import json
from datetime import datetime

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJyYW1wcmFrYXNoMjMxMDA1QGdtYWlsLmNvbSIsImV4cCI6MTc3ODA1MTA3NywiaWF0IjoxNzc4MDUwMTc3LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiNzMwZWFjMzUtODZhMC00MjdhLWJhOTktODAxNWYxNGQwODQwIiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoic3VicmFtYW5pYW4gcmFtcHJha2FzaCIsInN1YiI6IjJhYzU3YzBmLTRmZDktNGRjZC1iZTU5LTdlYzBiYzdmNjliOCJ9LCJlbWFpbCI6InJhbXByYWthc2gyMzEwMDVAZ21haWwuY29tIiwibmFtZSI6InN1YnJhbWFuaWFuIHJhbXByYWthc2giLCJyb2xsTm8iOiIyMTE3MjMwMDIwMjI5IiwiYWNjZXNzQ29kZSI6IkJUQ0RxVCIsImNsaWVudElEIjoiMmFjNTdjMGYtNGZkOS00ZGNkLWJlNTktN2VjMGJjN2Y2OWI4IiwiY2xpZW50U2VjcmV0IjoiWUZ6QmpGZ2tEVkdmRXNjaCJ9.BUNN9BDSMrMac7Oh7-MP6xuIouci2zsoKxXapP94P1o"
URL = "http://20.207.122.201/evaluation-service/notifications"

weights = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def fetch_notifications():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.get(URL, headers=headers)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return []

        data = response.json()
        return data.get("notifications", [])

    except Exception as e:
        print("Request failed:", str(e))
        return []

def get_top_10(notifications):
    def priority(n):
        weight = weights.get(n.get("Type"), 0)

        try:
            time = datetime.strptime(n.get("Timestamp"), "%Y-%m-%d %H:%M:%S")
        except:
            time = datetime.min

        return (weight, time)

    sorted_data = sorted(notifications, key=priority, reverse=True)
    return sorted_data[:10]

def main():
    notifications = fetch_notifications()

    if not notifications:
        print("No notifications received")
        return

    top10 = get_top_10(notifications)

    output = [
        {
            "ID": n.get("ID"),
            "Type": n.get("Type"),
            "Message": n.get("Message"),
            "Timestamp": n.get("Timestamp")
        }
        for n in top10
    ]

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
