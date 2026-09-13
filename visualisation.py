import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector
import higgs_signal
import zz_background

fig, ax = plt.subplots()

ax.hist([higgs_signal.lepton_mass, zz_background.muons_mass], bins=50, histtype="step", label=["Lepton pT", "ZZ Background"], color=["blue","red"], density=True)
hep.style.use("CMS")
ax.set_xlabel("Mass [GeV]")
ax.legend()

plt.show()
