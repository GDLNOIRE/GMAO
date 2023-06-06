import pandas as pd
import graphviz
import os
from pyagrum_extra import gum
import pyAgrum.lib.notebook as gnb 


ot_odr_filename = os.path.join(".", "donnees/OT_ODR.csv.bz2")
ot_odr_df = pd.read_csv(ot_odr_filename,
                        compression="bz2",
                        sep=";")

equipements_filename = os.path.join(".", 'donnees/EQUIPEMENTS.csv')
equipements_df = pd.read_csv(equipements_filename,
                             sep=";")
"""
Transformation des kilométrages en classes
"""

# Définition des limites des intervalles pour chaque classe
kilometrage_bins = [0, 15000, 30000, 60000, 85000, 115000,150000,200000,250000,float('inf')]

# Définition des étiquettes pour chaque classe
kilometrage_labels = ['0-15000', '15000-30000', '30000-60000', '60000-85000', '85000-115000', '115000-150000','150000-200000','200000-250000','250000+']

# Transformation de la variable "kilométrage" en classe
ot_odr_df['kilométrage_classe'] = pd.cut(ot_odr_df['kilométrage'], bins=kilometrage_bins, labels=kilometrage_labels)

# Conversion de la nouvelle variable en catégorie
ot_odr_df['kilométrage_classe'] = ot_odr_df['kilométrage_classe'].astype('category')
print(ot_odr_df["kilométrage_classe"])


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

bn.cpt("SYSTEM_N1")
bn.cpt("SIG_OBS")
bn.fit_bis(ot_odr_df, verbose_mode=True)
bn.cpt("SIG_OBS")
bn.cpt("SYSTEM_N1")
pred_prob = bn.predict_proba(ot_odr_df[["SIG_OBS","SIG_ORGANE"]].iloc[-1000:], 
                             var_target="SYSTEM_N1",
                             show_progress=True)
print(pred_prob)

pred = bn.predict(ot_odr_df[["SIG_OBS","SIG_ORGANE"]].iloc[-1000:], 
                  var_target="SYSTEM_N1",
                  show_progress=True)
print(pred)
bn





