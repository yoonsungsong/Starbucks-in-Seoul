# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## 공공데이터 활용 서울 스타벅스 시각화
#
# **환경**
#
# - Mac Os
# - Python 3.9.4 (default, Apr  9 2021, 09:32:38)
#
# **데이터 개요**
#
# - 2021년 9월 30일 기준
# - 상권업종중분류명이 "커피점/카페"로 등록된 카페 (제과/제빵은 포함하지 않았음)
# - 데이터 출처 :
#     - 공공데이터포털(data.go.kr) : 소상공인시장진흥공단_상가(상권)정보
#     - https://www.data.go.kr/data/15083033/fileData.do
#
# **프로젝트 개요**
#
# - 공공데이터를 활용하여 서울의 스타벅스에 대한 다양한 시각화를 통해 분석해보고자 한다.(연습)
#
# **프로젝트 상세**
#
# - barplot과 pieplot을 통해 서울 스타벅스 점포 수를 시각화 해보고자 한다.
# - folium 패키지를 활용하여 지도 위에 서울의 스타벅스 분포 정도를 시각화 해보고자 한다.
# - folium documentation : https://python-visualization.github.io/folium/index.html
#

# +
# 기초 라이브러리 불러오기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import warnings
warnings.filterwarnings(action='ignore')

import matplotlib
matplotlib.rc('font', family='AppleGothic')
matplotlib.rc('axes', unicode_minus=False)

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

# pd.options.display.max_rows=100
# pd.options.display.max_columns=100
# pd.set_option('display.float_format','{:.4f}'.format)
# -

# ## 1. Load Dataset

# 임시로 하나만 우선 살펴보기
temp = pd.read_csv("data/소상공인시장진흥공단_상가(상권)정보_서울_202109.csv", encoding='utf-8')
temp.head()

# +
# data 폴더에 있는 모든 csv 파일을 읽어오기 위해 glob을 사용
from glob import glob

# csv 목록 불러오기
file_names = glob("data/*.csv")
# file_names
total = pd.DataFrame()
# 모든 csv 병합
for file_name in file_names:
    temp = pd.read_csv(file_name, encoding='utf-8')
    total = pd.concat([total, temp])

# reset index
total.reset_index(inplace=True, drop=True)
total.head()
# -

total.columns

# 분석에 필요한 column 고르기
data_columns = ['상가업소번호', '상호명', '지점명', '상권업종대분류명', '상권업종중분류명', '시도명', '시군구명', '행정동명', '경도', '위도', '데이터기준일자'] 
data = total[data_columns]
data.head()

data.info()

total.info()

# 메모리 낭비를 막기 위해 필요없는 변수는 제거한다.
del total

total.head() # 삭제 완료.

# ## 2. Data Exploration

# #### 전국 커피 전문점 

# set(data['상권업종대분류명'])
set(data['상권업종중분류명'])

# +
# 상권업종중분류명이 "커피점/카페" 인 곳
df_coffee = data[data["상권업종중분류명"] == "커피점/카페"]
# index 다시 세팅
df_coffee.index = range(len(df_coffee))

print("전국 커피 전문점 점포 수 : ", len(df_coffee))
df_coffee.head()
# -

# #### 서울내 커피 전문점 

set(data["시도명"])

# 커피전문점 중에 "서울"에 위치하고 있는 점포만 뽑아낸다.
df_seoul_coffee = df_coffee[df_coffee["시도명"] == "서울특별시"]
df_seoul_coffee.index = range(len(df_seoul_coffee))
print('서울시 내 커피 전문점 점포 수 :', len(df_seoul_coffee))
df_seoul_coffee.head()

# #### 전국 스타벅스

# 스타벅스 상호를 가진 모든 커피전문점
df_starbucks = df_coffee[df_coffee["상호명"].str.contains("스타벅스")]
df_starbucks.index = range(len(df_starbucks))
print('전국 스타벅스 점포 수 :', len(df_starbucks))
df_starbucks.head()

# #### 서울 스타벅스

# 서울에 있는 스타벅스
df_seoul_starbucks = df_starbucks[df_starbucks["시도명"] == "서울특별시"]
df_seoul_starbucks.index = range(len(df_seoul_starbucks))
print('서울시 내 스타벅스 점포 수 :', len(df_seoul_starbucks))
df_seoul_starbucks.head()

# 구별로 스타벅스 수를 구한다.
df_seoul_starbucks['시군구명'].value_counts()

# ## Data Visualization

