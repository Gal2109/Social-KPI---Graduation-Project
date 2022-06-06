# -*- coding: utf-8 -*-
"""Final_Project_Functioned.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bbun5FHf3eCJcik9_Dt4ZPR6C5YF_cny
"""

import numpy as np
import pandas as pd
# import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.impute import KNNImputer
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
import warnings
warnings.filterwarnings("ignore")

def rawToValCatagorized(raw_csv): # gets a raw DF from as arrive from authority and returns catagorized by value DF
  df = pd.read_csv(raw_csv)
  df = df.query('usage == 1')
  f_origin = df
  df.arnona_cat = pd.Categorical(df.arnona_cat)
  df['arnona_cat_code'] = df.arnona_cat.cat.codes.astype(int)
  # MARTIAL - arbitrar scoring
  df.martial = pd.Categorical(df.martial)
  df['martial_code'] = df.martial.cat.codes

  arnona_cat_score_dict = { 'Construction' : 0, 'Empty' : 2, 'corona19' : -2 ,'warTrauma' : -2 ,'soldier' : -2 ,'other' : -2 ,'one_parent' : -2 ,'income' : -2 ,'immigrants' : -1 ,'elderlies_nursing' : -2 ,'elderlies' : -1 ,'disabilities' : -2 }
  df['arnona_cat_score'] = df['arnona_cat'].apply(lambda x : arnona_cat_score_dict[x] if x==x else 0)
  df['arnona_cat_score'] = df['arnona_cat_score'].fillna(0)

  martial_score_dict = { 'אלמן/ה' : -2, 'גרוש/ה' : -2, 'נשוי/ה' : 2 ,'רווק/ה' : 0 }
  df['martial_score'] = df['martial'].apply(lambda x : martial_score_dict[x] if x==x else 0)
  df['martial_score'] = df['martial_score'].fillna(0)

  df['members_Water_score'] = df['members_Water'].apply(lambda x : -2 if x==1  else (1 if 1<x<4 else (2 if x>3  else 0)))
  df['age_score'] = df['age'].apply(lambda x : 2 if 18<x<44  else (-1 if 43<x<64 else (-2 if x>63  else 0)))
  df.rename(columns = { 'near 106 pizul and dangerous buildings' : 'near_106_pizul_and_dangerous_buildings' }, inplace = True)
  df['near_106_pizul_and_dangerous_buildings_score'] = df['near_106_pizul_and_dangerous_buildings'].apply(lambda x : -2 if x==2  else 0)
  df["count"] = df.groupby("STAT")["index"].transform('count') # population size of a statistic area
  # df.head()
  df = df.iloc[: , 1:]

  # PROBABILITY FUNCTION - gets a numeric number and devide by the total population for that s.a (statistical area)
  def prob_func(df, col_name):
    df[f'{col_name}'] = df[f'{col_name}']/df['count']

  prob_cols = ['widow_grown', 'widow_elderlies', 'lonely_elderlies', 'p85_plus', 'avtachat_hachansa_family', 'mekabley_kizva_elderlies', 'hashlamta_hachnasa_family_eldelies', 'hashlama_kizvat_nechut_elderlies', 'Hashlamat_hachnasa_sheerim_family', 'Mekabley_mezonot', 'Mekabley_kizbaot_nechut', 'zachaim_kizbat_nechut_children', 'mekabley_kizbaot_from_injured_Work', 'mekabley_kizba_siud', 'accumulated_cases', 'accumulated_recoveries', 'accumulated_hospitalized', 'accumulated_vaccination_first_dose', 'accumulated_vaccination_second_dose', 'accumulated_vaccination_third_dose']
  # probcols is the list of all aggrigated parameters, it shows the probability of one to be *col name*
  for col_name in prob_cols:
    prob_func(df, col_name)

  # INCOME COLUMNS
  df['total_income'] = df['all_jobs_no_household_jobs_mean']+df['household_jobs_mean']+df['pension_mean']+df['kizbat_sheerim_mean']+df['self_employed_mean']
  df['income_per_person'] = df['total_income']/(df['members_Water']+1)

  for prob_col in prob_cols:
    df[f'{prob_col}_score'] = df[f'{prob_col}']*(-2)
    df[f'{prob_col}_score'] = df[f'{prob_col}_score'].fillna(0)

  # df['income_per_person'].quantile(0.25)
  q25 = df['income_per_person'].quantile(0.25)
  q50 = df['income_per_person'].quantile(0.5)
  q75 = df['income_per_person'].quantile(0.75)
  df['income_per_person_score'] = df['income_per_person'].apply(lambda x : -2 if x<=q25  else (-1 if q25<x<q50 else (1 if q50<x<q75 else(2 if x>=q75 else 0))))

  df['socio_economic_score'] = df['socio_economic'].apply(lambda x : -2 if 1<=x<=2  else (-1 if x==3 else (1 if x==5 else(2 if 6<=x<=7 else 0))))

  all_scored_params = [] 
  for col in df.columns:
    if ('score' in col):
      all_scored_params.append(col)

  all_scored_params # hold all of the parameters (which may effect the metrics)

  #Lets make the DF more readable and relevant by leaving only the are (stat and coordiantes):

  df_scores = df[['index','STAT','north','east']+all_scored_params]
  return df_scores

