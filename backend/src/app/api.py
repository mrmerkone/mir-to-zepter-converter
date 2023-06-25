from aiohttp import web

from app.rates import get_zepter_rates, get_mir_rates


async def index(_request):
    return web.FileResponse('./dist/index.html')


async def favicon(_request):
    return web.FileResponse('./dist/favicon.ico')


async def rates(_request):
    zepter_rates = await get_zepter_rates()
    mir_rates = await get_mir_rates()
    return web.json_response(
        data={
            "USD": round(zepter_rates.USD_SELL * mir_rates.BYN_BUY, ndigits=2),
            "EUR": round(zepter_rates.EUR_SELL * mir_rates.BYN_BUY, ndigits=2),
        }
    )


def get_app() -> web.Application:
    app = web.Application()
    app.add_routes([
        web.get("/", index),
        web.get("/api/rates", rates),
        web.get("/favicon.ico", favicon),
        web.static("/assets", "dist/assets")
    ])
    return app
