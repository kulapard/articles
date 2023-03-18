"""
Example 2:
Demonstrating how asyncio.shield() does not prevent
tasks from being canceled during a shutdown.
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
        if n < 3:
            # protect task from being canceled (spoiler: it will be canceled anyway)
            task = asyncio.shield(task)

        tasks.append(task)

    # wait for all tasks to finish
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("App was interrupted")
    else:
        print("App was finished gracefully")
