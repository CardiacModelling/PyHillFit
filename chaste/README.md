# Chaste code

For performing the uncertainty propagation simulations.

## Pre-requisites

 * `Chaste` - from www.github.com/Chaste/Chaste
 * `ApPredict` - from www.github.com/Chaste/ApPredict

The files in this folder should be copied into `ApPredict/test`.

## Contents

 * `samples/*` - contains samples from hierarchical inference results (based on running the scripts in other folders).
 * `drug_list.txt` - a simple text file telling the Chaste code which concentrations to use for which compounds.
 * `CrumbDrugList.hpp` - a helper class to read in `drug_list.txt`
 * `CrumbDataReader.hpp` - a helper class to read in the samples from `samples/*`
 * `TestCrumbPredictions.hpp` - the main test to run.

## Running the simulations

Should be as simple as getting a copy of Chaste and ApPredict, e.g.

```
git clone https://github.com/Chaste/Chaste.git
git clone https://github.com/Chaste/ApPredict.git
cd Chaste/projects
ln -s ../../ApPredict
```
and then copy these files into
```
ApPredict/test/
```
and run the simulations from the Chaste folder, with:
```
scons cl=1 b=GccOptNative projects/ApPredict/test/TestCrumbPredictions.hpp
```










