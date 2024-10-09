# TEM_Homogeneous_Series_CompositionDopingMolePerc
# Simulate EDS spectra of a TEM sample with homogeneous composition for different doping levels (mol%) of an added composition/material.
#
# Author: Lukas Gruenewald

import dtsa2.mcSimulate3 as mc
import __builtin__

# Get folder location of this script to store results
from inspect import getsourcefile
import os

### -----------------
### User Parameters
### -----------------

# Directory for results (default: Directory of the script)
# simDir = "path/to/output"
simDir = os.path.dirname(getsourcefile(lambda: 0))

# sample setup
density = 8.0  # sample density
sample = material("GdBa2Cu3O7", density)  # Material
dopant = material("BaHfO3", density)  # dopant material
thickness = 70  # nm (TEM sample thickness)

# series setup (define as manual list or linear array in list)
# Dopant value in !!mole/atomic percent!! added to the sample stoichiometry

# MANUAL
df = [0, 12.0]  # Dopant value in !!mol/atomic percent!!

# LIST
start = 0.5
end = 2
interval = 0.5

steps = (end - start) / interval
# df= [start + x*(end-start)/steps for x in range(int(steps+1))]

# beam / acquisition setup
e0 = 200.0  # keV (primary beam energy)
pc = 1.0  # nA (probe current)
lt = 20.0  # live time
dose = pc * lt  # nA*sec
bs = 1.0  # nm (beam size, FWHM)
det = d101  # Select detector to be used. Must be defined beforehand in DTSA GUI.
# Then get detector number via "listDetectors()" from Command window.

# simulation parameters
nTraj = 10000  # number of trajectories to run
nTrajShow = 200  # number of trajectories to show in image
vmrlEl = 200  # number of electrons for VMRL
imgSize = 2048  # pixel size for images
imgSzNm = (
    thickness * 2
)  # image size/field of view in nm, default is 2x TEM sample thickness
Poisson = True  # Add Poisson count statistics (default True)
charF = True  # include characteristic fluorescence (default True)
bremF = True  # include continuum fluorescence  (default True)

# results options
display_spectrum_in_dtsa = True
print_xray_accumulator_results = False
save_results_to_subfolder = True
save_msa_to_extra_subfolder = True
save_detector_properties = True

### -----------------
### End of User Parameters
### -----------------

# Convert from mol% to fractions
df = [f / 100 for f in df]


# calculate mass of components from stoichiometry
def materialMass(m):
    eles = m.getSortedElements()
    ele_mass = [m.stoichiometry(ele) * ele.getMass() for ele in eles]
    return __builtin__.sum(ele_mass)


mass_sample = materialMass(sample)
mass_dopant = materialMass(dopant)

for i, f in enumerate(df):
    print("-----------------------------------------------------------")
    print("Doping:\t\t\t\t\t" + dopant.getName() + " -> " + sample.getName())
    print(
        "Doping level (mol%):\t"
        + str(f * 100)
        + " ("
        + str(i + 1)
        + "/"
        + str(len(df))
        + ")"
    )

    # create a new sample by adding dopant material
    # we calculate mole fraction from masses of sample/dopant
    c = epq.Composition()
    c.defineByMaterialFraction(
        [sample, dopant],
        [
            (1 - f) * mass_sample / (mass_sample + mass_dopant),
            f * mass_dopant / (mass_sample + mass_dopant),
        ],
    )
    sample_tmp = material(c, density)
    sample_tmp.setName("DopeComp")

    print("Stoichimetry (norm.):\t" + sample_tmp.stoichiometryString())

    print("-----------------------------------------------------------")

    # define the desired transitions for X-ray emission images (up to e0)
    xrts = mc.suggestTransitions(sample_tmp, e0)

    xtraParams = {}
    xtraParams.update(
        mc.configureXRayAccumulators(
            xrts,
            charAccum=charF,
            charFluorAccum=charF,
            bremFluorAccum=bremF,
            printRes=print_xray_accumulator_results,
        )
    )
    xtraParams.update(mc.configureBeam(0, 0, 0, bs * 1.0e-9))  # beam size
    xtraParams.update(
        mc.configureEmissionImages(xrts, imgSzNm * 1.0e-9, imgSize)
    )  # emission images, i.e. DETECTED x-rays (!= generated!)
    # xtraParams.update(mc.configureContinuumImages([[2.5, 5], [0, 2.5]], imgSzNm*1.0e-9, imgSize))
    xtraParams.update(mc.configurePhiRhoZ(imgSzNm * 1.0e-9))
    xtraParams.update(mc.configureTrajectoryImage(imgSzNm * 1.0e-9, imgSize, nTrajShow))
    xtraParams.update(mc.configureVRML(nElectrons=vmrlEl))
    xtraParams.update(mc.configureOutput(simDir))

    # Source: https://github.com/usnistgov/DTSA-II/blob/master/Lib/dtsa2/mcSimulate3.py
    sim = mc.multiFilm(
        [[sample_tmp, thickness * 1e-9]],
        det,
        e0,
        withPoisson=Poisson,
        nTraj=nTraj,
        dose=dose,
        sf=charF,
        bf=bremF,
        xtraParams=xtraParams,
    )

    # Spectrum name
    spec_name = (
        "TEM_"
        + sample.getName().encode("utf-8")
        + "+"
        + str(f * 100)
        + "molP-"
        + dopant.getName().encode("utf-8")
        + "_t="
        + str(thickness)
        + "nm_d="
        + str(dose)
        + "nAs_e0="
        + str(int(e0))
        + "keV_tr="
        + str(nTraj / 1000)
        + "k_det="
        + det.name.encode("utf-8")
    )

    # Only add these if they are not added to the simulation (special case)
    if not charF:
        spec_name += "_noCSF"
    if not bremF:
        spec_name += "_noBSF"

    sim.rename(spec_name)

    # Get latest created folder, typically the one generated by mc.multiFilm above
    all_subdirs = [d for d in os.listdir(simDir) if os.path.isdir(simDir + "/" + d)]
    all_subdirs = [(simDir + "/" + d) for d in all_subdirs]
    latest_subdir = max(all_subdirs, key=os.path.getmtime)

    if save_results_to_subfolder:
        msa_save_dir = latest_subdir + "/results"
        try:
            os.mkdir(msa_save_dir)
        except:
            pass
        sim.save(msa_save_dir + "/" + spec_name + ".msa")

        # Save sample info as html
        html_out = open(
            msa_save_dir + "\SampleInfo_" + spec_name + ".html",
            "w",
        )
        html_out.write(str(sample.toHTMLTable()))
        html_out.close()

    if save_msa_to_extra_subfolder:
        extra_msa_save_dir = simDir + "\msa_Series"
        try:
            os.mkdir(extra_msa_save_dir)
        except:
            pass
        sim.save(extra_msa_save_dir + "/" + spec_name + ".msa")

    if display_spectrum_in_dtsa:
        display(sim)
        print("Total counts: " + str(sim.totalCounts()))

    if save_detector_properties:
        # Save detector properties as
        det_out = open(msa_save_dir + "\Detector_" + spec_name + ".txt", "w")
        det_out.write(det.name.encode("utf-8") + "\n")
        det_out.write(det.detectorProperties.properties.toString().encode("utf-8"))
        det_out.close()

        det_out = open(msa_save_dir + "\Detector_" + spec_name + ".html", "w")
        det_out.write(det.detectorProperties.properties.asHTML().encode("utf-8"))
        det_out.close()
