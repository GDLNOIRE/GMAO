import pandas as pd
import graphviz
import numpy as np
import os
from pyagrum_extra import gum
from pyagrum_extra import predict
import pyAgrum.lib.notebook as gnb 

class ReseauBayesien:
    merged_df = None
    bn = None
    var_bn = {}
    dictPrediction = dict()
    bin_web = []
    
    def __init__(self):
        ot_odr_filename = os.path.join(".", "donnees/OT_ODR.csv.bz2")
        ot_odr_df = pd.read_csv(ot_odr_filename,
                                compression="bz2",
                                sep=";")

        equipements_filename = os.path.join(".", 'donnees/EQUIPEMENTS.csv')
        equipements_df = pd.read_csv(equipements_filename,
                                    sep=";")

        # on fait un seul tableau à partir de nos 2 csv
        self.merged_df = pd.merge(ot_odr_df, equipements_df, on='EQU_ID')
        #on supprime une ligne qui possède des valeurs non définit (kilométrage)
        self.merged_df.drop(178662, inplace=True)

        # Définition des limites des intervalles pour chaque classe
        kilometrage_bins = [-1, 50000, 100000,150000,200000,250000,float('inf')]

        # Définition des étiquettes pour chaque classe
        kilometrage_labels = ['0-50000', '50000-100000','100000-150000','150000-200000','200000-250000','250000+']

        # Transformation de la variable "kilométrage" en classe
        self.merged_df['KILOMETRAGE_CLASSE'] = pd.cut(self.merged_df['KILOMETRAGE'], bins=kilometrage_bins, labels=kilometrage_labels)
        self.merged_df = self.merged_df.sort_values('KILOMETRAGE')

        # Conversion de la nouvelle variable en catégorie
        self.merged_df['KILOMETRAGE_CLASSE'] = self.merged_df['KILOMETRAGE_CLASSE'].astype('category')

        """
        COLONNE EN BINAIRE
        """
        # Séparation des valeurs de la colonne en utilisant le séparateur "/"
        split_values = self.merged_df["SIG_CONTEXTE"].str.split("/")

        # Création des colonnes binaires pour chaque valeur unique
        unique_values = set(value for values in split_values for value in values)
        var_to_model = []
        bin_model    = []
        for value in unique_values:
            self.merged_df[f"{value}_BIN"] = split_values.apply(lambda x: int(value in x))
            var_to_model.append(f"{value}_BIN")

        bin_model = var_to_model.copy()     
        self.bin_web = bin_model.copy()
        other_var_to_model = ["SYSTEM_N1", "SIG_OBS","SIG_ORGANE","SYSTEM_N2","SYSTEM_N3","TYPE_TRAVAIL","MODELE","KILOMETRAGE_CLASSE"]
        for var in other_var_to_model:
            var_to_model.append(var)

        for var in var_to_model:
            self.merged_df[var] = self.merged_df[var].astype('category')


        for var in var_to_model:
            nb_values = len(self.merged_df[var].cat.categories)
            self.var_bn[var] = gum.LabelizedVariable(var, var, nb_values)
            
        for var in self.var_bn:
            for i, modalite in enumerate(self.merged_df[var].cat.categories):
                self.var_bn[var].changeLabel(i, str(modalite))
        self.merged_df


        self.bn = gum.BayesNet("modèle simple")
        for var in self.var_bn.values():
            self.bn.add(var)
        for i in range(len(bin_model)):
            self.bn.addArc("SYSTEM_N2",str(bin_model[i]))
        self.bn.addArc("SIG_OBS", "SYSTEM_N1")
        self.bn.addArc("SIG_ORGANE", "SYSTEM_N1")
        self.bn.addArc("MODELE", "SYSTEM_N1")
        self.bn.addArc("SYSTEM_N1", "SYSTEM_N2")
        self.bn.addArc("SYSTEM_N2", "SYSTEM_N3")
        self.bn.addArc("SYSTEM_N3", "TYPE_TRAVAIL")
        self.bn.addArc("TYPE_TRAVAIL", "KILOMETRAGE_CLASSE")

        self.bn.fit(self.merged_df, verbose_mode=True)

    
    """
    WEB CONTENT
    """
    def getAllSig_Obs(self):
        return set(self.merged_df["SIG_OBS"])
        
    def getAllSig_Organe(self):
        return set(self.merged_df["SIG_ORGANE"])

    def getAllConstructeur(self):
        return set(self.merged_df["CONSTRUCTEUR"])

    def getAllModeleWithConstruct(self,constructeurValue):
        allLineWithConstructeur = self.merged_df.loc[self.merged_df['CONSTRUCTEUR'] == constructeurValue]
        return set(allLineWithConstructeur["MODELE"])

    def getAllModele(self):
        return set(self.merged_df["MODELE"])

    def getAllSigContexte(self):
        return set(self.merged_df["SIG_CONTEXTE"])

    def getAllKilometrage(self):
        return set(self.merged_df["KILOMETRAGE_CLASSE"])

    def cinqMeilleur(self,bin_web,target):
        #transformation dict en dataframe
        df = pd.DataFrame(self.dictPrediction)
        #récupération des proba de N1
        proba = self.bn.predict_proba(df[bin_web], 
                    var_target=target,
                    show_progress=True)
        #récupération des labels de N1
        labels = self.var_bn[target].labels()
        #récupération des 5 indices des 5 plus grandes proba
        indices_plus_haut = np.argsort(proba[0])[-5:]
        tabProba = []
        tabLabel = []
        for ind in indices_plus_haut:
            #Récupération des valeurs possibles de la variable cible
            tabProba.append(proba[0][ind])
            tabLabel.append(labels[ind])
        return tabLabel,tabProba
    def context_ToBinary(self,dictWeb):
        # Séparation des valeurs de la colonne en utilisant le séparateur "/"
        split_values = dictWeb["SIG_CONTEXTE"].split("/")
        split_values = pd.DataFrame(split_values)
        # Création des colonnes binaires pour chaque valeur unique
        for value in self.bin_web:
            value = value.replace("_BIN","")
            self.dictPrediction[f"{value}_BIN"] = split_values.apply(lambda x: int(value in x))
        return self.dictPrediction
            
            
    def predictionWebN1(self,dictWeb):
        VAR_PRED = ["MODELE","KILOMETRAGE_CLASSE","SIG_OBS","SIG_ORGANE"]
        VAR_TARGET = "SYSTEM_N1"
        self.dictPrediction = self.context_ToBinary(dictWeb)
        for var in VAR_PRED:
            self.dictPrediction[var] = dictWeb[var]
            self.bin_web.append(var)
        return self.cinqMeilleur(["SIG_OBS","SIG_ORGANE","MODELE"],VAR_TARGET)

    def predictionWebN2(self,dictWeb):
        VAR_TARGET = "SYSTEM_N2"
        VAR_GET = "SYSTEM_N1"
        self.dictPrediction[VAR_GET] = dictWeb[VAR_GET]
        self.bin_web.append(VAR_GET)
        return self.cinqMeilleur(self.bin_web,VAR_TARGET)


    def predictionWebN3(self,dictWeb):
        VAR_TARGET = "SYSTEM_N3"
        VAR_GET = "SYSTEM_N2"
        self.dictPrediction[VAR_GET] = dictWeb[VAR_GET]
        self.bin_web.append(VAR_GET)
        return self.cinqMeilleur(self.bin_web,VAR_TARGET)

    def predictionWebWork(self,dictWeb):
        VAR_TARGET = "TYPE_TRAVAIL"
        VAR_GET = "SYSTEM_N3"
        self.dictPrediction[VAR_GET] = dictWeb[VAR_GET]
        self.bin_web.append(VAR_GET)
        return self.cinqMeilleur(self.bin_web,VAR_TARGET)

