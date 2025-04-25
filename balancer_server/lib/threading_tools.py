from threading import RLock

class MultiLock:
    def __init__(self):
        self.lock = RLock()
        self.lock_count = 0

    def acquire(self, blocking=True):
        self.lock_count += 1
        return self.lock.acquire(blocking)

    def release(self, *args):
        self.lock_count -= 1
        if self.lock_count == 0:
            self.lock.release(*args)
        
    def __enter__(self):
        self.acquire()

    def __exit__(self, *args):
        self.release(*args)


def locked_reader(func):
    def wrapper(self, *args, **kwargs):
        with self.__write_cond__:
            self.__read_cond__.acquire(blocking=False)
            try:           
                res = func(*args, **kwargs)
            finally:
                self.__read_cond__.release()
                return res
    return wrapper

def locked_writer(func):
    def wrapper(self, *args, **kwargs):
        with self.__read_cond__, self.__write_cond__:
            return func(*args, **kwargs)
    return wrapper

def rw_locked_struct(cls):
    def wrapper(*args, **kwargs):
        instance = cls(*args, **kwargs)
        setattr(instance, "__reader_lock__", MultiLock())
        setattr(instance, "__writer_lock__", RLock())
        return instance
    return wrapper
