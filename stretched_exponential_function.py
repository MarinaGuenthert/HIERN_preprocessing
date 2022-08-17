import numpy as np

from lmfit.model import Model, save_model


def mystretchedexponential(x, tau, b):
    return np.exp((-1.0)*(x/tau)**(1.0/b))

stretched = Model(mystretchedexponential)
pars = stretched.make_params(tau = 100, b = 0.5)


# sinemodel = Model(mysine)
# pars = sinemodel.make_params(amp=1, freq=0.25, shift=0)

save_model(stretched, 'stretched.sav')
# <end examples/doc_model_savemodel.py>