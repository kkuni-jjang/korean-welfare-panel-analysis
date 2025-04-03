# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:41:15 2025

@author: KIMMINJI
"""
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
'''
주제 : 건강보험  
    하위목표 1 : 건강보험 
        + 시각화/ 결론
    하위목표 2
        + 시각화/ 결론
    하위목표 3
        + 시각화/ 결론
    
* pdf로 분석결과 제출
* 기존 변수 사용 불가 : 성별/결혼/나이/직종/지역/월급
'''
raw_welfare = pd.read_spss('./data/Koweps_hpwc14_2019_beta2.sav')

# 복사본
welfare = raw_welfare.copy()

"""
하위목표 1 : 의료비와 건강보험가입여부
"""
# 월 생활비 - 의료비 지출
welfare = welfare.rename(columns = {'h1413_6'    :   'help'})          

# 모름/무응답 = 9999 -> 평균대체
welfare['help'] = np.where(welfare['help'] == 999, np.nan, welfare['year_count'])

# 결측치 확인 : isna().sum()
welfare['month_pay_medical'].isna().sum() # 0
welfare['month_pay_medical'].median()
welfare['month_pay_medical'].describe()
'''
count    14418.000000
mean        20.793758
std         25.953589
min          0.000000
25%          5.000000
50%         12.000000
75%         26.000000
max        383.000000

* 
'''
#ㄱ 건강보험 가입 여부 
welfare['h1411_7'].value_counts()
'''
1.0    13661    # yes
2.0      757    # no
'''
# 이름 바꾸기
welfare = welfare.rename(columns = {'h1405_1'    :   'have'})  
welfare['h1405_4'] = np.where(welfare['h1405_4'] == 1, 'yes', 'no')
welfare['h1405_5'].value_counts()
'''
yes    13661
no       757
'''

sex_income = welfare.groupby(['h1405_4','months'], as_index = False).agg(n = ('h1405_4','count'))
sex_income
'''
      sex  mean_income
0  female   186.293096
1    male   349.037571
'''

sns.barplot(data = sex_income, x = 'months', y = 'n', hue='h1405_4')
plt.xlabel('의료비 도움 받은 경험')  # x축 이름
plt.ylabel('한 달 생활비')  # y축 이름
plt.title('한 달 생활비에 따른 의료비 지원 경험')  # 그래프 제목
plt.show()

sns.violinplot(x='have', y='month_pay', data=welfare)
plt.title('바이올린 플롯')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# 산점도에서 범주형 변수로 색상 구분
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family' : 'Malgun Gothic'})
sns.barplot(x='month_pay', y='h1411_7', hue='have', data=welfare)
plt.xlabel('한 달 생활비(만 원)')  # x축 이름
plt.ylabel('한 달 의료비(만 원)')  # y축 이름
plt.title('건강보험 가입 여부에 따른 생활비와 의료비의 관계')  # 그래프 제목
plt.show()

welfare['months'].value_counts()


welfare = welfare.rename(columns = {'h1407_9'    :   'not'})  

yes_group = welfare[welfare['have'] == 'yes']['month_pay_medical']
no_group = welfare[welfare['have'] == 'no']['month_pay_medical']

# t-test 수행
from scipy import stats  
stats.ttest_ind(yes_group, no_group, equal_var=False) 



welfare['p1402_8aq1'].corr(welfare['month_pay_medical'])



welfare = welfare.assign(months = np.where(welfare['month_pay'] < 183.000000, 'low', np.where(welfare['month_pay'] <= 543.0000, 'middle', 'high')))
region_ageg = welfare.groupby('months', as_index = False)['h1405_4']\
                    .value_counts(normalize = True)
region_ageg


region_ageg = region_ageg.assign(proportion = region_ageg['proportion']*100).round(1)
region_ageg


pivotdf = region_ageg[['h1405_4','months','proportion']].pivot(index = 'months', 
                                                                 columns='h1405_4',
                                                                 values ='proportion')
pivotdf

pivotdf.plot.barh(stacked = True)

reorder_df = pivotdf.sort_values('high')[['low','middle','high']]
pivotdf.plot.barh(stacked = True)
plt.xlabel('한 달 생활비 ')  # x축 이름
plt.ylabel('건강보험료 미납 경험')  # y축 이름
plt.title('생활비와 건강보험료 미납의 관계')  # 그래프 제목
plt.show()



