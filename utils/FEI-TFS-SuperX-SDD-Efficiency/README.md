# SuperX-SDD-Efficiency

The `custom.csv` file approximately models the detector efficiency (window transmission + SDD thickness) of the common SuperX detector (G1) from FEI/TFS TEMs.\ 

## How to use it
There is a [guide](https://probesoftware.com/smf/index.php?topic=1225.msg9676#msg9676) by Nicholas Ritchie how to install the custom detector window. The `custom.csv` file in this repository is build from the detector efficiency curve extracted from the publication by [Schlossmacher et al.](https://www.researchgate.net/publication/281539024_Nanoscale_chemical_compositional_analysis_with_an_innovative_STEM-EDX_system) (Fig. 4b).\
Note that (i) the data was extracted from a pixelated figure from the publication, (ii) a simple interpolation was used to build the curve, and (iii) the `custom.csv` "window" is actually the detector window + all other effects that affect the efficiency (such as possible transmission of high-energy x-rays through the 450 µm thick Si detector chip), whereas DTSA-II expects only the window transmission. Regarding (iii), we set the detector's Si thickness in DTSA-II to 10 mm instead of the typical 0.45 mm for SDDs. In this way, the drop-off of detector efficiency after around 10 keV is modeled more correctly. If we instead would use 0.45 mm, DTSA-II will apply an additional dampening of the curve after around 10 keV which we included into the `custom.csv` already.

![grafik](https://github.com/user-attachments/assets/8cd04244-3dad-41c2-b978-74cf790c4700)
