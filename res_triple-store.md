# Test insertion and query of triple-stores: 4store, virtuoso, jena/fuseki/tdb

from: ipynb:benchmarking triple-store (svn rev: 6)


## 4store
### iterative insert
usr: 4.779295, sys: 2.742316, usr+sys: 7.521611, real: 38.747595787
usr: 4.971425, sys: 2.868526, usr+sys: 7.839951, real: 41.8456749916
usr: 5.059606, sys: 2.907358, usr+sys: 7.966964, real: 39.6719210148
usr: 4.792507, sys: 2.743436, usr+sys: 7.535943, real: 39.802312851
usr: 4.992187, sys: 2.885235, usr+sys: 7.877422, real: 41.9499938488

### query all
n_res: 5000
usr: 0.549325, sys: 0.044063, usr+sys: 0.593388, real: 0.750782012939
n_res: 5000
usr: 0.322808, sys: 0.036011, usr+sys: 0.358819, real: 0.389111042023
n_res: 5000
usr: 0.3169, sys: 0.018793, usr+sys: 0.335693, real: 0.372928857803
n_res: 5000
usr: 0.337614, sys: 0.021034, usr+sys: 0.358648, real: 0.404145002365
n_res: 5000
usr: 0.270823, sys: 0.017819, usr+sys: 0.288642, real: 0.3332259655



## Virtuoso
### iterative insert
usr: 8.57676, sys: 3.538956, usr+sys: 12.115716, real: 27.1760480404
usr: 8.633939, sys: 3.565519, usr+sys: 12.199458, real: 27.4809589386
usr: 8.486856, sys: 3.493113, usr+sys: 11.979969, real: 25.1185510159
usr: 8.49002, sys: 3.487675, usr+sys: 11.977695, real: 25.0770051479
usr: 8.579587, sys: 3.537318, usr+sys: 12.116905, real: 26.274698019

### query all
n_res: 5000
usr: 0.315929, sys: 0.01818, usr+sys: 0.334109, real: 0.623888969421
n_res: 5000
usr: 0.316845, sys: 0.016928, usr+sys: 0.333773, real: 0.542975902557
n_res: 5000
usr: 0.318844, sys: 0.014725, usr+sys: 0.333569, real: 0.62872004509
n_res: 5000
usr: 0.323579, sys: 0.01587, usr+sys: 0.339449, real: 0.557684898376
n_res: 5000
usr: 0.270773, sys: 0.013585, usr+sys: 0.284358, real: 0.522509098053


## Jena
### iterative insert
usr: 7.425725, sys: 2.662635, usr+sys: 10.08836, real: 30.2433958054
usr: 7.42331, sys: 2.660237, usr+sys: 10.083547, real: 28.2038800716
usr: 7.410488, sys: 2.64566, usr+sys: 10.056148, real: 27.1701090336
usr: 7.422158, sys: 2.649807, usr+sys: 10.071965, real: 25.8813109398
usr: 7.410862, sys: 2.644918, usr+sys: 10.05578, real: 25.2761421204

### query all
n_res: 5000
usr: 0.637748, sys: 0.050797, usr+sys: 0.688545, real: 2.02631688118
n_res: 5000
usr: 0.375376, sys: 0.032983, usr+sys: 0.408359, real: 1.3696808815
n_res: 5000
usr: 0.354195, sys: 0.023708, usr+sys: 0.377903, real: 0.537157058716
n_res: 5000
usr: 0.350666, sys: 0.023551, usr+sys: 0.374217, real: 0.443670988083
n_res: 5000
usr: 0.345224, sys: 0.023318, usr+sys: 0.368542, real: 0.438075780869
