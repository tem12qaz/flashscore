import asyncio
import time
import traceback
from asyncio import AbstractEventLoop

import aiohttp
import parse
from aiohttp import ClientConnectorError

from tours import tours
from years import years


class GameList:
    games = []
    errors = {}
    start = time.time()


async def get_games_of_year(year: str):
    try:
        while games.start > time.time():
            print('wait ')
            await asyncio.sleep(2)
        async with aiohttp.ClientSession() as session:
            resp = await session.get(
                url=f'https://www.flashscore.com{year}'
            )
            resp = await resp.text()
        result = parse.findall('¬~AA÷{}¬AD', resp)
        while True:
            try:
                game = result.next()[0]
                if len(game) == 8:
                    games.games.append(game)
            except StopIteration:
                break
        games.games.extend(result)
    except ClientConnectorError:
        print('CONNECT ERROR')
        games.start = time.time() + 30
        await get_games_of_year(year)
        return

    except Exception as e:
        print(traceback.format_exc())
        games.errors[year] = e


async def get_games(years_: list[str], loop: AbstractEventLoop):
    i = 0
    for tour in years_:
        while games.start > time.time():
            print('wait ')
            await asyncio.sleep(2)
        loop.create_task(get_games_of_year(tour))
        await asyncio.sleep(0.03)
        print(len(games.games))
        i += 1
        print(f'{i}/ {len(years_)}')

    while len(asyncio.all_tasks(loop)) > 1:
        await asyncio.sleep(4)
        print('wait all tasks')

    with open('games.py', 'w') as f:
        f.write(str(games.games))
    # print('------------------------')
    print(games.errors)


if __name__ == "__main__":
    games = GameList()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_games(years, loop))

