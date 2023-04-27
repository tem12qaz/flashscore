import asyncio
import os
import time
import traceback
from asyncio import AbstractEventLoop

import aiohttp
from aiohttp import ClientConnectorError
from games import  collected_games

import db
from games_not_recorded import gms
from get_info import get_info
from get_match_score import get_score
from get_odds import get_odds
from models import Tennis


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Parser:
    def __new__(cls, games_):
        if not hasattr(cls, 'instance'):
            cls.instance: Parser = super(Parser, cls).__new__(cls)
            cls.instance.errors = {}
            cls.instance.parsed = 0
            cls.instance.no_odds = 0
            cls.instance.success = 0
            cls.instance.start = time.time()
            cls.instance.games = games_
            cls.instance.connections_errors = {}
            cls.instance.loop: AbstractEventLoop = None

            cls.instance.proxies = [
                ("95.164.110.247", "9698", "bRThFf", "8BG6G3"),
                ("95.164.111.210", "9074", "bRThFf", "8BG6G3"),
                ("95.164.111.233", "9366", "bRThFf", "8BG6G3"),
                ("168.80.24.183", "8000", "uS8XJB", "MgSNbp"),
                ("168.80.25.190", "8000", "uS8XJB", "MgSNbp"),
                ("91.218.51.20", "9516", "bWQH4C", "a8sA5y"),

            ]

        return cls.instance

    def shift_proxy(self):
        proxy = self.proxies.pop(0)
        self.proxies.append(proxy)
        return proxy

    def get_proxies(self) -> tuple[str, aiohttp.BasicAuth]:
        proxy_tuple = self.shift_proxy()
        proxy = f'http://{proxy_tuple[0]}:{proxy_tuple[1]}'
        proxy_auth = aiohttp.BasicAuth(proxy_tuple[2], proxy_tuple[3])
        return proxy, proxy_auth

    async def parse_game_wrapper(self, game):
        try:
            while self.start > time.time():
                await asyncio.sleep(1)
            await self.parse_game(game)
            if self.connections_errors.get(game):
                self.connections_errors.pop(game)

        except ClientConnectorError as e:
            errs = self.connections_errors.get(game)

            if errs and (self.connections_errors[game] >= 5):
                self.connections_errors.pop(game)
                self.errors[game] = e
                return
            if errs:
                self.connections_errors[game] = errs + 1
            else:
                self.connections_errors[game] = 1

            # print('CONNECT ERROR')
            self.start = time.time() + 15
            await self.parse_game_wrapper(game)
            return
        except Exception as e:
            # print(game)
            # print(traceback.format_exc())
            # print('-------------------------------------------')
            self.errors[game] = e

    async def parse_game(self, game):
        proxy, proxy_auth = self.get_proxies()
        print(proxy)
        result = {'event_id': game}
        try:
            result.update(await get_odds(game, proxy, proxy_auth))
        except:
            self.no_odds += 1
        result.update(await get_score(game, proxy, proxy_auth))
        result.update(await get_info(game, proxy, proxy_auth))
        self.parsed += 1
        # print(result)
        await Tennis.create(**result)
        self.success += 1
        self.games.remove(game)

    async def main(self):
        await db.db_init()
        for game in self.games:
            self.log()
            while self.start > time.time():
                await asyncio.sleep(1)
            self.loop.create_task(self.parse_game_wrapper(game))
            await asyncio.sleep(0.1)

        while len(asyncio.all_tasks(self.loop)) > 1:
            await asyncio.sleep(4)
            print('wait all tasks')

        with open('games_not_recorded.py', 'w') as f:
            f.write(str(self.games))
        with open('errs.txt', 'w') as f:
            f.write(str(self.games))

        return

    def log(self):
        OK = Colors.OKGREEN +'OK' + Colors.ENDC
        WAIT = Colors.WARNING +'WAIT' + Colors.ENDC
        os.system('cls')
        print(f'''
{Colors.HEADER}GAMES:{Colors.ENDC} {len(self.games)}


{Colors.HEADER}STATUS:{Colors.ENDC} {OK if self.start < time.time() else WAIT}


        
{Colors.OKCYAN}EVENTS:{Colors.ENDC} {self.parsed}
{Colors.OKCYAN}EVENTS IN BASE:{Colors.ENDC} {self.success}

{Colors.WARNING}NO_ODDS:{Colors.ENDC} {self.no_odds}

{Colors.FAIL}ERRORS:{Colors.ENDC} {len(self.errors)}'''
              )

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            self.loop = loop
            loop.run_until_complete(self.main())
        except KeyboardInterrupt:
            with open('games_not_recorded.py', 'w') as f:
                f.write(str(self.games))
            with open('errs.txt', 'w') as f:
                f.write(str(self.errors))
            raise KeyboardInterrupt('exit')



if __name__ == '__main__':
    parser = Parser(games_=gms)
    parser.run()
