# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:36:54 2025

@author: KIMMINJI
"""
'''
가설 검정이란?

통계분석 : 기술통계, 추론통계
    기술통계 : 데이터를 요약해서 설명하는 통계분석 기법
    예) 월급 평균 구하기
    추론통계 : 어떤 값이 발생할 확률을 계산하는 통계분석기법
    예) 월급 차이 있다고 했을 때, 그 차이가 우연인지 아닌지 /상관/가설
'''
import pandas as pd
mpg = pd.read_csv('./mpg.csv')
mpg.query('category in ["compact","suv"]')\
    .groupby('category', as_index = False)\
        .agg(n = ('category', 'count'), mean = ('cty','mean'))
'''
  category   n      mean
0  compact  47  20.12766
1      suv  62  13.50000
'''
# t 검정
# mpg에서 category가 'compact' => 'cty'
# mpg에서 category가 'suv' => 'cty'        
compact = mpg.query('category == "compact"')['cty']
suv = mpg.query('category == "suv"')['cty']        

# t-test : stats.ttest_ind(compact, suv, equal_var = True)
from scipy import stats        
        
stats.ttest_ind(compact, suv, equal_var=True)
#=> Ttest_indResult(statistic=11.917282584324107, pvalue=2.3909550904711282e-21)
#=> pvalue=2.3909550904711282e-21 : 0.05보다 작으므로 유의하다. 
        
mpg.query('fl in ["r","p"]').groupby('fl', as_index = False).agg(n = ('category','count'),mean = ('cty','mean'))
'''
  fl    n       mean
0  p   52  17.365385
1  r  168  16.738095
'''
regular = mpg.query('fl == "r"')['cty']
premium = mpg.query('fl == "p"')['cty']     
  
stats.ttest_ind(regular, premium, equal_var=True)       
#=> Ttest_indResult(statistic=-1.066182514588919, pvalue=0.28752051088667036)
#=> pvalue=0.28752051088667036 유의하지 않음

#=========상관분석========================
## 실업자 수와 개인 소비 지출의 상관관계 : economics.csv
mtcars = pd.read_csv('./mtcars.csv') 

# 상관계수 : corr         
car_cor = mtcars.corr()

import matplotlib.pyplot as plt
import seaborn as sns

# 해상도 설정, 가로 세로 크기 결정
plt.rcParams.update({'figure.dpi' : '120',
                    'figure.figsize' : [7.5,5.5]})

# 히트맵 : heatmap
# 상관계수 표시 : annot = True
# 컬러맵 : cmap = 'RdBu'
sns.heatmap(car_cor, annot = True, cmap = 'RdBu')

## 대각 행렬 제거
import numpy as np

mask = np.zeros_like(car_cor)

# 오른쪽 위 대각선 행렬을 1로 바꾸기 
mask[np.triu_indices_from(mask)] = 1

# 히트맵에 적용
sns.heatmap(car_cor, annot = True, cmap = 'RdBu', mask=mask)

## 산점도
mpg = pd.read_csv('./mpg.csv')
import plotly.express as px
fig = px.scatter(data_frame = mpg, 
           x = 'cty', y = 'hwy',
           color = 'drv')

import matplotlib.pyplot as plt
fig.write_html('scatter_plt.html')

import webbrowser
webbrowser.open_new('scatter_plt.html')

df = mpg.groupby('category', as_index = False).agg(n = ('category','count'))

fig = px.bar(data_frame = df, 
           x = 'category', y = 'n',
           color = 'category')
fig.write_html('scatter_plt.html')
webbrowser.open_new('scatter_plt.html')

