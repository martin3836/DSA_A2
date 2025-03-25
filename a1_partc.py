#    Main Author(s): 
#    Main Reviewer(s):



class Stack:
    def __init__(self, cap=10):
        """
        Initializes the Stack with a given capacity or a default of 10.
        """
        self.capacity_val = cap  # Stack capacity
        self.stack = []          # Stack list to store elements

    def capacity(self):
        """
        Returns the current capacity of the stack.
        """
        return self.capacity_val

    def push(self, data):
        """
        Adds an item to the top of the stack. If the stack exceeds its capacity, it resizes.
        """
        if len(self.stack) >= self.capacity_val:
            self.capacity_val *= 2  # Double the capacity
        self.stack.append(data)

    def pop(self):
        """
        Removes and returns the top item from the stack. Raises IndexError if the stack is empty.
        """
        if self.is_empty():
            raise IndexError('pop() used on empty stack')
        return self.stack.pop()

    def get_top(self):
        """
        Returns the top item from the stack without removing it.
        Returns None if the stack is empty.
        """
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        """
        Returns True if the stack is empty, otherwise False.
        """
        return len(self.stack) == 0

    def __len__(self):
        """
        Returns the number of items in the stack.
        """
        return len(self.stack)



class Queue:
    def __init__(self, cap=10):
        """
        Initializes the Queue with a given capacity or a default of 10.
        """
        self.capacity_val = cap  # Queue capacity
        self.queue = []          # Queue list to store elements

    def capacity(self):
        """
        Returns the current capacity of the queue.
        """
        return self.capacity_val

    def enqueue(self, data):
        """
        Adds an item to the back of the queue. If the queue exceeds its capacity, it resizes.
        """
        if len(self.queue) >= self.capacity_val:
            self.capacity_val *= 2  # Double the capacity
        self.queue.append(data)

    def dequeue(self):
        """
        Removes and returns the front (oldest) item from the queue. Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError('dequeue() used on empty queue')
        return self.queue.pop(0)  # Remove the first element (FIFO)

    def get_front(self):
        """
        Returns the front (oldest) item from the queue without removing it.
        Returns None if the queue is empty.
        """
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self):
        """
        Returns True if the queue is empty, otherwise False.
        """
        return len(self.queue) == 0

    def __len__(self):
        """
        Returns the number of items in the queue.
        """
        return len(self.queue)




class Deque:
    def __init__(self, cap=10):
        """
        Initializes the Deque with a given capacity or a default of 10.
        """
        self.capacity_val = cap  # Initial capacity of the deque
        self.deque = []          # Internal list to store elements

    def capacity(self):
        """
        Returns the current capacity of the deque.
        """
        return self.capacity_val

    def push_front(self, data):
        """
        Adds data to the front of the deque. If the deque exceeds capacity, it resizes.
        """
        if len(self.deque) >= self.capacity_val:
            self.capacity_val *= 2  # Double the capacity
        self.deque.insert(0, data)  # Insert element at the front

    def pop_front(self):
        """
        Removes and returns the value from the front of the deque. Raises IndexError if deque is empty.
        """
        if self.is_empty():
            raise IndexError('pop_front() used on empty deque')
        return self.deque.pop(0)  # Remove the first element

    def push_back(self, data):
        """
        Adds data to the back of the deque. If the deque exceeds capacity, it resizes.
        """
        if len(self.deque) >= self.capacity_val:
            self.capacity_val *= 2  # Double the capacity
        self.deque.append(data)  # Append element to the back

    def pop_back(self):
        """
        Removes and returns the value from the back of the deque. Raises IndexError if deque is empty.
        """
        if self.is_empty():
            raise IndexError('pop_back() used on empty deque')
        return self.deque.pop()  # Remove the last element

    def get_front(self):
        """
        Returns the value from the front of the deque without removing it.
        """
        if self.is_empty():
            return None
        return self.deque[0]

    def get_back(self):
        """
        Returns the value from the back of the deque without removing it.
        """
        if self.is_empty():
            return None
        return self.deque[-1]

    def is_empty(self):
        """
        Returns True if the deque is empty, otherwise False.
        """
        return len(self.deque) == 0

    def __len__(self):
        """
        Returns the number of elements in the deque.
        """
        return len(self.deque)

    def __getitem__(self, k):
        """
        Returns the k'th element from the front of the deque without removing it.
        Raises IndexError if k is out of range.
        """
        if k < 0 or k >= len(self.deque):
            raise IndexError('Index out of range')
        return self.deque[k]
