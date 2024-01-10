# Iterative Percentile Estimation

**Problem to solve**

A set of N data observations are to be created.  You are
unable to store the N observations, but you need estimates of percentiles.

**A Solution**

* Keep an estimate of the percentile starting with the first data observations.
* For each generated data observtaion compare to the current estimate

  * if current observation is less than the current estimate:
    * update estimate to a slightly smaller value
  * if current observation is greater then the current estimate:
    * update estimate to a slightly larger value
  * if current observation is equal to the the current estimate
    * do nothing

The script `ipe.py` defines a class tracking this information and has some
additional values which could be used to tracking other statistics.

## Use
The needed modules are defined in the conda envrionment file `environment.yml`

Get the usage for the proof of concept program:

```
python ipe.py -h
```

Example use for finding the 90th percentile from 1 million observations

```bash
$ python ipe.py --N=1000000 --percentile=0.9
|████████████████████████████████████████| 1000000/1000000 [100%] in 2.6s (381514.59/s)
After 1000001 data observations
  Estiamte of the mean 2.8640499937785764
  Expected value: 2.86

  Estiamte of the standard deviation 3.1881617044724093
  Expected value: 3.188

  Estiamte of the 90.0th percentile is 6.938094258080731
  Expected 90.0th percentile: 6.945586390956185
```
