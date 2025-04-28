import asyncio

class MultiLock:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self.lock_count = 0

    async def acquire(self, blocking: bool = True) -> bool:
        self.lock_count += 1
        if not blocking:
            if not self._lock.locked():
                await self._lock.acquire()
                return True
            else:
                return False
        else:
            await self._lock.acquire()
            return True

    def release(self) -> None:
        self.lock_count -= 1
        if self.lock_count == 0 and self._lock.locked():
            self._lock.release()

    async def __aenter__(self):
        await self.acquire(blocking=True)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.release()
