#include <sys/types.h>
#include "cuckoo_hash/cuckoo_hash.h"

#ifndef NULL
#define NULL    0
#endif  /* NULL */


int
cuckoo_table_size(CKHash_Table *D)
{
	/* number of actual elements in the table, NOT the size of the table */
	return (int)(D->size);
}

typedef int (*applyfunc)(char *key, int value, void *arg);

void 
cuckoo_apply(CKHash_Table *D, applyfunc cb, void *arg)
{
	/* walk the table and perform a callback on elements */
	unsigned int i;
	int ret;

        for (i = 0; i < D->table_size; i++) {
                if (D->T1[i].key != NULL) {
			cb(D->T1[i].key, D->T1[i].value, arg);
                }
                if (D->T2[i].key != NULL) {
			cb(D->T2[i].key, D->T2[i].value, arg);
		}
        }
	
}
