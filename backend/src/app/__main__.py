from aiohttp import web

from app.api import get_app


def main():
    app = get_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
