import requests

LOG_API_URL = "http://20.207.122.201/evaluation-service/logs"

def send_log(stack, level, package, message):
    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }

    try:
        response = requests.post(LOG_API_URL, json=payload, timeout=2)
        return response.status_code
    except Exception as e:
        print("Log API failed:", str(e))