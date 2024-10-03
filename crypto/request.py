from datetime import date, timedelta
from asyncio import run

from aiohttp import ClientSession

class AssetServices:
    async def day_sumary(self, symbol: str):
        async with ClientSession() as session:
            yesterday = date.today() - timedelta(days=1)

            url = f'https://www.mercadobitcoin.net/api/{symbol.upper()}/day-summary/{yesterday.year}/{yesterday.month}/{yesterday.day}'

            response = await session.get(url)
            data = await response.json()

            return {
                'highest': data['highest'],
                'lowest': data['lowest'],
                'symbol': symbol
            }

if __name__ == '__main__':
    romario = AssetServices()
    print(run(AssetServices().day_sumary(symbol='BTC')))