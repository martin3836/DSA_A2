class HashTable:
    def __init__(self, capacity=32):
        """
        Initializes the hash table with a given capacity.

        Parameters:
        capacity (int, optional): The initial capacity of the hash table. Default is 32.

        Attributes:
        _capacity (int): The current capacity of the hash table.
        table (list of list of tuple): The hash table, where each index contains a list of key-value pairs.
        size (int): The number of key-value pairs in the hash table.
        """
        self._capacity = capacity 
        self.table = [None] * self._capacity 
        self.size = 0 

    def _hash(self, key):
        """
        Hashes the key and maps it to an index within the table's capacity.

        Parameters:
        key (any): The key to be hashed.

        Returns:
        int: The index within the table's capacity.
        """
        return hash(key) % self._capacity

    def _resize(self):
        """Resizes the hash table"""
        old_table = self.table
        self._capacity *= 2
        self.table = [None] * self._capacity
        self.size = 0  

        for chain in old_table:
            if chain:
                for key, value in chain:
                    self.insert(key, value)

    def insert(self, key, value):
        """
        Inserts a new key-value pair into the hash table.

        Parameters:
        key (any): The key to be inserted.
        value (any): The value to be associated with the key.

        Returns:
        bool: False if the key already exists in the hash table, True otherwise.
        """
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = [] 

        for k, v in self.table[index]:
            if k == key:
                return False

        self.table[index].append((key, value))
        self.size += 1
        if self.size / self._capacity > 0.7:
            self._resize()

        return True

    def modify(self, key, value):
        """
        Modifies the value of an existing key in the hash table.

        Parameters:
        key (any): The key whose value is to be modified.
        value (any): The new value to be associated with the key.

        Returns:
        bool: True if the key was found and the value was modified, False otherwise.
        """
        index = self._hash(key)
        if self.table[index] is None:
            return False

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return True

        return False

    def remove(self, key):
        """
        Removes the key-value pair associated with the given key.

        Parameters:
        key (any): The key to be removed.

        Returns:
        bool: True if the key was found and removed, False otherwise.
        """
        index = self._hash(key)
        if self.table[index] is None:
            return False

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.size -= 1
                if not self.table[index]:
                    self.table[index] = None
                return True

        return False

    def search(self, key):
        """Searches for the value associated with the key."""
        index = self._hash(key)
        if self.table[index] is None:
            return None

        for k, v in self.table[index]:
            if k == key:
                return v

        return None

    def capacity(self):
        """Returns the number of slots in the table."""
        return self._capacity

    def __len__(self):
        """Returns the number of records stored in the table."""
        return self.size
