all: cuckoo.c cuckoo_util.c
	python setup.py build

cuckoo.c: cuckoo.pyx
	pyrexc cuckoo.pyx

test: test.py
	python test.py

install: all test
	python setup.py install

clean:
	rm -f *.o *.so *.pyc *.pyo
	rm -rf build
