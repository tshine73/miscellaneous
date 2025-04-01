from requests import post, get
import time
import asyncio


async def Async_POST(url, sequence, loop):
    print(url)
    print(f"{sequence} start post time : {time.strftime('%X')}")
    if sequence == 1:
        await asyncio.sleep(2)
    resp = await loop.run_in_executor(None, GET, url)
    print(f"{sequence} response time : {time.strftime('%X')}")
    return sequence


def GET(url):
    return get(url=url)


async def main():
    url = r'http://localhost:5000/async?id='
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(1, 3):
        tasks.append(loop.create_task(Async_POST(url + str(i), i, loop)))
    # x = await asyncio.gather(*tasks)
    # print(x)



if __name__ == '__main__':
    asyncio.run(main())
    print("end....")
