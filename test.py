import unittest
import cuckoo

class TestCuckooHash(unittest.TestCase):
    def setUp(self):
        self.c = cuckoo.cuckoohash(10)

    def testInsert(self):
        # basic integer assignments
        self.assertEqual(self.c.insert('a', 100), None)
        self.c.delete('a')

        # insert to a python object by direct value
        self.c.insert('a', {'foo': 'bar'})
        self.assertEqual(self.c.get('a'), {'foo': 'bar'})
        self.c.delete('a')

        # insert to a python object by reference
        m = {'foo': 'bar'}
        self.c.insert('a', m)
        self.assertEqual(self.c.get('a'), {'foo': 'bar'})
        self.assertEqual(self.c.get('a'), m)
        self.c.delete('a')

        # test reinserting the same value
        self.c.insert('a', 'one')
        self.assertEqual(self.c.get('a'), 'one')
        x = self.c.insert('a', 'two')
        self.assertEqual(x, None)
        self.assertEqual(self.c.get('a'), 'two')
        self.c.delete('a')

        # test __ssetitem__
        self.c['z'] = 'Foobar'
        self.assertEqual(self.c.get('z'), 'Foobar')

    def testDelete(self):
        self.c = cuckoo.cuckoohash(10)
        self.c.insert('a', 'Foobar')
        self.assertEqual(self.c.has_key('a'), True)
        self.c.delete('a')
        self.assertEqual(self.c.has_key('a'), False)

        # test __delitem__
        self.c.insert('a', 'Foobar')
        self.assertEqual(self.c.has_key('a'), True)
        del self.c['a']
        self.assertEqual(self.c.has_key('a'), False)

    def testGet(self):
        self.c.insert('a', 100)
        self.assertEqual(self.c.get('a'), 100)
        self.assertEqual(self.c['a'], 100)

    def testLookup(self):
        self.c.insert('a', 100)
        self.assertEqual(self.c.lookup('a'), True)
        self.c.delete('a')
        self.assertEqual(self.c.lookup('a'), False)

    def testHaskey(self):
        self.c.insert('a', 100)
        self.assertEqual(self.c.has_key('a'), True)
        self.c.delete('a')
        self.assertEqual(self.c.has_key('a'), False)

    def testKeys(self):
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})
        
        k = list(self.c.keys())
        k.sort()
        keys = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(k, keys)


    def testValues(self):
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})

        v = list(self.c.values())
        v.sort()
        values = [{'b': 'bar'},
                  {'c': 10},
                  {'d': 20},
                  {'e': 'g'},
                  {'a': 100, 'b': 22}]
        self.assertEqual(v, values)

    def testSize(self):
        del(self.c)
        self.c = cuckoo.cuckoohash()
        self.assertEqual(len(self.c), 0)
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})
        self.assertEqual(len(self.c), 5)
        self.c.delete('a')
        self.assertEqual(len(self.c), 4)

    def testIteritems(self):
        self.c = cuckoo.cuckoohash()
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})
        values = [{'b': {'b': 'bar'}},
                  {'c': {'c': 10}},
                  {'d': {'d': 20}},
                  {'e': {'e': 'g'}},
                  {'a': {'a': 100, 'b': 22}}]
        for k, v in self.c.iteritems():
            x = {k: v}
            self.assertEqual(x in values, True)
            values.remove(x)
        self.assertEqual(len(values), 0)

    def testIterkeys(self):
        self.c = cuckoo.cuckoohash()
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})
        values = [{'b': {'b': 'bar'}},
                  {'c': {'c': 10}},
                  {'d': {'d': 20}},
                  {'e': {'e': 'g'}},
                  {'a': {'a': 100, 'b': 22}}]
        keys = ['a', 'b', 'c', 'd', 'e']
        for k in self.c.iterkeys():
            self.assertEqual(k in keys, True)
            keys.remove(k)
        self.assertEqual(len(keys), 0)

    def testItervalues(self):
        self.c = cuckoo.cuckoohash()
        self.c.insert('a', {'a': 100, 'b': 22})
        self.c.insert('b', {'b': 'bar'})
        self.c.insert('c', {'c': 10})
        self.c.insert('d', {'d':20})
        self.c.insert('e', {'e': 'g'})
        values = [{'b': 'bar'},
                  {'c': 10},
                  {'d': 20},
                  {'e': 'g'},
                  {'a': 100, 'b': 22}]
        for v in self.c.itervalues():
            self.assertEqual(v in values, True)
            values.remove(v)
        self.assertEqual(len(values), 0)

if __name__ == '__main__':
    unittest.main()

