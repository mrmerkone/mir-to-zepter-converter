import asyncio
import json

import aiohttp
from attr import dataclass
from bs4 import BeautifulSoup


ZEPTER_CURRENCY_RATES_URL = "https://zepterbank.by/personal/services/currency/card/"
MIR_CURRENCY_RATES_URL = "https://api-user.privetmir.ru/backend/api/v2/currencies/rates"


@dataclass(slots=True, frozen=True)
class ZepterRates:
    USD_SELL: float
    USD_BUY: float
    EUR_SELL: float
    EUR_BUY: float
    RUB_SELL: float
    RUB_BUY: float


async def get_url_content(url: str) -> str:
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                return await response.text()
            return ""


async def get_zepter_rates() -> ZepterRates:
    html = await get_url_content(ZEPTER_CURRENCY_RATES_URL)
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


@dataclass(slots=True, frozen=True)
class MirRates:
    BYN_BUY: float


async def get_mir_rates() -> MirRates:
    data = await get_url_content(MIR_CURRENCY_RATES_URL)

    rates = json.loads(data)

    for rate in rates["content"]:
        if rate["currency"]["strcode"] == "BYN":
            return MirRates(BYN_BUY=rate["valueBuy"])

    return MirRates(BYN_BUY=99999999)


async def main():
    zepter_rates = await get_zepter_rates()
    mir_rates = await get_mir_rates()

    print("Курс доллара", zepter_rates.USD_SELL * mir_rates.BYN_BUY)
    print("Курс евро", zepter_rates.EUR_SELL * mir_rates.BYN_BUY)


if __name__ == "__main__":
    asyncio.run(main())
