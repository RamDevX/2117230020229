from middleware import LoggingMiddleware

def simple_app(request):
    return {
        "status": 200,
        "data": "Hi RP"
    }

app = LoggingMiddleware(simple_app)


request = {
    "method": "GET",
    "path": "/test"
}

response = app(request)
print(response)