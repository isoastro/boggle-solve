class Trie:
    def __init__(self, value=None, end=False):
        '''
        Recursive implementation of a trie

        All methods that iterate through the trie to add or look up run recursively
        '''
        self._value = value
        self._end = False
        self._children = {}


    def __repr__(self):
        return 'Trie(value={self._value}, end={self._end}, children={0:})'\
               .format(sorted(self._children.keys()), self=self)


    def add_child(self, child: 'Trie'):
        '''Add a child sub-trie'''
        if child._value in self._children:
            return
        self._children[child._value] = child


    def mark_end(self):
        '''
        Mark the current root node of the trie as an end node

        This indicates that the nodes leading up to this one make a full sequence.
        This node may have children still
        '''
        self._end = True


    @property
    def end(self):
        '''Returns true for end nodes'''
        return self._end


    def add_iterable(self, iterable):
        '''
        Add any iterable sequence to the trie

        Recursively add smaller and smaller subsequences
        '''
        it = iter(iterable)
        try:
            item = next(it) # Consume an item
        except StopIteration:
            # We're done
            self.mark_end()
            return

        # Create sub-trie
        self.add_child(Trie(value=item))
        self._children[item].add_iterable(it)


    def find_prefix(self, prefix):
        '''
        Recursively search through the trie to find a prefix

        Runs in O(N), returning early if the prefix of this prefix does not exist
        '''
        it = iter(prefix)
        try:
            item = next(it)
        except StopIteration:
            return self # End of the line

        try:
            return self._children[item].find_prefix(it)
        except KeyError:
            return None # Prefix does not exist


    def has_sequence(self, seq):
        '''Returns True if the trie contains the entire sequence, ending on an end node'''
        try:
            return self.find_prefix(seq)._end # Is an end node?
        except AttributeError:
            return False # Prefix doesn't exist so therefore word doesn't
        

    # Is the prefix contained in the trie?
    # That is, does a node containing each letter exist in the trie?
    def has_prefix(self, prefix):
        '''
        Returns True if the prefix can be found in the trie

        Does not indicate if the prefix ends on an end node
        '''
        return self.find_prefix(prefix) is not None


    def __contains__(self, prefix):
        '''Helper for 'x in trie' calls'''
        return bool(self.find_prefix(prefix))


    def __str__(self, level=0, indent='  '):
        '''Chain together string representations of each child trie'''
        ret = ''
        for item, child in sorted(self._children.items()):
            ret += indent * level + str(child._value)
            if child._end:
                ret += '*' # Flag as end node
            ret += '\n'
            ret += child.__str__(level=level+1)
        return ret
