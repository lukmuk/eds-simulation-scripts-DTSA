# SuperX-SDD-Efficiency

The `custom.csv` file approximately models the detector efficiency (window transmission + SDD thickness) of the common SuperX detector (G1) from FEI/TFS TEMs.

## How to use it
There is a [guide](https://probesoftware.com/smf/index.php?topic=1225.msg9676#msg9676) by Nicholas Ritchie how to install the custom detector window. The `custom.csv` file in this repository is build from the detector efficiency curve from the publication by Schlossmacher et al. ([https://doi.org/10.1017/S1551929510000404](https://doi.org/10.1017/S1551929510000404)).\
Note that (i) the data was extracted from a pixelated figure from the publication, (ii) a simple interpolation was used to build the curve, and (iii) the `custom.csv` "window" is actually the detector window + all other effects the affect the efficiency (such as possible transmission of high-energy x-rays through the 450 µm thick Si detector chip), whereas DTSA-II expects only the window transmission. Therefore, there is uncertainty in the detector efficiency.