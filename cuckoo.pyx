#
# cuckoo.pyx
#

"""Cuckoo Hash library

This module provides a simple interface to the Cuckoo Hash,
an efficient sparse array implementation.

Cuckoo Hashing was proposed by Pagh and Rodler (2001). The idea is to
build a dictionary data structure with two hash tables and two different
hash functions.

SEE ALSO
Rasmus Pagh and Flemming Friche Rodler. 2001. Cuckoo Hashing, Proceedings
of ESA 2001, Lecture Notes in Computer Science, vol. 2161.

Chuleerat Jaruskulchai and Canasai Kruengkrai. 2002. Building Inverted
Files Through Efficient Dynamic Hashing. Proceedings of the Fifth National
Computer Science and Engineering Conference (NCSEC-2002).

L Devroye, P Morin. 2003. Cuckoo hashing: Further analysis. Information 
Processing Letters.


This Python interface is to CKHash 0.4.2:
 * Copyright (C) 2005-2008 Thai Computational Linguistics Laboratory (TCL),
 * National Institute of Information and Communications Technology (NICT)
 * Written by Canasai Kruengkrai <canasaiREMOVETHIS@gmail.com>
"""

__author__ = 'Jose Nazario <jose@monkey.org>'
__copyright__ = 'Copyright (c) 2008 Jose Nazario'
__license__ = 'GPL2'
__url__ = ''
__version__ = '1.0-0.4.2'

cdef extern from "../cuckoo_hash/cuckoo_hash.h":
    pass

cdef extern from "Python.h":
    void Py_INCREF(object o)
    void Py_DECREF(object o)

cdef extern from *:
    cdef struct CKHash_Cell_t:
        unsigned char *key
        int value        

    cdef struct CKHash_Table_t:
        unsigned int size
        unsigned int table_size            
        int shift                      
        unsigned int min_size         
        unsigned int mean_size       
        unsigned int max_chain      
        CKHash_Cell_t *T1          
        CKHash_Cell_t *T2         
        int function_size        
        int *a1                 
        int *a2                

    ctypedef int (*applyfunc)(char *key, int value, void *arg)

    CKHash_Table_t *ckh_construct_table(int min_size)
    int ckh_lookup(CKHash_Table_t *D, char *key)
    int ckh_insert (CKHash_Table_t *D, char *key, int value)
    int ckh_delete(CKHash_Table_t *D, char *key)
    int ckh_get(CKHash_Table_t *D, char *key, int *ret_value)
    void cuckoo_apply(CKHash_Table_t *D, applyfunc cb, void *arg)
    int cuckoo_table_size(CKHash_Table_t *D)
    CKHash_Table_t *ckh_destruct_table(CKHash_Table_t *D)

cdef int _cuckoo_get_keys(char *key, int val, void *arg):
        lst = <object>arg
        lst.append(key)

cdef int _cuckoo_get_values(char *key, int val, void *arg):
        lst = <object>arg
        lst.append(<object>val)

cdef int _cuckoo_get_items(char *key, int val, void *arg):
        lst = <object>arg
        lst.append((key, <object>val))


cdef class cuckoohash:
    """cuckoohash() -> new empty Cuckoo Hash table

    cuckoohash(size=n) -> Create a new Cuckoo Hash table with 
        initial size n. 
        Note: the table will automatically grow as needed.
    cuckoohash(seq=seq) -> Create a new Cuckoo Hash table as if via:
        c = cuckoohash()
        for k, v in seq: c[k] = v

    """

    cdef CKHash_Table_t *table

    def __init__(self, size=1024, seq=[]):
        self.table = ckh_construct_table(size)
        if len(seq) > 0:
            for k, v in seq: self.insert(k, v)

    def __del__(self):
        ckh_destruct_table(self.table)

    def __len__(self):
        return cuckoo_table_size(self.table)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def delete(self, char *key):
        """delete(key)

        delete the specified key"""
        cdef int ret
        ckh_get(self.table, key, &ret)
        Py_DECREF(<int><void *>ret)
        ckh_delete(self.table, key)

    def lookup(self, char *key):
        """lookup(key)

        test to see if the key is present in the hash table"""
        return ckh_lookup(self.table, key)

    def has_key(self, char *key):
        """has_key(key)

        a synonym for lookup(key)"""
        return self.lookup(key)

    def insert(self, char *key, object val):
        """insert(key, val)

        insert the key:value pair into the hash table.
	key - a string
	val - any Python object"""
        Py_INCREF(val)
        ckh_insert(self.table, key, <int><void *>val)

    def get(self, char *key):
        """get(key)

        retriee the value for the specified key"""
        cdef int ret
        ckh_get(self.table, key, &ret)
        return <object>ret

    cdef object __cuckoo_gather(self,
                                int gatherfunc(char *key, int val, void *arg)):
        l = []
        cuckoo_apply(self.table, gatherfunc, <void *>l)
        return l

    def keys(self):
        """keys() - the list of keys for the hash table"""
        return self.__cuckoo_gather(_cuckoo_get_keys)

    def values(self):
        """values() - the list of values held in the hash table"""
        return self.__cuckoo_gather(_cuckoo_get_values)

    def items(self):
        """C.items() -> list of (key, value) pairs in C"""
        return self.__cuckoo_gather(_cuckoo_get_items)

    def __iter__(self):
        return iter(self.keys())

    def iteritems(self):
        """C.iteritems() -> iterate over the (key, value) items in C"""
        return iter(self.items())

    def iterkeys(self):
        """C.iterkeys() -> iterate over the keys in C"""
        return iter(self)

    def itervalues(self):
        """C.itervalues() -> iterate over the value in C"""
        return iter(self.values())

