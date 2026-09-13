import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector




dummyfile1 = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/ZZto4L_EWK_PolarizedZ0Z0_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2550000/26A3DE6B-7295-F241-A2A7-54C94DCD1926.root")

dummyfile2 = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/GluGluHToZZTo4L_M125_CP5TuneDown_13TeV_powheg2_JHUGenV7011_pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2540000/17C2B325-DBA6-8145-9237-5A1859E9C2BA.root")

inspection1 = dummyfile1["Events;1"]
# print(inspection2.keys())

muoninspect = inspection1.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], entry_stop = 10000, library = "ak")
mask = (abs(muoninspect["Muon_eta"]) < 2.4) & (muoninspect["Muon_pt"] > 5)
fmask1 = muoninspect[mask]

filtered1 = fmask1[(ak.num(fmask1["Muon_pt"]) == 4) & (ak.sum(fmask1["Muon_charge"], axis=1) == 0)]
print(filtered1)

muons_p1 = vector.zip({
    "pt": filtered1["Muon_pt"],
    "eta": filtered1["Muon_eta"],
    "phi": filtered1["Muon_phi"],
    "mass": filtered1["Muon_mass"]})

sum_muons1 = muons_p1[:, 0] + muons_p1[:, 1] + muons_p1[:, 2] + muons_p1[:, 3]
muons_mass = sum_muons1.mass

fig, ax = plt.subplots()

# print(dummyfile2["Events;1"].keys())

inspection2 = dummyfile2["Events;1"]

muoninspect2 = inspection2.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], entry_stop = 10000, library = "ak")

mask2 = (abs(muoninspect2["Muon_eta"]) < 2.4) & (muoninspect2["Muon_pt"] > 5)
fmask2 = muoninspect2[mask2]

filtered2 = fmask2[(ak.num(fmask2["Muon_pt"]) == 4) & (ak.sum(fmask2["Muon_charge"], axis=1) == 0)]

muons_p2 = vector.zip({
    "pt": filtered2["Muon_pt"],
    "eta": filtered2["Muon_eta"],
    "phi": filtered2["Muon_phi"],
    "mass": filtered2["Muon_mass"]})

sum_muons2 = muons_p2[:, 0] + muons_p2[:, 1] + muons_p2[:, 2] + muons_p2[:, 3]
muons_mass2 = sum_muons2.mass

ax.hist([muons_mass, muons_mass2], bins=50, histtype="step", label=["Muon pT", "Muon pT 2"], color=["blue", "red"], density=True)
hep.style.use("CMS")
ax.set_xlabel("Mass [GeV]")
ax.legend()

plt.show()



# Tasks
# 2e2m filter
# Add statistics to correct histogram
# delta R = sqrt((eta1-eta2)^2 + (phi1-phi2)^2)
# In the dense environment of a heavy-ion collision, overlapping tracks and high particle multiplicities can make accurate tracking difficult, 
# necessitating sophisticated algorithms and detector technologies. High tracking efficiency ensures
#  that the measured particle yields and spectra accurately reflect the true particle production in the collision.
# source: cern open data atlas documentation
# 33.40±0.30 fb-1
# 10 fb^-1

