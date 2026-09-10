import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector




dummyfile1 = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/ZZto4L_EWK_PolarizedZ0Z0_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2550000/26A3DE6B-7295-F241-A2A7-54C94DCD1926.root")

dummyfile2 = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16MiniAODv2/GluGluHToZZTo4L_M125_CP5TuneDown_13TeV_powheg2_JHUGenV7011_pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/2540000/322B314A-B34D-764A-BCF5-2088CF0ACA1B.root")

# print(dummyfile2["Events;1"].keys())


inspection2 = dummyfile1["Events;1"]
# print(inspection2.keys())

muoninspect = inspection2.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass"], entry_stop = 10000, library = "ak")
mask1 = (abs(muoninspect["Muon_eta"]) < 2.4) & (muoninspect["Muon_pt"] > 5)
fmask1 = muoninspect[mask1]

filtered2 = fmask1[ak.num(fmask1["Muon_pt"]) == 4]
print(filtered2)




muons_p = vector.zip({
    "pt": filtered2["Muon_pt"],
    "eta": filtered2["Muon_eta"],
    "phi": filtered2["Muon_phi"],
    "mass": filtered2["Muon_mass"]})

sum_muons = muons_p[:, 0] + muons_p[:, 1] + muons_p[:, 2] + muons_p[:, 3]
muons_mass = sum_muons.mass

fig, ax = plt.subplots()

ax.hist([muons_mass,], bins=50, histtype="step", label="Muon pT", color="blue")
hep.style.use("CMS")


plt.show()
