
import httpx
import datetime
import asyncio
import time


async def request(client):
    resp = await client.get('http://httpbin.org/get')
    result = resp.content.decode()
    print(result)


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        start = time.time()
        task_list = []
        for _ in range(100):
            req = request(client)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
        end = time.time()
    print(f'发送100次请求，耗时：{end - start}')

asyncio.run(main())
# import random
# import time
# import datetime
# import requests
#
#
# def make_request(session):
#     resp = session.get('http://httpbin.org/get', proxies={"http": "http://110.243.2.44:9999"})
#     result = resp.json()
#     print(result)
#
#
# def main():
#     session = requests.Session()
#     start = time.time()
#     for _ in range(10):
#         make_request(session)
#     end = time.time()
#     print(f'发送100次请求，耗时：{end - start}')
#
#
# if __name__ == '__main__':
#     main()
