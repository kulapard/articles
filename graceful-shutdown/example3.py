"""
Example 3:
Graceful shutdown with handling signals.
"""

import asyncio
import signal

# tasks that shouldn't be canceled
_DO_NOT_CANCEL_TASKS: set[asyncio.Task] = set()


def protect(task: asyncio.Task) -> None:
    _DO_NOT_CANCEL_TASKS.add(task)


def shutdown(sig: signal.Signals) -> None:
    print(f"Received exit signal {sig.name}")

    all_tasks = asyncio.all_tasks()
    tasks_to_cancel = all_tasks - _DO_NOT_CANCEL_TASKS

    for task in tasks_to_cancel:
        task.cancel()

    print(f"Cancelled {len(tasks_to_cancel)} out of {len(all_tasks)} tasks")


def setup_signal_handler() -> None:
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown, sig)


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
    # setup graceful shutdown
    setup_signal_handler()

    # protect main task from being canceled,
    # otherwise it will cancel all other tasks
    protect(asyncio.current_task())

    # create 6 tasks, shield only first 3
    tasks = []
    for n in range(6):
        task = asyncio.create_task(worker(n))
        if n < 3:
            protect(task)

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
