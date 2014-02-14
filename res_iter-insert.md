# Test iterative insertions and query

FOR *5000 iterative inserts*, 5 loops

*NOTE:* query might not be accurate, has it sometimes report 5000 or 5 x 5000 items

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


## PostgreSQL (SQLAlchemy)
### iterative inserts
usr: 3.479862, sys: 0.523029, usr+sys: 4.002891, real: 11.5393021107
usr: 3.293352, sys: 0.501966, usr+sys: 3.795318, real: 10.5881390572
usr: 3.376238, sys: 0.51332, usr+sys: 3.889558, real: 11.0423688889
usr: 3.443225, sys: 0.52494, usr+sys: 3.968165, real: 13.108697176
usr: 3.365698, sys: 0.508632, usr+sys: 3.87433, real: 10.1761519909

### query all
n_res: 5000
usr: 3.610292, sys: 0.142812, usr+sys: 3.753104, real: 4.41579508781
n_res: 5000
usr: 2.309419, sys: 0.087788, usr+sys: 2.397207, real: 2.75843715668
n_res: 5000
usr: 2.103566, sys: 0.073552, usr+sys: 2.177118, real: 2.58719015121
n_res: 5000
usr: 2.112045, sys: 0.062383, usr+sys: 2.174428, real: 2.21936488152
n_res: 5000
usr: 2.146364, sys: 0.072386, usr+sys: 2.21875, real: 2.32225108147


## SQLite (SQLAlchemy)
### iterative inserts
usr: 9.442218, sys: 6.324217, usr+sys: 15.766435, real: 71.6462140083
usr: 9.641125, sys: 6.635341, usr+sys: 16.276466, real: 75.9487550259
usr: 9.565106, sys: 6.617006, usr+sys: 16.182112, real: 86.3603260517
usr: 9.658567, sys: 6.856925, usr+sys: 16.515492, real: 88.330603838
usr: 9.515457, sys: 6.644232, usr+sys: 16.159689, real: 93.9919419289


### query all
n_res: 5000
usr: 3.552035, sys: 0.14743, usr+sys: 3.699465, real: 3.93816900253
n_res: 5000
usr: 2.265173, sys: 0.087942, usr+sys: 2.353115, real: 2.94849991798
n_res: 5000
usr: 2.090545, sys: 0.08051, usr+sys: 2.171055, real: 2.71408605576
n_res: 5000
usr: 2.142618, sys: 0.075125, usr+sys: 2.217743, real: 2.37443304062
n_res: 5000
usr: 2.129594, sys: 0.068733, usr+sys: 2.198327, real: 2.43790507317

## PostgreSQL (standalone plugin)
### iterative inserts
usr: 0.922784, sys: 0.290819, usr+sys: 1.213603, real: 6.52835297585
usr: 0.98375, sys: 0.300525, usr+sys: 1.284275, real: 8.06845211983
usr: 0.921418, sys: 0.290806, usr+sys: 1.212224, real: 6.20144820213
usr: 0.905467, sys: 0.288199, usr+sys: 1.193666, real: 5.84414100647
usr: 0.917643, sys: 0.288443, usr+sys: 1.206086, real: 5.55856895447


### query all
n_res: 5000
usr: 2.819751, sys: 0.061112, usr+sys: 2.880863, real: 5.82864189148
n_res: 5000
usr: 1.520889, sys: 0.029675, usr+sys: 1.550564, real: 4.52252197266
n_res: 5000
usr: 1.576241, sys: 0.027604, usr+sys: 1.603845, real: 4.8151550293
n_res: 5000
usr: 1.542, sys: 0.03296, usr+sys: 1.57496, real: 4.10985517502
n_res: 5000
usr: 1.602513, sys: 0.031202, usr+sys: 1.633715, real: 5.04405593872


## SQLite (standalone plugin)
### iterative inserts
usr: 2.265674, sys: 4.702799, usr+sys: 6.968473, real: 51.3567528725
usr: 2.266411, sys: 4.832428, usr+sys: 7.098839, real: 63.4678750038
usr: 2.360517, sys: 6.054702, usr+sys: 8.415219, real: 74.3862631321
usr: 2.326928, sys: 6.329106, usr+sys: 8.656034, real: 85.4042901993
usr: 2.416501, sys: 6.478899, usr+sys: 8.8954, real: 88.416574955


### query all
n_res: 5000
usr: 2.819751, sys: 0.061112, usr+sys: 2.880863, real: 5.82864189148
n_res: 5000
usr: 1.520889, sys: 0.029675, usr+sys: 1.550564, real: 4.52252197266
n_res: 5000
usr: 1.576241, sys: 0.027604, usr+sys: 1.603845, real: 4.8151550293
n_res: 5000
usr: 1.542, sys: 0.03296, usr+sys: 1.57496, real: 4.10985517502
n_res: 5000
usr: 1.602513, sys: 0.031202, usr+sys: 1.633715, real: 5.04405593872
