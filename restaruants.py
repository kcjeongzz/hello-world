import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide") # width of dataframe widens
st.title("Top 100 US Chain Restaurants Analysis")
st.header("Segment / Menu ")

col1, col2 = st.columns(2) # layout setting

df = pd.read_csv('Top100Chains.csv', sep=',', skipinitialspace=True)
df['MENU CATEGORY'] = df['MENU CATEGORY'].str.strip()
df['SEGMENT'] = df['SEGMENT'].str.strip()
df['yoy'] = df['YOY SALES CHANGE']
df['yoy'] = df['yoy'].str.replace('%','',) # removing %
df['yoy'] = pd.to_numeric(df['yoy']) # str to num to calculate mean
df_group_segment = df.groupby('SEGMENT', as_index=False).agg({'CHAIN': 'count', 'yoy': 'mean'})
df_group_menu = df.groupby('MENU CATEGORY', as_index=False).agg({'CHAIN': 'count', 'yoy': 'mean'})
with col1: # apply new layout
    st.markdown("""Segment Analysis""")
    st.write(df_group_segment)

with col2:
    st.markdown('Menu Analysis')
    st.dataframe(df_group_menu)

unique_menu = sorted(df['MENU CATEGORY'].unique())
menu_all=[]
menu_all=unique_menu[:]
menu_all.append("All") # giving select all options
menu_all = sorted(menu_all)
selected_menu = st.sidebar.multiselect("Select Food Category", menu_all, menu_all[0])

if 'All' in selected_menu: # when select all selected
    selected_menu = unique_menu # choose all

unique_segment = sorted(df.SEGMENT.unique())
segment_all = []
segment_all = unique_segment[:]
segment_all.append("All")
segment_all = sorted(segment_all)
selected_segment = st.sidebar.multiselect('Select Segment', segment_all, segment_all[0])

if 'All' in selected_segment:
    selected_segment = unique_segment

df_selected = df[(df['MENU CATEGORY'].isin(selected_menu)) & df.SEGMENT.isin(selected_segment)]

st.write("""***""")

st.subheader('Selected Data')
st.write('Data Dimension ' + str(df_selected.shape[0]) + ' rows and ' + str(df_selected.shape[1]) + ' columns.')
st.dataframe(df_selected)

st.write("""***""")

df_count = df.groupby(['SEGMENT'], as_index=False)['CHAIN'].count()
x = df_group_segment['SEGMENT']
y = df_group_segment['CHAIN']
y2 = df_group_segment['yoy']

st.write('Number of Chains by Segment')
f, ax1 = plt.subplots(figsize=(7, 3))
ax2 = ax1.twinx()
ax1.set_xlabel('Segment')
ax1.set_ylabel('Chain')
ax1 = plt.bar(x,y)


ax2.set_ylabel('yoy')
ax2 = plt.bar(x,y2)
plt.tight_layout()

st.pyplot(f)

# x = df_count['SEGMENT']
# y = df_count['CHAIN']

# st.write('Number of Chains by Segment')
# f, ax = plt.subplots(figsize=(7, 3))
# ax = plt.bar(x,y)
# plt.xticks(fontsize=6, rotation=45)
# plt.xlabel('Segment', fontsize=10)
# plt.ylabel('# of Chains', fontsize=10)
#
# st.pyplot(f)