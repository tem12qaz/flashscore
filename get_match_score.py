import asyncio

import aiohttp
import parse
from parse import search
import requests
'''
day month year time tour tour2 step p1 p2 r1 r2 score1 score2 status alltime times с1 с2 fs1 fs2 
с1 с2 
'''


async def get_score(game: str, proxy = None, proxy_auth = None) -> dict:
    headers = {
        'authority': 'd.flashscorekz.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.flashscorekz.com',
        'referer': 'https://www.flashscorekz.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-fsign': 'SW9D1eZo',
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            url=f'https://d.flashscorekz.com/x/feed/df_sur_1_{game}',
            headers=headers,
            proxy=proxy,
            proxy_auth=proxy_auth
        )
        resp = await resp.text()

    # print(resp)
    result = parse_score(resp)
    # print(result)
    return result


def parse_score(score_str: str) -> dict:
    try:
        result = {'full_time': parse.search('¬~RB÷{}¬~', score_str)[0]}
    except TypeError:
        result = {}
    score_str = score_str.split('¬~RB÷')[0]
    sets = score_str.split('¬~')
    i = 1
    for set_ in sets:
        fmt = 'B{:w}÷{p1:d}¬B{:w}÷{p2:d}¬R{:w}÷{time}$'.replace(
            'p1', f'team_1_set_{i}'
        ).replace(
            'p2', f'team_2_set_{i}'
        ).replace(
            'time', f'set_{i}_time'
        )
        data = parse.search(fmt, set_ + '$')
        if not data:
            fmt = 'B{:w}÷{p1:d}¬D{:w}÷{tp1:d}¬B{:w}÷{p2:d}¬D{:w}÷{tp2:d}¬R{:w}÷{time}$'.replace(
                'p1', f'team_1_set_{i}'
            ).replace(
                'p2', f'team_2_set_{i}'
            ).replace(
                'tp1', f'team_2_set_{i}_break'
            ).replace(
                'tp2', f'team_2_set_{i}_break'
            ).replace(
                'time', f'set_{i}_time'
            )
            data = parse.search(fmt, set_ + '$')
            if not data:
                fmt = 'B{:w}÷{p1:d}¬B{:w}÷{p2:d}$'.replace(
                    'p1', f'team_1_set_{i}'
                ).replace(
                    'p2', f'team_2_set_{i}'
                )
                data = parse.search(fmt, set_ + '$')
                if not data:
                    fmt = 'B{:w}÷{p1:d}¬D{:w}÷{tp1:d}¬B{:w}÷{p2:d}¬D{:w}÷{tp2:d}$'.replace(
                        'p1', f'team_1_set_{i}'
                    ).replace(
                        'p2', f'team_2_set_{i}'
                    ).replace(
                        'tp1', f'team_2_set_{i}_break'
                    ).replace(
                        'tp2', f'team_2_set_{i}_break'
                    )
                    data = parse.search(fmt, set_ + '$')

        if data:
            result.update(data.named)
        elif i <= 1:
            # raise ValueError('score not success')
            return result
        i += 1
    # print(result)
    return result



if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(get_score('fLryUxQB'))
    loop.run_until_complete(get_score('Wd46FjTl'))