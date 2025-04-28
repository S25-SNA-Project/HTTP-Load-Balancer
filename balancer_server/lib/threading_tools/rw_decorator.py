from asyncio import Lock
from MultiLock import MultiLock

def locked_reader(func):
    async def wrapper(self, *args, **kwargs):
        async with self.__write_lock__:
            await self.__read_lock__.acquire(blocking=False)
            try:    
                # in general case function call should be awaited, but our heap - not asynchronous by itself       
                res = func(*args, **kwargs)
            finally:
                self.__read_lock__.release()
                return res
    return wrapper

def locked_writer(func):
    async def wrapper(self, *args, **kwargs):
        async with self.__read_lock__, self.__write_lock__:
            return func(*args, **kwargs)
    return wrapper

def rw_locked_struct(cls):
    class _ReaderWriterDecorator(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__read_lock__ = MultiLock()
            self.__write_lock__ = Lock()

    return _ReaderWriterDecorator
