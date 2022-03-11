import os


def when_ready(server):
    # touch app-initialized when ready
    open("/tmp/app-initialized", "w").close()


max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "10000"))
