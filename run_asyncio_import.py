import argparse
import string
import time
import urllib.request

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import terminaltables
import tqdm


URL = u'http://www.fightmetric.com/statistics/fighters?char={}&page=all'
LETTERS = [l for l in string.ascii_lowercase[:26]]
HEADERS = [
    'First name',
    'Last Name',
    'Nickname',
    'Height',
    'Weight (lbs)',
    'Reach',
    'Stance',
    'Wins',
    'Losses',
    'Draws',
]


def process_fighters(response):
    fighters = []
    soup = BeautifulSoup(response, "html.parser")
    fighter_table_rows = soup.find_all('tr')

    # start from 2 offset (first 2 rows are headers)
    for fighter in fighter_table_rows[2:]:
        data = fighter.find_all('td')

        # grab name data
        first_name = data[0].a.string.strip()
        last_name = data[1].a.string.strip()
        nickname = data[2].a.string
        if nickname:
            nickname = nickname.strip()

        # work out height
        height = data[3].string.strip()
        if not height or height == '--':
            height = None

        # work out weight
        weight = data[4].string.strip()

        # work out reach
        reach = data[5].string.strip()
        if not reach or reach == '--':
            reach = None

        # work out stance
        stance = data[6].string.strip()
        if not stance or stance == '--':
            stance = None

        # grab wins, losses and draws
        wins = int(data[7].string.strip())
        losses = int(data[8].string.strip())
        draws = int(data[9].string.strip())

        fighters.append([
            first_name,
            last_name,
            nickname,
            height,
            weight,
            reach,
            stance,
            wins,
            losses,
            draws,
        ])
    return fighters


def fetch_page_sync(letter):
    url = URL.format(letter)
    print(url)
    response = urllib.request.urlopen(url)
    fighters = process_fighters(response.read())
    return fighters


def synchronous():
    """
    synchronous version so that we can see the difference in speed
    """
    print('Loading Fighters from fightmtetric.com synchronously...')
    start = time.time()
    table_data = [HEADERS]

    for l in LETTERS:
        fighters = fetch_page_sync(l)
        for f in fighters:
            table_data.append(f)

    table = terminaltables.AsciiTable(table_data)
    print(table.table)
    print ("{} Fighters retrieved!".format(len(table_data) - 1))
    print("Process took: {:.2f} seconds".format(time.time() - start))


async def aiohttp_get(url, compress=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, compress=compress) as response:
            return await response.text()


async def fetch_page_async(letter):
    url = URL.format(letter)
    async with sem:
        page = await aiohttp_get(url, compress=True)
    fighters = process_fighters(page)
    return fighters


async def wait_with_progress(tasks):
    print('Loading Fighters from fightmtetric.com using asyncio...')
    table_data = [HEADERS]
    for future in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        fighters = await future
        for f in fighters:
            table_data.append(f)
    table = terminaltables.AsciiTable(table_data)
    print(table.table)
    print ("{} Fighters retrieved!".format(len(table_data) - 1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--sync",
        action="store_true", dest="run_sync", default=False,
        help="Run import synchronously")
    args = parser.parse_args()
    if args.run_sync:
        synchronous()
    else:
        start = time.time()
        sem = asyncio.Semaphore(5)
        loop = asyncio.get_event_loop()
        tasks = [fetch_page_async(l) for l in LETTERS]
        loop.run_until_complete(wait_with_progress(tasks))
        print("Process took: {:.2f} seconds".format(time.time() - start))
