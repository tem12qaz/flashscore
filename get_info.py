import asyncio
import traceback
from datetime import datetime

import aiohttp
import parse
import pytz as pytz
from bs4 import BeautifulSoup as bs4

from status_dict import statuses


async def get_info(game: str, proxy=None, proxy_auth=None) -> dict:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            url=f'https://www.flashscorekz.com/match/{game}/#/match-summary/match-summary',
            proxy=proxy,
            proxy_auth=proxy_auth
        )
        resp = await resp.text()
    result = {}

    soup = bs4(resp, 'html.parser')
    html = str(soup)

    players_data = soup.find('meta', {'name': "og:title"})['content']

    status = str(parse.search('"DB":{:d}', html, case_sensitive=True)[0])
    result['status'] = statuses[status]

    if 'Завершен' in result['status']:
        result['fs1'], result['fs2'] = players_data[-3:].split(':')
    else:
        result['fs1'], result['fs2'] = '', ''

    players_data = players_data[:-4]
    result['p1'], result['p2'] = players_data.split(' - ')

    game_data = soup.find('meta', {'name': "og:description"})['content']
    result['tour'], game_data = game_data.split(': ')

    try:
        result['tour2'], result['step'] = game_data.split(' - ', 1)
    except ValueError as e:
        if 'not enough values to unpack' in str(e):
            result['tour2'] = game_data
            result['step'] = ''
        else:
            raise ValueError(e)

    time = parse.search('"DC":{:d}', html, case_sensitive=True)[0]
    time = datetime.fromtimestamp(int(time), tz=pytz.timezone('Asia/Yekaterinburg'))
    result['day'] = time.day
    result['month'] = time.month
    result['year'] = time.year
    result['time'] = time.strftime('%H:%M')

    ranks = parse.findall('"rank":["{:w}","{rank:d}",', html)
    try:
        if '/' in result['p1']:
            try:
                result['r1'] = f'{ranks.next()["rank"]} / {ranks.next()["rank"]}'
                result['r2'] = f'{ranks.next()["rank"]} / {ranks.next()["rank"]}'
            except:
                print('----')
                ranks2 = parse.findall('"rank":[{}]', html)

                rank = parse.search('"{:w}","{rank:d}","', ranks2.next()[0])
                rank2 = parse.search('"{:w}","{rank:d}","', ranks2.next()[0])
                result['r1'] = f'{rank["rank"] if rank else "-"} / {rank2["rank"] if rank2 else "-"} '

                rank = parse.search('"{:w}","{rank:d}","', ranks2.next()[0])
                rank2 = parse.search('"{:w}","{rank:d}","', ranks2.next()[0])
                result['r2'] = f'{rank["rank"] if rank else "-"} / {rank2["rank"] if rank2 else "-"} '

        else:
            result['r1'] = ranks.next()['rank']
            result['r2'] = ranks.next()['rank']
    except:
        # print(traceback.format_exc())
        pass

    # print(result)
    return result

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_info('KO5LovIl'))