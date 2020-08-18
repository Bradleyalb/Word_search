class Trie:
    def __init__(self):
        """
        Initialize an empty trie.
        """
        self.value = 1
        self.children = {}
        self.type = None

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.type != type(key):
            raise TypeError
        if len(key) == 0:
            if self.value == None:
                raise KeyError
            return self.value
        else:#Recurse on getItem
            return self.children[key[0:1]][key[1:]]


    def __setitem__(self, key, value):
        """ 
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        #print(key)
        if self.type == None:
            self.type = type(key)
        elif self.type != type(key):
            raise TypeError
        if len(key) == 0:
            self.value = value
        else:
            if key[0:1] not in self.children:    
                self.children[key[0:1]] = Trie()
            self.children[key[0:1]][key[1:]] = value

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self[key] = None

    def __contains__(self, key):
        """
        Return True if key is in the trie and has a value, return False otherwise.
        """
        try:
            self[key]
        except:
            return False
        return True



    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator or iterator!
        """
        if self.value != None: 
            yield self.value#Yield a value if not none
        for child in self.children:
            for c in self.children[child]:#Recurses on iterator
                if isinstance(c,tuple):
                    key = c[0]
                    key = child + key
                    yield (key,c[1])
                else:#First time returning
                    yield (child,c)