import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector
import higgs_signal
import zz_background

# CMS style used for visualisation

# hep.style.use("CMS")

fig, ax = plt.subplots()
lum = 35900
c1 = 0.012
c2 = 3.654e-3


w1 = (lum*c1*higgs_signal.lepton_weights["Generator_weight"])/ak.sum(higgs_signal.gen_weight["Generator_weight"])
w2 = (lum*c2*zz_background.lepton_weights["Generator_weight"])/ak.sum(zz_background.gen_weight["Generator_weight"])

print(len(w1))
print(len(higgs_signal.lepton_mass))

print(len(w2))
print(len(zz_background.lepton_mass))

# histograms are weighted for accurate representation



ax.hist([higgs_signal.lepton_mass, zz_background.lepton_mass],
         bins=50,range=(70,250), histtype="step", label=["Higgs Signal", "ZZ Background"],
           color=["blue","red"],
           weights = [w1,w2])
ax.set_xlabel("Mass [GeV]")


# bin_edges = np.linspace(70, 250, 50)

# run through np first then pass through







ax.legend()

plt.show()

# Weight = lum * cross section/MC GEN WEIGHTS
# lum * cross section = prob
