import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from mlxtend.plotting import plot_decision_regiond

df= pd.read("https://d.docs.live.net/C5B281885460835C/Documents/mldata.xlsx")
# /Activation function 
pr= Perceptro(alpha=1)
pr.fit(x_train,y_train)

pr.score(x_train,y_train)*100,pr.score(x_test,y_test)*100







