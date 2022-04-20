import requests
import json
import math
import pandas as pd
import numpy as np
import owlready2
from pandas import json_normalize
from owlready2 import *

def get_database(ontology_class, dataset_id = 2):
    '''function for criterion data base'''
    o_list = [] 
    for current_class in ontology_classes:
        hp_id = current_class.name.replace('_', ':')
        o_list.append(hp_id)

    o_100 = o_list[0:100]
    s = ",".join(o_100).replace(",", ";")
    para = {'q': s}
    response = requests.get('https://rare.cohd.io/api/vocabulary/findConceptByCode', params = para).json()
    df_z = json_normalize(response['results'])
    list_z = df_z['concept_id'].values.tolist()
    list_z = list(map(str, list_z))
    str_z = ",".join(list_z).replace(",", ";")
    query = {'dataset_id': dataset_id, 'concept_id': str_z}
    info = requests.get('https://rare.cohd.io/api/frequencies/singleConceptFreq', params=query).json()
    result = json_normalize(info['results'])

    i = 101
    while i < 16400: 
        o_100 = o_list[i:i+99]
        s = ",".join(o_100).replace(",", ";")
        para = {'q': s}
        response = requests.get('https://rare.cohd.io/api/vocabulary/findConceptByCode', params = para).json()
        df_z = json_normalize(response['results'])
        list_z = df_z['concept_id'].values.tolist()
        list_z = list(map(str, list_z))
        str_z = ",".join(list_z).replace(",", ";")
        query = {'dataset_id': 2, 'concept_id': str_z}
        info = requests.get('https://rare.cohd.io/api/frequencies/singleConceptFreq', params=query).json()
        df = json_normalize(info['results'])
        result = pd.concat([result, df])
        i = i+100

    o_last = o_list[16401:16480]
    s = ",".join(o_last).replace(",", ";")
    para = {'q': s}
    response = requests.get('https://rare.cohd.io/api/vocabulary/findConceptByCode', params = para).json()
    df_z = json_normalize(response['results'])
    list_z = df_z['concept_id'].values.tolist()
    list_z = list(map(str, list_z))
    str_z = ",".join(list_z).replace(",", ";")
    query = {'dataset_id': 2, 'concept_id': str_z}
    info = requests.get('https://rare.cohd.io/api/frequencies/singleConceptFreq', params=query).json()
    df = json_normalize(info['results'])
    result = pd.concat([result, df])
    terms = result.loc[:,("concept_code", "concept_id", "concept_name", "concept_count", "concept_frequency")]
    condition = (d_data.concept_code == 'HP:0010943') | (d_data.concept_code == 'HP:0012236') | (d_data.concept_code == 'HP:0032174') | (d_data.concept_code == 'HP:0032493') | (d_data.concept_code == 'HP:0033036')  | (d_data.concept_code == 'HP:0002156') | (d_data.concept_code == 'HP:0100775') | (d_data.concept_code == 'HP:0004060') | (d_data.concept_code == 'HP:0034044') | (d_data.concept_code == 'HP:0033377') | (d_data.concept_code == 'HP:0003612') | (d_data.concept_code == 'HP:0100609')
    database = terms[condition]
    return database

def get_log_odds (p_data):
    '''fuction for get the log odds estimate corrsesponding to phenotype j'''
    '''still working'''
    frequency = p_data['concept_frequency']
    log_odds = np.log(frequency/(1-frequency))
    log_odds_list = log_odds.to_list()
    return(log_odds_list)


def get_indicator_ftn1 (log_odds):
    '''indicator function equals 1 when the estimate (log_odds) is greater than 0 '''
    Ind1 = []   
    for i in log_odds:
        if i > 0:
            i = 1
        else:
            i = 0
        Ind1.append(i)
    return(Ind1)
        
        
def get_indicator_ftn2 (log_odds):
    '''indicator function equals 1 when the estimate (log_odds) is less than 0'''   
    Ind2 = []
    for i in log_odds:
        if i < 0:
            i = 1
        else:
            i = 0
        Ind2.append(i)
    return(Ind2)

def get_Dij (p_data, d_data):
    '''indicator variable eqaul to 1 when patient i has been diagnosed with phenotype j''' 
    p_c_data = p_data['concept_name'].to_list()
    database = database['concept_name'].to_list()
    D_i = []
    for i in database:
        if i in p_c_data:
            i = 1
        else:
            i = 0
        D_i.append(i)
    return(D_i)


def cal_risk(p_data, database):
    
    log_odds = get_log_odds(p_data)
    Ind1 = get_indicator_ftn1(log_odds)
    Ind2 = get_indicator_ftn2(log_odds)
    D_i = get_Dij(p_data, database)

    risk = np.array([])
    
    for i in range(0, len(log_odds)):
        r = (log_odds[i] * D_i[i] * Ind1[i]) - (log_odds[i] * (1-D_i[i]) * Ind2[i])
        risk = np.append(risk, np.array([r]))

    PhRes = sum(risk)
    return(PhRes)

#sum of clinical features observed in a given subject weighted by the log inverse prevalence of the feature



onto = get_ontology("http://purl.obolibrary.org/obo/hp.owl").load()
obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
ontology_classes = obo.HP_0000001.descendants()
database = get_ddata(ontology_classes, 2)
p_data = d_data.head()

cal_risk(p_data, database)
