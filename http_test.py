import asyncio
import socket
import aiohttp

WB_URL = 'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?locale=ru&lang=ru&curr=rub&nm='


async def fetch_url(i):
    url = WB_URL + str(i)
    async with aiohttp.request('get', url) as request:
        return await request.text()


async def async_main(id):
    resource = list(i for i in range(id, id + 1000))

    tasks = [
        asyncio.ensure_future(fetch_url(id_))
        for id_ in resource
    ]

    parts = []
    for future in asyncio.as_completed(tasks):
        parts.append(await future)

    with open('result.txt', 'a') as text_file:
        text_file.write('{}\n'.format('\n'.join(parts)))


if __name__ == '__main__':

    for i in range(10000000, 20000000, 1000):
        print(i)
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(async_main(i))
