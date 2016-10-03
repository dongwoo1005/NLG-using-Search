# stack structure
class Stack():
    def __init__(self):
        self.stack = []
        self.length = 0

    def push(self, item):
        if not self.stack:
            self.stack = [ item ]
        else:
            self.stack = [item ] + self.stack
        self.length += 1

    def pop(self):
        if not self.stack:
            return
        else:
            item = self.stack.pop(0)
            self.length -= 1
            return item

    def empty(self):
        isEmpty = False
        if not self.stack:
            isEmpty = True
        return isEmpty