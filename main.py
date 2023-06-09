import pandas as pd
import graphviz
import numpy as np
import os
from pyagrum_extra import gum
from pyagrum_extra import predict
import pyAgrum.lib.notebook as gnb 

ot_odr_filename = os.path.join(".", "donnees/OT_ODR.csv.bz2")
ot_odr_df = pd.read_csv(ot_odr_filename,
                        compression="bz2",
                        sep=";")

equipements_filename = os.path.join(".", 'donnees/EQUIPEMENTS.csv')
equipements_df = pd.read_csv(equipements_filename,
                             sep=";")

# on fait un seul tableau à partir de nos 2 csv
merged_df = pd.merge(ot_odr_df, equipements_df, on='EQU_ID')
#on supprime une ligne qui possède des valeurs non définit (kilométrage)
merged_df.drop(178662, inplace=True)

# Définition des limites des intervalles pour chaque classe
kilometrage_bins = [-1, 50000, 100000,150000,200000,250000,float('inf')]

# Définition des étiquettes pour chaque classe
kilometrage_labels = ['0-50000', '50000-100000','100000-150000','150000-200000','200000-250000','250000+']

# Transformation de la variable "kilométrage" en classe
merged_df['KILOMETRAGE_CLASSE'] = pd.cut(merged_df['KILOMETRAGE'], bins=kilometrage_bins, labels=kilometrage_labels)
merged_df = merged_df.sort_values('KILOMETRAGE')

# Conversion de la nouvelle variable en catégorie
merged_df['KILOMETRAGE_CLASSE'] = merged_df['KILOMETRAGE_CLASSE'].astype('category')

"""
COLONNE EN BINAIRE
"""
# Séparation des valeurs de la colonne en utilisant le séparateur "/"
split_values = merged_df["SIG_CONTEXTE"].str.split("/")

# Création des colonnes binaires pour chaque valeur unique
unique_values = set(value for values in split_values for value in values)
var_to_model = []
bin_model    = []
for value in unique_values:
    merged_df[f"{value}_BIN"] = split_values.apply(lambda x: int(value in x))
    var_to_model.append(f"{value}_BIN")

bin_model = var_to_model.copy()     
binForWeb = bin_model.copy()
other_var_to_model = ["SYSTEM_N1", "SIG_OBS","SIG_ORGANE","SYSTEM_N2","SYSTEM_N3","TYPE_TRAVAIL","MODELE","KILOMETRAGE_CLASSE"]
for var in other_var_to_model:
    var_to_model.append(var)

for var in var_to_model:
    merged_df[var] = merged_df[var].astype('category')

var_bn = {}
for var in var_to_model:
    nb_values = len(merged_df[var].cat.categories)
    var_bn[var] = gum.LabelizedVariable(var, var, nb_values)
    
for var in var_bn:
    for i, modalite in enumerate(merged_df[var].cat.categories):
        var_bn[var].changeLabel(i, str(modalite))
merged_df


bn = gum.BayesNet("modèle simple")
for var in var_bn.values():
    bn.add(var)
for i in range(len(bin_model)):
    bn.addArc("SYSTEM_N2",str(bin_model[i]))
bn.addArc("SIG_OBS", "SYSTEM_N1")
bn.addArc("SIG_ORGANE", "SYSTEM_N1")
bn.addArc("MODELE", "SYSTEM_N1")
bn.addArc("SYSTEM_N1", "SYSTEM_N2")
bn.addArc("SYSTEM_N2", "SYSTEM_N3")
bn.addArc("SYSTEM_N3", "TYPE_TRAVAIL")
bn.addArc("TYPE_TRAVAIL", "KILOMETRAGE_CLASSE")

bn.fit(merged_df, verbose_mode=True)

"""test"""
proba = bn.predict_proba(merged_df[["SIG_OBS","SIG_ORGANE","MODELE"]].iloc[-1:], 
                var_target="SYSTEM_N1",
                show_progress=True)
test2 = bn.predict(merged_df[["SIG_OBS","SIG_ORGANE","MODELE"]].iloc[-1:], 
                var_target="SYSTEM_N1",
                show_progress=True)

labels = var_bn["SYSTEM_N1"].labels()
def cinqMeilleur(labels,proba):
    indices_plus_haut = np.argsort(proba[0])[-5:]
    tabProba = []
    tabLabel = []
    for ind in indices_plus_haut:
        #Récupération des valeurs possibles de la variable cible
        tabProba.append(proba[0][ind])
        tabLabel.append(labels[ind])
    return tabLabel,tabProba
cinqMeilleur(labels,proba)

"""prediction"""
pred_SystemN1 = bn.predict(merged_df[["SIG_OBS","SIG_ORGANE","MODELE"]].iloc[-5000:], 
                  var_target="SYSTEM_N1",
                  show_progress=True)
bin_model.append("SIG_OBS")
bin_model.append("SIG_ORGANE")
bin_model.append("MODELE")
bin_model.append("SYSTEM_N1")
bin_model.append("KILOMETRAGE_CLASSE")
pred_SystemN2 = bn.predict(merged_df[bin_model].iloc[-5000:], 
                  var_target="SYSTEM_N2",
                  show_progress=True)
print(bin_model)
bin_model.append("SYSTEM_N2")
pred_SystemN3 = bn.predict(merged_df[bin_model].iloc[-5000:], 
                  var_target="SYSTEM_N3",
                  show_progress=True)
bin_model.append("SYSTEM_N3")
pred_TypeTravail = bn.predict(merged_df[bin_model].iloc[-5000:], 
                  var_target="TYPE_TRAVAIL",
                  show_progress=True)

print((merged_df["SYSTEM_N1"].iloc[-5000:] == pred_SystemN1).mean())
print((merged_df["SYSTEM_N2"].iloc[-5000:] == pred_SystemN2).mean())
print((merged_df["SYSTEM_N3"].iloc[-5000:] == pred_SystemN3).mean())
print((merged_df["TYPE_TRAVAIL"].iloc[-5000:] == pred_TypeTravail).mean())

"""
WEB CONTENT
"""
def getAllSig_Obs():
    return set(merged_df["SIG_OBS"])
    
def getAllSig_Organe():
    return set(merged_df["SIG_ORGANE"])

def getAllConstructeur():
    return set(merged_df["CONSTRUCTEUR"])

def getAllModeleWithConstruct(constructeurValue):
    allLineWithConstructeur = merged_df.loc[merged_df['CONSTRUCTEUR'] == constructeurValue]
    return set(allLineWithConstructeur["MODELE"])

def getAllModele():
    return set(merged_df["MODELE"])

def getAllSigContexte():
    return set(merged_df["SIG_CONTEXTE"])

def getAllKilometrage():
    return set(merged_df["KILOMETRAGE_CLASSE"])

def predictionWeb(bn,dict,bin_web):
    VAR_PRED = ["MODELE","KILOMETRAGE_CLASSE","SIG_OBS","SIG_ORGANE"]
    dictPrediction = dict()
    context_ToBinary(dictPrediction,bin_web)
    for var in VAR_PRED:
        dictPrediction[var] = dict[var]
        bin_web.append(var)
    # res = bn.predict_proba(dictPrediction[[bin_web]],var_target="SYSTEM_N1",show_progress=True)
    # print(res)
def context_ToBinary(dict,bin_web):
    # Séparation des valeurs de la colonne en utilisant le séparateur "/"
    split_values = dict["SIG_CONTEXTE"].str.split("/")
    # Création des colonnes binaires pour chaque valeur unique
    for value in bin_web:
        dict[f"{value}_BIN"] = split_values.apply(lambda x: int(value in x))