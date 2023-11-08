import asyncio
import json
import os

import aiohttp

CN_SH_INDEX_SYMBOL = "SH000001"
US_SP500_INDEX_SYMBOL = ".INX"
US_SP500_ETF_SYMBOL = "SPY"
API_KEY = os.getenv("QUOTE_API_KEY")

from dataclasses import dataclass
from typing import Optional, Coroutine
from dataclasses_json import DataClassJsonMixin


@dataclass
class StockQuote(DataClassJsonMixin):
    symbol: str
    name: str
    price: float
    changesPercentage: float
    change: float
    dayLow: float
    dayHigh: float
    yearHigh: float
    yearLow: float
    marketCap: int
    priceAvg50: float
    priceAvg200: float
    exchange: str
    volume: int
    avgVolume: int
    open: float
    previousClose: float
    eps: float
    pe: float
    earningsAnnouncement: Optional[str]
    sharesOutstanding: int
    timestamp: int

    @property
    def changesPercentageStr(self) -> str:
        return (
            f"{self.changesPercentage :.2f}%"
            if self.changesPercentage < 0
            else f"+{self.changesPercentage :.2f}%"
        )


async def fetch_us_quote() -> Optional[StockQuote]:
    url = f"https://financialmodelingprep.com/api/v3/quote/{US_SP500_ETF_SYMBOL}?apikey={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            print(data)
            data = json.loads(data)
            if not data:
                return None
            stock = StockQuote.from_dict(data[0])  # data is a list, get first item
            return stock


async def main():
    stock = await fetch_us_quote()
    print(stock.changesPercentageStr)


if __name__ == "__main__":
    asyncio.run(main())