plt.figure(figsize=(10, 6))
plt.title("서울의 스타벅스 분포", fontdict={"fontsize" : 20})
plt.bar(df_seoul_starbucks['시군구명'].value_counts().index, df_seoul_starbucks['시군구명'].value_counts().values)
plt.xticks(rotation='vertical')
# plt.xticks(rotation='horizontal')
plt.savefig("starbucks_barplot.png")
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data = df_seoul_starbucks, y='시군구명')
plt.savefig("starbucks_countplot.png")
plt.show()

# +
# 땅값, 회사 수 등과 비교 가능 스타벅스와 관계.(회귀분석, 상관관계 분석)
# -

plt.figure(figsize=(8,8))
plt.pie(df_seoul_starbucks['시군구명'].value_counts().values,
        labels=df_seoul_starbucks['시군구명'].value_counts().index,
        autopct='%d%%',
        colors=sns.color_palette('hls',len(df_seoul_starbucks['시군구명'].value_counts().index)),
        textprops={'fontsize':12})
plt.axis('equal')
plt.title("Pie chart for Starbusks count", fontsize=16, pad=50)
plt.savefig("starbucks_piechart.png")
plt.show()

# ### 지도 위에 시각화하기

df_seoul_starbucks.head(1)

# 스타벅스가 어디에 있는지 경도와 위도를 활용해 나타냅니다.
df_seoul_starbucks[["지점명", "경도", "위도"]]

# +
# # !pip install folium
import folium

# 중심 지정
lat = df_seoul_starbucks['위도'].mean()
long = df_seoul_starbucks['경도'].mean()

m = folium.Map([lat, long], zoom_start=11)

# 지도위에 표시
for i in df_seoul_starbucks.index:
    sub_lat = df_seoul_starbucks.loc[i, '위도']
    sub_long = df_seoul_starbucks.loc[i, '경도']
    
    title = df_seoul_starbucks.loc[i, '지점명']
    
    #지도에 데이터 찍어서 보여주기
    folium.Marker([sub_lat, sub_long], tooltip = title).add_to(m)

m.save('starbucks_mark.html')
m

# +
# 동그라미 마크 표시하기
m = folium.Map([lat, long], zoom_start=11, tiles='OpenStreetMap') #tiles = 'Stamen Toner', 'OpenStreetMap', 'Stamen Terrain'

for i in df_seoul_starbucks.index:
    sub_lat = df_seoul_starbucks.loc[i, '위도']
    sub_long = df_seoul_starbucks.loc[i, '경도']
    
    title = df_seoul_starbucks.loc[i, '지점명']
    
    folium.CircleMarker([sub_lat, sub_long], color='green', radius = 4, tooltip = title).add_to(m)

m.save('starbucks_cmark.html')
m

# +
# 코로플레스를 위한 시/군/구별 좌표 json파일 가져오기
import json

geo_path = 'skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))
# -

df_seoul_starbucks_count = pd.pivot_table(df_seoul_starbucks, index='시군구명', values='상가업소번호', aggfunc='count')

# +
# 코로플레스 지도 그리기
m = folium.Map(location=[lat, long], zoom_start=11, tiles='Stamen Toner')  #tiles = 'Stamen Toner', 'OpenStreetMap', 'Stamen Terrain'

m.choropleth(
    geo_data = geo_str,
    data = df_seoul_starbucks_count['상가업소번호'],
    columns = ['시군구명','상가업소번호'],
               fill_color = 'YlGn', # 'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'
               key_on = 'feature.properties.name',
               legend_name='Number of Parking lots (%)')

m.save('starbucks_choropleth.html')
m
# -

# ## 결론
#
# **프로젝트에 대하여**
#
# - 공공데이터셋은 모든 상권 데이터가 들어있지만, 빠른 연습을 위해 서울에 있는 스타벅스 데이터만 뽑아서 진행하였다.
# - 간단한 결과이고 특별한 관찰은 없었지만, 그래프 시각화와 지도 시각화를 진행해보았다.
#
#
# **관찰 결과**
#
# - 강남구, 중구, 서초구, 송파구, 종로구 등 순으로 스타벅스가 많이 들어서 있다.
# - 특별한 관찰 결과는 없다. 연습이기 때문.
#
# **Develop Project**
#
# - 다양한 분석을 시행할 수 있으며, 땅값, 회사 수 등과 스타벅스 입점 수와의 상관관계를 살펴볼 수도 있울 것이다.
# - 스타벅스 뿐아니라 다른 브랜드에 대해서도 분석해볼 수 있다.
# - 프랜차이즈 비율에 대해서도 살펴볼 수 있다.
# - 커피전문점이 아닌 다른 항목에 대해서도 분석해볼 수 잇다.


