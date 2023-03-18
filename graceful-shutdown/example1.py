"""
Example 1:
Demonstrates what's happening with tasks when an app is interrupted.
"""

import asyncio


async def worker(n: int) -> None:
    print(f"[{n}] Started!")
    try:
        # this is a task that shouldn't be canceled in the middle
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print(f"[{n}] Canceled while doing something (this is bad)!")
    else:
        print(f"[{n}] Successfully done!")


async def main() -> None:
    # create 6 tasks, shield only first 3
    tasks = []
    for n in range(6):
        task = asyncio.create_task(worker(n))
        tasks.append(task)

    # wait for all tasks to finish
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App was interrupted")
    else:
        print("App was finished gracefully")
