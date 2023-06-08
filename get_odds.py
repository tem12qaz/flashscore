import asyncio
import aiohttp


async def get_odds(game: str, proxy, proxy_auth) -> dict:
    headers = {
        'authority': '46.ds.lsapp.eu',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://www.flashscore.com',
        'referer': 'https://www.flashscore.com/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            url=f'https://46.ds.lsapp.eu/pq_graphql?_hash=ope&eventId={game}&projectId=46&geoIpCode=RU&geoIpSubdivisionCode=RUMOW',
            headers=headers,
            proxy=proxy,
            proxy_auth=proxy_auth
        )
        resp = await resp.json()
    result = parse_odds(resp)
    # print(result)
    return result


def parse_odds(data: dict) -> dict:
    result = {}
    data = data['data']['findPrematchOddsById']['odds'][0]['odds']
    result['c1'] = data[0]['value']
    result['c2'] = data[1]['value']
    return result


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_odds('UJQSQOjB'))