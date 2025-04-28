from balancer_server.lib.threading_tools.rw_decorator import (
    locked_reader,
    locked_writer,
    rw_locked_struct,
)


class LoadNode:
    def __init__(self, load: int, ip: str):
        self.load = load
        self.ip = ip

    def __lt__(self, other: any):
        return self.load < other.load

    def __repr__(self):
        return f"Node({self.load}, {self.ip})"

    def __str__(self):
        return f"Node({self.load}, {self.ip})"


@rw_locked_struct
class ServersHeap:
    def __init__(self, comparator=lambda a, b: a < b):
        self.heap = []
        self._compare = comparator
        self.keymap = {}

    def __len__(self):
        return len(self.heap)

    def __bool__(self):
        return bool(self.heap)

    def __str__(self):
        return str(self.heap)

    @locked_reader
    def __getitem__(self, ip: str) -> LoadNode:
        if ip not in self.keymap:
            raise KeyError(f"{ip!r} is not in the heap.")
        idx = self.keymap[ip]
        return self.heap[idx]

    @locked_writer
    def update_load(self, ip: str, new_load: int) -> None:
        if ip not in self.keymap:
            raise KeyError(f"{ip!r} is not in the heap.")
        idx = self.keymap[ip]
        self.heap[idx] = LoadNode(new_load, ip)
        self._heapify(idx)

    @locked_reader
    def peek(self) -> LoadNode:
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    @locked_writer
    def push(self, ip: str, load: int=0) -> None:
        if ip in self.keymap:
            raise KeyError(f"{ip!r} is already in the heap.")
        idx = len(self.heap)
        self.heap.append(LoadNode(load, ip))
        self.keymap[ip] = idx
        self._heapify_up(idx)

    @locked_writer
    def pop(self) -> LoadNode:
        if not self.heap:
            raise IndexError("pop from empty heap")
        root = self.heap[0]
        last = self.heap.pop()
        del self.keymap[root.ip]
        if self.heap:
            self.heap[0] = last
            self.keymap[last.ip] = 0
            self._heapify_down(0)
        return root

    @locked_writer
    def update_root(self, new_load: int) -> None:
        if not self.heap:
            raise IndexError("update_root from empty heap")
        self.heap[0].load = new_load
        self._heapify_down(0)

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        ip_i = self.heap[i].ip
        ip_j = self.heap[j].ip
        self.keymap[ip_i] = i
        self.keymap[ip_j] = j

    def _heapify(self, i):
        if i > 0 and self._compare(self.heap[i], self.heap[self._parent(i)]):
            self._heapify_up(i)
        else:
            self._heapify_down(i)

    def _heapify_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._compare(self.heap[i], self.heap[p]):
                self._swap(i, p)
                i = p
            else:
                break

    def _heapify_down(self, i):
        n = len(self.heap)
        while True:
            l, r = self._left(i), self._right(i)
            best = i
            if l < n and self._compare(self.heap[l], self.heap[best]):
                best = l
            if r < n and self._compare(self.heap[r], self.heap[best]):
                best = r
            if best == i:
                break
            self._swap(i, best)
            i = best
