import networkx as nx
import numpy as np
import os
import pandas as pd

from configuration import config

from matplotlib import pyplot as plt

class MinimumSpanningTree():
    
  def __init__(self):
      self.random_state = 2019
      self.alpha = 0.05
      self.bonferroni_factor = alpha/(42*5)
  
  
  def get_csv_files(self):
      folder_list = os.listdir(config['home_folder'])
      csv_file_dict = {}
      for folder in folder_list:
          csv_file_list = sorted(os.listdir(os.path.join(config['home_folder'], folder, 'linear_regression', 'without_idh1')), key=lambda x: int(x.split('_')[0]))
          csv_file_dict[folder] = csv_file_list
  
      return csv_file_dict
   
  
  def filter_relevant_features(self, modality_csv_files):
      results_dict = {}
      for modality in modality_csv_files.keys():
          results_dict[modality] = {}
          csv_file_list = modality_csv_files[modality]
          for csv_file in csv_file_list:
              df = pd.read_csv(os.path.join(config['home_folder'], modality, 'linear_regression', 'without_idh1', csv_file))
              experiment_number = csv_file.split('_')[0]
              results_dict[modality][experiment_number] = []
              for idx, feature in enumerate(features):
                  feature_df = df[df['response_variable'] == feature]
                  if np.all(feature_df['pvals']>self.bonferroni_factor):
                     results_dict[modality][experiment_number].append(feature)
                     continue
              
      return results_dict
 
  def load_relevant_features(self, modality, experiment_number):
      try:
         assert(1<=experiment_number<=25)
         
   
