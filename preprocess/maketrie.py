
# Dictionary initializer

#For now, let's represent this as a simple trie


dictfile = '../csw12.txt'

fh = open(dictfile, 'r')
wordlist = [w.replace("\n", "").upper() for w in fh.readlines()]
fh.close()


_end = '_end_'

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
            current_dict[_end] = _end
    return root

def in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter in current_dict:
            current_dict = current_dict[letter]
        else:
            return False
    else:
        if _end in current_dict:
            return True
        else:
            return False


#TESTING
    
d1 = make_trie(['foo', 'bar', 'baz', 'barz'])
d2 = make_trie(wordlist[:10])

print