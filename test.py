import asyncio

import multiprocessing

#import resource

import threading

import time

from pathlib import Path

from typing import Iterator



import aiohttp

import orjson

from rich import print

from yarl import URL



GROUPS: int = 35_000_000

PROCESSES: int = 10

THREADS: int = 1

TASKS: int = 1

PROXIES: list[str] = [f"http://{i}" for i in Path("./proxies.txt").read_text().split("\n")]

PROXY_COOLDOWN: int = 30





async def detect(id: int) -> None:

    """Your code for when a claimable group is detected here."""

    print(f"[bold green]FOUND GROUP[/]: {id}")



"""

DO NOT EDIT PAST THIS POINT.

"""



_GROUP_DIV = GROUPS // PROCESSES

_THREADS_DIV = _GROUP_DIV // THREADS

_TASK_DIV = _THREADS_DIV // TASKS



_MANAGER = multiprocessing.Manager()

_FOUND = _MANAGER.list()

_NAMESPACE = _MANAGER.Namespace()



_NAMESPACE.last_minute = time.time()

_NAMESPACE.cpm = -1

__version__ = '2.0.0-alpha'



"""

if len(PROXIES) == 0:

    print("[bold red]no proxies set, ending...", file=sys.stderr)

    exit()

"""



def _chunked(limit: int, max: int) -> Iterator[tuple[int, int]]:

    amount = -(-max // limit)

    chunk = 0



    for i in range(limit):

        chunk += amount

        yield i, chunk





async def _req(ids: list[int], session: aiohttp.ClientSession, proxy_addr: URL, overload: dict) -> None:

    e = overload.get(str(proxy_addr))

    if e:

        await asyncio.to_thread(e.wait)



    async with session.get(f"https://groups.roblox.com/v2/groups?groupIds={','.join([str(i) for i in ids])}") as resp:

        json = await resp.json()

        _NAMESPACE.cpm += 1



        groups = json.get("data")



        if not groups:

            if str(proxy_addr) in overload:

                return



            event = threading.Event()

            print(f"[bold red]{proxy_addr} is on cooldown[/] (too many requests)")

            overload[str(proxy_addr)] = event

            await asyncio.sleep(PROXY_COOLDOWN)

            print(f"[bold green]{proxy_addr} back online[/]")

            event.set()

            overload[str(proxy_addr)] = None

            return



        for data in groups:

            if (not data["owner"]):

                id: int = data["id"]

                if id in _FOUND:

                    return

                

                next_res = await session.get(f"https://groups.roblox.com/v1/groups/{id}")

                next_json = await next_res.json()

                if "errors" in next_json:

                    event = threading.Event()

                    print(f"[bold red]{proxy_addr} had an error[/]", next_json)

                    overload[str(proxy_addr)] = event

                    await asyncio.sleep(PROXY_COOLDOWN)

                    event.set()

                    overload[str(proxy_addr)] = None

                elif ("isLocked" not in next_json) and (next_json.get("publicEntryAllowed")):

                    _FOUND.append(id)

                    await detect(id)



async def _task(proc_id: int, thread_id: int, id: int, chunk: int, event: threading.Event, overload: dict):

    print(f"[bold green]process {proc_id}[/] [bold blue]thread {thread_id}[/] [bold red]task {id}[/]: ready at chunk {chunk}")

    event.wait()

    batches: list[list[int]] = [[]]

    for id in range(chunk - _TASK_DIV, chunk):

        continue_outside = False



        for rng in (range(17412877, 31999999), range(32300000, 33216400)):

            if id in rng:

                continue_outside = True



        if continue_outside:

            continue



        if len(batches[-1]) == 99:

            batches.append([])



        batches[-1].append(id)



    loop = asyncio.get_event_loop()

    tasks = []

    gens = []

    current_proxy = 0

    async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:  # type: ignore

        for batch in batches:

            current_proxy += 1

            if current_proxy == len(PROXIES):

                current_proxy = 0

            

            proxy = URL(PROXIES[current_proxy])



            def _spawn():

                return loop.create_task(_req(batch, session, proxy, overload))

            

            gens.append(_spawn)



        while True:

            tasks = [spawn() for spawn in gens]

            await asyncio.gather(*tasks)



def _thread(proc_id: int, id: int, chunk: int, event: threading.Event, overload: dict):

    print(f"[bold green]process {proc_id}[/] [bold blue]thread {id}[/]: ready at chunk {chunk}")

    event.wait()

    

    loop = asyncio.new_event_loop()

    tasks = []

    task_event = threading.Event()



    for index, t_chunk in _chunked(TASKS, _THREADS_DIV):

        tasks.append(loop.create_task(_task(proc_id, id, index, t_chunk + (chunk - _THREADS_DIV), task_event, overload)))



    task_event.set()

    loop.run_until_complete(asyncio.gather(*tasks))



def _process(id: int, chunk: int):

    print(f"[bold green]process {id}[/]: ready at chunk {chunk}")

    event = threading.Event()

    threads = []

    overload = {}



    for index, t_chunk in _chunked(THREADS, _GROUP_DIV):

        t = threading.Thread(target=_thread, args=(id, index, t_chunk + (chunk - _GROUP_DIV), event, overload),)

        threads.append(t)

        t.start()



    event.set()



    for thread in threads:

        thread.join()



def _cpm():

    while True:

        if (round(time.time()) - round(_NAMESPACE.last_minute)) >= 60:

            print("Checks per minute:", _NAMESPACE.cpm)

            _NAMESPACE.cpm = 0

            _NAMESPACE.last_minute = time.time()



def main():

    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)

    resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))

    print(f'[bold green]Intensifinder {__version__}[/]')

    cpm_proc = multiprocessing.Process(target=_cpm)

    cpm_proc.start()

    procs = [cpm_proc]



    for index, chunk in _chunked(PROCESSES, GROUPS):

        proc = multiprocessing.Process(target=_process, args=(index, chunk))

        procs.append(proc)

        proc.start()

        

    for proc in procs:

        proc.join()





if __name__ == '__main__':

    main()