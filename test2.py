#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[5]:

st.header('Test app')

with st.sidebar:
    st.write('There will be other pages here.')

file = st.file_uploader("Choose an excel file", type = 'xlsx')

if file is not None:
    x = pd.read_excel(file)
    
    
    #Pivot the data
    pivoted = pd.pivot_table(x, index = ['branch_long'], aggfunc = {'id':lambda val: len(val.unique())}).reset_index()
    
    pivoted = pivoted.sort_values(by = 'id', ascending = True)
    
    #Create a column with these figures cleaned and with a k to represent thousand
    
    pivoted['id_tidy'] = pivoted.apply(lambda x: "{:,}".format(x['id']), axis = 1)
    
    #Function to add the 'k'
    def tidy_nums(x):
        if ',' in x:
            if x[1] == ',':
                num = x[0]
                return num+'.'+x[2]+'k'
            elif x[2] == ',':
                num = x[:2]
                return num+'.'+x[3]+'k'
            elif x[2] == ',':
                num = x[:3]
                return num+'.'+x[4]+'k'
            else:
                return x
        else:
            return x
    
    pivoted['short_id'] = pivoted['id_tidy'].apply(tidy_nums)
    
    #Create a set of groupby objects for different metrics
    sun = x.groupby(['branch_long', 'catg']).nunique().reset_index()
    tree = x.groupby(['branch_long', 'Rule', 'Description']).nunique().reset_index()
    
    total_breaks = x.groupby(['branch_long']).count().reset_index()
    total_breaks = total_breaks[['branch_long', 'id']]
    
    total_breaks['id_tidy'] = total_breaks.apply(lambda x: "{:,}".format(x['id']), axis = 1)
    total_breaks['short_id'] = total_breaks['id_tidy'].apply(tidy_nums)

    b_id = pivoted[pivoted['branch_long'] == 'Brussels']['short_id'][0]
    b_id = str(b_id)
    
    b_id_total = total_breaks[total_breaks['branch_long'] == 'Brussels']['short_id'][0]
    b_id_total = str(b_id_total)


    
    #Visualise things        
    col1, col2 = st.columns(2)
    
    with col2:  
        fig = px.sunburst(sun, path = ['catg', 'branch_long'], values = 'id',
                          color = 'id', color_continuous_scale = 'RdBu_r',
                          height = 600, width = 800)
        st.plotly_chart(fig, use_container_width = False)
    
    with col1:
        fig = px.scatter(pivoted, x="branch_long", y="id",
                         size = 'id', color = 'branch_long',
                         labels = {'id': 'Unique IDs',
                                   'branch_long':'branch'},
                         log_x = False, size_max = 100, height = 570, width = 750)
        fig.update_yaxes(visible = True, showticklabels = True)
        st.plotly_chart(fig, use_container_width = False)
     
    padding, col1, padding = st.columns([1,2,1])
    
    with col1:
        fig = px.treemap(tree, path = [px.Constant("all"), 'branch_long', 'Rule',
                                       'id'], values = 'id', color = 'id',
                         color_continuous_scale = 'RdBu_r', height = 700, width = 900)
        fig.update_traces(hoverinfo = 'skip', hovertemplate = None, marker_line_width = 0)
        fig.update_layout(margin = dict(t=50, l =25, r = 25, b = 25))
        st.plotly_chart(fig, use_container_width = False)

with st.form("my_form"):
    st.write("Inside the form")
    
    option = st.selectbox(
    'Please select a branch',
    ('','Belgium', 'France', 'Singapore'))
    
    region = st.radio(
    'Select a category',
    ('Party', 'Account', 'Holiday'))
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if option == 'Belgium':
            
            st.metric('Unique IDs', b_id)
            st.metric('Total breaks', b_id_total)
            
            df = px.data.iris()
            fig = px.scatter(df, x="sepal_width", y="sepal_length", width = 500)
            st.plotly_chart(fig, use_container_width = False)
            
            if region == 'Party':
                st.write('This returns a party chart')
            elif region == 'Account':
                st.write('This returns an account chart')
        
        elif option == 'France':
            df = px.data.iris()
            fig = px.scatter(df, x="sepal_width", y="sepal_length", width = 500)
            st.plotly_chart(fig, use_container_width = False)
            
            if region == 'Party':
                st.write('This returns a party chart in France')
            elif region == 'Account':
                st.write('This returns an account chart in France')
            

# In[ ]:

