import time
from logger import send_log

class LoggingMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, request):
        start_time = time.time()

        try:
            response = self.app(request)

            duration = time.time() - start_time

            send_log(
                stack="backend",
                level="info",
                package="route",
                message=f"{request['method']} {request['path']} {response['status']} {round(duration,3)}s"
            )

            return response

        except Exception as e:
            send_log(
                stack="backend",
                level="error",
                package="handler",
                message=str(e)
            )
            raise