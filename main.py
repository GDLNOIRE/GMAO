import pandas as pd
import os
from pyagrum_extra import gum


ot_odr_filename = os.path.join(".", "donnees/OT_ODR.csv.bz2")
ot_odr_df = pd.read_csv(ot_odr_filename,
                        compression="bz2",
                        sep=";")

equipements_filename = os.path.join(".", 'donnees/EQUIPEMENTS.csv')
equipements_df = pd.read_csv(equipements_filename,
                             sep=";")

#permet de décrire nos variables suivantes : 
var_sig = ["SIG_ORGANE", "SIG_CONTEXTE", "SIG_OBS"]
ot_odr_df[var_sig].describe()

var_sys = ["SYSTEM_N1", "SYSTEM_N2", "SYSTEM_N3"]
ot_odr_df[var_sys].describe()

var_odr = ["TYPE_TRAVAIL", "ODR_LIBELLE"]
ot_odr_df[var_odr].describe()

var_cat = ['ODR_LIBELLE', 'TYPE_TRAVAIL',
           'SYSTEM_N1', 'SYSTEM_N2', 'SYSTEM_N3', 
           'SIG_ORGANE', 'SIG_CONTEXTE', 'SIG_OBS', 'LIGNE']
for var in var_cat:
    ot_odr_df[var] = ot_odr_df[var].astype('category')

ot_odr_df.info()

var_to_model = ["SYSTEM_N1", "SIG_OBS"]

var_bn = {}
for var in var_to_model:
    nb_values = len(ot_odr_df[var].cat.categories)
    var_bn[var] = gum.LabelizedVariable(var, var, nb_values)
    
for var in var_bn:
    for i, modalite in enumerate(ot_odr_df[var].cat.categories):
        var_bn[var].changeLabel(i, modalite)
        
bn = gum.BayesNet("modèle simple")
for var in var_bn.values():
    bn.add(var)
    
bn.addArc("SIG_OBS", "SYSTEM_N1")

#vérification de notre RB
import pyAgrum.lib.notebook as gnb 
bn

bn.cpt("SIG_OBS")
bn.cpt("SYSTEM_N1")

bn.fit_bis(ot_odr_df, verbose_mode=True)
bn.cpt("SIG_OBS")
bn.cpt("SYSTEM_N1")

pred_prob = bn.predict_proba(ot_odr_df[["SIG_OBS"]].iloc[-1000:], 
                             var_target="SYSTEM_N1",
                             show_progress=True)
print(pred_prob)

pred = bn.predict(ot_odr_df[["SIG_OBS"]].iloc[-1000:], 
                  var_target="SYSTEM_N1",
                  show_progress=True)

print(pred)