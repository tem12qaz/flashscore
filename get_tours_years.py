import asyncio
import time
import traceback
from asyncio import AbstractEventLoop

import aiohttp
import requests
from bs4 import BeautifulSoup as bs4

from tours import tours


class YearsList:
    years = []
    errors = {}


async def get_years_of_tour(tour: str):
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(
                url=f'https://www.flashscorekz.com{tour}archive/'
            )
            resp = await resp.text()
        soup = bs4(resp, 'html.parser')
        for year in soup.find_all('a', 'archive__text'):
            years.years.append(year['href'])
    except Exception as e:
        print(traceback.format_exc())
        years.errors[tour] = e


async def get_years(tours_: list[str], loop: AbstractEventLoop):
    i = 0
    for tour in tours_:
        loop.create_task(get_years_of_tour(tour))
        await asyncio.sleep(0.05)
        print(len(years.years))
        i += 1
        print(f'{i}/ {len(tours)}')

    while len(asyncio.all_tasks(loop)) > 1:
        await asyncio.sleep(4)
        print('wait all tasks')

    with open('years.txt', 'w') as f:
        f.write(str(years.years))
    # print('------------------------')
    print(years.errors)


if __name__ == "__main__":
    years = YearsList()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_years(tours, loop))

