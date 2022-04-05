class Series:
    def __init__(self, item, selfType:type=None):
        #print(f'creating series from item {item}') #debug
        
        if type(item) is set or type(item) is tuple:
            item = list(item)
        elif type(item) is str or type(item) is int or type(item) is float:
            if selfType and type(item) is not selfType:
                raise TypeError(f'type of given item {item} is not the same as given type {selfType}')
                
            self.value = item
            self.type = type(item)
            self.next = None
            
        if type(item) is list:
            if selfType and type(item[0]) is not selfType:
                raise TypeError(f'type of given item {item[0]} is not the same as given type {selfType}')
                
            for subItem in item:
                if type(subItem) is not type(item[0]):
                    raise TypeError('container passed to series must be of uniform type')
                    
            self.type = type(item[0])
            self.value = item[0]
            if len(item) > 1:
                self.next = Series(item[1:])
            else:
                self.next = None

    def __len__(self):
        if self.value is not None:
            length = 1
            done = False
            current = self
            while current.next is not None:
                length += 1
                current = current.next

            return length
            
        else:
            return 0

    @property
    def last(self):
        current = self
        done = False
        while current.next:
            current = current.next

        return current

    def __getitem__(self, index:int):
        if index >= len(self) or -index > len(self):
            raise IndexError('series index out of range')

        current = self
        if index >= 0:
            for i in range(index):
                current = current.next
        else:
            for i in range(len(self) - abs(index)):
                current = current.next

        return current.value

    def __setitem__(self, index:int, value):
        if index >= len(self):
            raise IndexError('series index out of range')

        current = self
        for i in range(index):
            current = current.next

        current.value = value

    def __iter__(self):
        self.iterIndex = -1
        return self

    def __next__(self):
        self.iterIndex += 1
        if self.iterIndex >= len(self):
            raise StopIteration
            
        return self[self.iterIndex]

    def __add__(self, other):
        result = self.deepcopy()
        
        if type(other) is Series:
            if self.type != other.type:
                raise TypeError(f'cannot add series of type {other.type} to series of type {self.type}')

            result.last.next = other
            
        elif type(other) is self.type:
            result.last.next = Series(other)
            
        else:
            raise TypeError(f'cannot add object of type {type(other)} to series of type {self.type}')

        return result

    def __radd__(self, other):
        if type(other) is self.type:
            output = Series(other)
            output.next = self.deepcopy()
        else:
            raise IndexError(f'cannot add series of type {self.type} to object of type {type(other)}')

        return output

    def __iadd__(self):
        if type(other) is Series:
            if self.type != other.type:
                raise TypeError(f'cannot add series of type {other.type} to series of type {self.type}')

            self.last.next = other
            
        elif type(other) is self.type:
            self.last.next = Series(other)
            
        else:
            raise TypeError(f'cannot add object of type {type(other)} to series of type {self.type}')

        return self

    def __str__(self):
        output = '['
        for i, item in enumerate(self):
            output += str(item)
            
            if i != len(self) - 1:
                output += ', '

        output += ']'
        return output

    def __list__(self):
        return [item for item in self]

    def copy(self):
        output = Series(self[0])
        current = output
        for i in range(1, len(self)):
            current.next = Series(self[i])
            current = current.next

        return output

    def deepcopy(self):
        try:
            output = Series(self[0].deepcopy())
        except AttributeError:
            output = Series(self[0])
            current = output
            for i in range(1, len(self)):
                current.next = Series(self[i])
                current = current.next
        else:
            current = output
            for i in range(1, len(self)):
                current.next = Series(self[i].deepcopy())
                current = current.next

        return output