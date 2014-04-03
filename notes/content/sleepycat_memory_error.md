Title: Sleepycat memory error
Date: 2014-03-04 10:34
Category: debug
Tags: sleepycat, error
Author: Vincent

# The problem
When trying to do some benchmarks with Sleepycat, the following error was raised:

> Cannot allocate memory -- BDB2034 unable to allocate memory for mutex; resize mutex region

## The solution
To solve this, go inside the Sleepycat database folder, and do a `db_recover`.

## Origin of the problem
The problem probably came from the lack of `graph.close()` after opening a
Sleepycat database in RDFLib with `graph.open()`.

# The second problem
Another error occured:

> bsddb.db.DBRunRecoveryError: (-30973, 'DB_RUNRECOVERY: Fatal error, run database recovery -- PANIC: Invalid argument')

## Solution
Same as before, run `db_recover` in the sleepycat folder.