def update_weights(metric_dict, param_to_update, new_weight): # updated given dict with a new value
  up_dict = {f'{param_to_update}' : new_weight}
  updated_metric_dict = metric_dict.update(up_dict)

  if round(sum(metric_dict.values()), 4) != 1:
    print(f"WARNING: dictionary weights are not summed to 1")
    print("sum:", round(sum(metric_dict.values()), 4) )
  else:
    print(f"---Dictionary sums to 1---")
  if param_to_update not in metric_dict:
    print("WARNING: param does not exist in dictionary")

  return updated_metric_dict

def weights_update(GUI_tuple): # gets (M, d) and update M dict by d changes
  metric_str = GUI_tuple[0]
  curr_dict = mapping_dict[metric_str] # holds the dict we want to update
  new_weights_dict = GUI_tuple[1] # holds the dict with the new weights

  for param, weight in new_weights_dict.items():
    update_weights(curr_dict, param, weight)

def MetricsCalc(catagorized_df, loneliness_dict, health_dict, economic_strength_dict  ): # this function recieve a DF (catagorized), wwights dictionary and return the same DF with metrics
  df_scores = catagorized_df
  columns_list = df_scores.columns
  df_scores['Loneliness'] = 6 - df_scores.apply(lambda row: sum([row[col] *loneliness_dict[col] for col in columns_list]), axis=1) # Now loneliness is not non-loneliness anymore (5 = lonenly)
  df_scores['Health'] = df_scores.apply(lambda row: sum([row[col] *health_dict[col] for col in columns_list]), axis=1)
  df_scores['Economic_Strength'] = df_scores.apply(lambda row: sum([row[col] *economic_strength_dict[col] for col in columns_list]), axis=1)

  Metrics = ['Loneliness', 'Health', 'Economic_Strength']
  for metric in Metrics: 
    q20 = df_scores[metric].quantile(0.20)
    q40 = df_scores[metric].quantile(0.40)
    q60 = df_scores[metric].quantile(0.60)
    q80 = df_scores[metric].quantile(0.80)
    q100 = df_scores[metric].quantile(0.100)
    df_scores[f'{metric}_score'] = df_scores[metric].apply(lambda x : 1 if x<=q20  else (2 if q20<x<=q40 else (3 if q40<x<=q60 else(4 if q60<x<=q80 else 5))))

  return df_scores

