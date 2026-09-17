import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector
import higgs_signal
import zz_background

# CMS style used for visualisation

hep.style.use("CMS")

fig, ax = plt.subplots()
lum = 35900
c1 = 0.012
c2 = 0.0015

w1 = (lum*c1*higgs_signal.lepton_weights)/ak.sum(higgs_signal.tree["Generator_weight"].array(library="ak"))
w2 = (lum*c2*zz_background.lepton_weights)/ak.sum(zz_background.tree["Generator_weight"].array(library="ak"))



# histograms are weighted for accurate representation

ax.hist([higgs_signal.lepton_mass, zz_background.lepton_mass],
         bins=50,range=(70,250), histtype="step", label=["Higgs Signal", "ZZ Background"],
           color=["blue","red"],
           weights = [ak.full_like(higgs_signal.lepton_mass,w1),ak.full_like(zz_background.lepton_mass,w2)])
ax.set_xlabel("Mass [GeV]")


# bin_edges = np.linspace(70, 250, 50)

# run through np first then pass through







ax.legend()

plt.show()

# Weight = lum * cross section/MC GEN WEIGHTS
# lum * cross section = prob

# signal cross seciton 0.012 pb
# background cross section 1.256 pb

# tree["Generator_weight"].array(library="ak",entry_stop=10000)

