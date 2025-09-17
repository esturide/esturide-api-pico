import uvicorn

from app import get_app

app = get_app()

if __name__ == '__main__':
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8080

    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)