def default_weights(df_catagorized, loneliness_dict, health_dict, economic_strength_dict):
#   loneliness_dict = {}
#   health_dict = {}
#   economic_strength_dict = {}
  for col in df_catagorized.columns:
    loneliness_dict[col] = 0
    health_dict[col] = 0
    economic_strength_dict[col] = 0
    
  update_weights(loneliness_dict, 'arnona_cat_score', 0.1 )
  update_weights(loneliness_dict, 'members_Water_score', 0.1 )
  update_weights(loneliness_dict, 'martial_score', 0.1 )
  update_weights(loneliness_dict, 'widow_grown_score', 0.05 )
  update_weights(loneliness_dict, 'widow_elderlies_score', 0.1 )
  update_weights(loneliness_dict, 'lonely_elderlies_score', 0.25 )
  update_weights(loneliness_dict, 'p85_plus_score', 0.05 )
  update_weights(loneliness_dict, 'accumulated_cases_score', 0.05)
  update_weights(loneliness_dict, 'age_score', 0.1 )
  update_weights(loneliness_dict, 'area_per_person_score', 0.05 )
  update_weights(loneliness_dict, 'Ownership_score', 0.05)

  update_weights(health_dict, 'arnona_cat_score', 0.2 )
  update_weights(health_dict, 'age_score', 0.08 )
  update_weights(health_dict, 'hashlama_kizvat_nechut_elderlies_score', 0.08 )
  update_weights(health_dict, 'Mekabley_kizbaot_nechut_score', 0.1 )
  update_weights(health_dict, 'zachaim_kizbat_nechut_children_score', 0.09 )
  update_weights(health_dict, 'mekabley_kizbaot_from_injured_Work_score', 0.11 )
  update_weights(health_dict, 'mekabley_kizba_siud_score', 0.15 )
  update_weights(health_dict, 'accumulated_cases_score', 0.05 )
  update_weights(health_dict, 'accumulated_recoveries_score', 0.01 )
  update_weights(health_dict, 'accumulated_hospitalized_score', 0.07 )
  update_weights(health_dict, 'accumulated_vaccination_first_dose_score', 0.02 )
  update_weights(health_dict, 'accumulated_vaccination_second_dose_score', 0.02 )
  update_weights(health_dict, 'accumulated_vaccination_third_dose_score', 0.02 )

  update_weights(economic_strength_dict, 'area_per_person_score', 0.03 )
  update_weights(economic_strength_dict, 'socio_economic_score', 0.05 )
  update_weights(economic_strength_dict, 'mekabley_kizba_siud_score', 0.02 )
  update_weights(economic_strength_dict, 'mekabley_kizbaot_from_injured_Work_score', 0.02 )
  update_weights(economic_strength_dict, 'zachaim_kizbat_nechut_children_score', 0.02 )
  update_weights(economic_strength_dict, 'Mekabley_kizbaot_nechut_score', 0.02 )
  update_weights(economic_strength_dict, 'Mekabley_mezonot_score', 0.02 )
  update_weights(economic_strength_dict, 'Hashlamat_hachnasa_sheerim_family_score', 0.02 )
  update_weights(economic_strength_dict, 'hashlama_kizvat_nechut_elderlies_score', 0.02 )
  update_weights(economic_strength_dict, 'hashlamta_hachnasa_family_eldelies_score', 0.02 )
  update_weights(economic_strength_dict, 'mekabley_kizva_elderlies_score', 0.02 )
  update_weights(economic_strength_dict, 'avtachat_hachansa_family_score', 0.02 )
  update_weights(economic_strength_dict, 'income_per_person_score', 0.2 )
  update_weights(economic_strength_dict, 'arnona_cat_score', 0.1 )
  update_weights(economic_strength_dict, 'Ownership_score', 0.20 )
  update_weights(economic_strength_dict, 'age_score', 0.05 )
  update_weights(economic_strength_dict, 'martial_score', 0.02 )
  update_weights(economic_strength_dict, 'members_Water_score', 0.05 )
  update_weights(economic_strength_dict, 'near_106_pizul_and_dangerous_buildings_score', 0.1 )

  return loneliness_dict, health_dict, economic_strength_dict
#########################################################################################################

# df_catagorized = rawToValCatagorized('big_table.csv')

# loneliness_dict = {}
# health_dict = {}
# economic_strength_dict = {}
# for col in df_catagorized.columns:
#   loneliness_dict[col] = 0
#   health_dict[col] = 0
#   economic_strength_dict[col] = 0



# mapping_dict = {"E" : economic_strength_dict, "H" : health_dict, "L" : loneliness_dict } #maps from a letter to the corresponding dictionary
# default_weights(loneliness_dict,health_dict,economic_strength_dict)

# # weights_update(GUI_tuple)

# df_scored = MetricsCalc(df_catagorized,loneliness_dict, health_dict, economic_strength_dict  )
# df_scored

# NL = df_scores['Loneliness_score']
# E = df_scores['Economic_Strength_score']
# H = df_scores['Health_score']
# K_const = 5
# T_threshold = 34 # risker than (1,2,2)

# df_scores['R_function'] = np.power(K_const-NL,2) + np.power(K_const-H,2) + np.power(K_const-E,2)
# df_scores['Risk'] = df_scores['R_function'].apply(lambda x : 1 if x>= T_threshold else 0)

# print(round(df_scores.query('Risk == 1').count()[1]/df_scores.shape[0]*100 ,3), '% of the households are under risk')
