from distutils.core import setup, Extension

setup(
    name = "cuckoo",
    version = "1.0-0.4.2",
    author = "Jose Nazario",
    author_email = "jose@monkey.org",
    license = "GPL2",
    long_description = " ",
    ext_modules = [Extension(
        "cuckoomodule",
        sources = ["cuckoo.c", "cuckoo_util.c"],
        include_dirs = [".."],
        libraries = ["ckhash"],
        library_dirs = ["../cuckoo_hash"]
        ) ],
    url = "http://code.google.com/p/pycuckoohash/",
)
    
