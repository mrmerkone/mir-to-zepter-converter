import asyncio

import aiohttp
from attr import dataclass
from bs4 import BeautifulSoup


ZEPTER_CURRENCY_RATES_URL = "https://www.zepterbank.by/personal/services/currency/card/"
MIR_CURRENCY_RATES_URL = "https://mironline.ru/support/list/kursy_mir/"


@dataclass(slots=True, frozen=True)
class ZepterRates:
    USD_SELL: float
    USD_BUY: float
    EUR_SELL: float
    EUR_BUY: float
    RUB_SELL: float
    RUB_BUY: float


async def get_rates_html(url: str) -> str:
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                return await response.text()
            return ""


async def get_zepter_rates() -> ZepterRates:
    html = await get_rates_html(ZEPTER_CURRENCY_RATES_URL)
    soup = BeautifulSoup(html, "html.parser")

    rates_table = soup.find("table", attrs={"class": "rate rate_long_name"})
    rates_table_body = rates_table.find("tbody")
    rates_table_rows = rates_table_body.find_all("tr")

    kwargs = {}

    for row in rates_table_rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]

        amount, currency, buy, sell = cols

        kwargs[f"{currency}_SELL"] = float(sell) / float(amount)
        kwargs[f"{currency}_BUY"] = float(buy) / float(amount)

    return ZepterRates(**kwargs)


MIR_CURRENCY_NAME_MAP = {
    "Армянский драм": "AMD",
    "Белорусский рубль": "BYN",
    "Казахстанский тенге": "KZT",
}


@dataclass(slots=True, frozen=True)
class MirRates:
    AMD_BUY: float
    BYN_BUY: float
    KZT_BUY: float


async def get_mir_rates() -> MirRates:
    html = await get_rates_html(MIR_CURRENCY_RATES_URL)
    soup = BeautifulSoup(html, "html.parser")

    rates_table = soup.find(
        "table",
        attrs={"cellpadding": "0", "cellspacing": "0", "style": "height: 500px;"},
    )
    rates_table_body = rates_table.find("tbody")
    rates_table_rows = rates_table_body.find_all("tr")

    kwargs = {}

    for row in rates_table_rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if cols:
            currency_name, buy = cols
            if currency_name in MIR_CURRENCY_NAME_MAP:
                currency = MIR_CURRENCY_NAME_MAP[currency_name]
                kwargs[f"{currency}_BUY"] = float(buy.replace(",", "."))

    return MirRates(**kwargs)


async def main():
    zepter_rates = await get_zepter_rates()
    mir_rates = await get_mir_rates()

    print("Курс доллара", zepter_rates.USD_SELL * mir_rates.BYN_BUY)
    print("Курс евро", zepter_rates.EUR_SELL * mir_rates.BYN_BUY)


if __name__ == "__main__":
    asyncio.run(main())
