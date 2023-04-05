#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import pulp
import streamlit as st
warnings.filterwarnings("ignore")


from pulp import LpProblem,LpVariable, LpMinimize, lpSum

st.title('Product Mix Optimization For Maximizing Profit')
st.subheader('The main goal is to compare the pricing provided by several suppliers for the necessary raw materials and choose the supplier who offers the most affordable alternative for each material.')

from PIL import Image

image = Image.open('logo.png')
st.sidebar.image(image, use_column_width=True)
# st.image(image)


st.sidebar.title("Upload data")
# # File uploader widget
file = st.sidebar.file_uploader("Upload the data file", type=["xlsx", "xls"])

show_def = st.sidebar.checkbox("Use Default data",key = "data_Def")


if file is not None:
    # Read Excel file
        excel_data = pd.ExcelFile(file)
        sheet_names = excel_data.sheet_names
        st.sidebar.write("Sheet Names in the file:", sheet_names)
        max_quantities = pd.read_excel(file, sheet_name=sheet_names[0], index_col=0)
        #st.sidebar.checkbox('max_quantities')
        costs = pd.read_excel(file, sheet_name=sheet_names[2], index_col=0)
        Req_raw_materials= pd.DataFrame(
                {'Total_qty': [1000,800,1160,1250,1340]
                }, index=['RM1', 'RM2', 'RM3', 'RM4', 'RM5'])
        max_quantities= max_quantities.T
        costs = costs.T
        st.sidebar.header('Raw Materials and cost Data')
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.sidebar.checkbox('max_quantities'):
                st.subheader('Raw materials data')
                st.write(max_quantities)

        with col2:
            if st.sidebar.checkbox('costs'):
                st.subheader('costs')
                st.write(costs)

        with col3:
            if st.sidebar.checkbox('Req_raw_materials'):
                st.subheader('Req_raw_materials')
                st.write(Req_raw_materials)

        # Create the LP problem object
        prob = LpProblem('Raw Materials', LpMinimize)

        # Define the decision variables
        vars_dict = LpVariable.dicts('X', [(i, j) for i in costs.index for j in costs.columns], lowBound=0, cat='Continuous')


        # Define the objective function
        prob += lpSum(costs.loc[(i, j)] * vars_dict[(i, j)] for i in costs.index for j in costs.columns)


        # Define the constraints
        for i in max_quantities.index:
            for j in max_quantities.columns:
                prob += vars_dict[(i, j)] <= max_quantities.loc[i, j]

                
        for i in Req_raw_materials.index:
            prob += lpSum(vars_dict[(i,j)] for j in costs.columns) == Req_raw_materials["Total_qty"].loc[i]

    
# Solve the problem
        prob.solve()

        data= []
        for i in costs.index:
            for j in costs.columns:
                var = vars_dict[(i,j)]
                if var.value() != 0:
                    data.append([i, j, var.value(), costs.loc[(i,j)] * var.value()])
        results = pd.DataFrame(data, columns=['Raw Material', 'Supplier', 'Quantity', 'Cost'])
        st.header('Supplier wise raw materials allocation and costs')
        st.write(results)

        html_str = f"""
                        <style>
                        p.b {{
                          font: bold {20}px Source Sans Pro;
                        }}
                        p.b {{
                          color: Green;
                        }}
                        </style>
                        <p class="b">The Total Cost for raw materials required is.</p>
                        <p class="b"> {pulp.value(prob.objective)}</p>
                        """
        st.markdown(html_str, unsafe_allow_html=True)

else:
    if show_def:
            xlsx = pd.ExcelFile('Raw_Data.xlsx')
            # Get the sheet names
            sheet_names = xlsx.sheet_names
            max_quantities = pd.read_excel(xlsx, 'r_m_max',index_col = 0)
            costs = pd.read_excel(xlsx, 'Costs',index_col = 0)

            Req_raw_materials= pd.DataFrame({
                'Total_qty': [270,320,360,350,340]
            }, index=['RM1', 'RM2', 'RM3', 'RM4', 'RM5'])


            # In[7]:


            max_quantities= max_quantities.T
            costs = costs.T
            st.sidebar.header('Raw Materials and cost Data')
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.sidebar.checkbox('max_quantities'):
                    st.subheader('Raw materials data')
                    st.write(max_quantities)

            with col2:
                if st.sidebar.checkbox('costs'):
                    st.subheader('costs')
                    st.write(costs)

            with col3:
                if st.sidebar.checkbox('Req_raw_materials'):
                    st.subheader('Req_raw_materials')
                    st.write(Req_raw_materials)


            # Create the LP problem object
            prob = LpProblem('Raw Materials', LpMinimize)

            # Define the decision variables
            vars_dict = LpVariable.dicts('X', [(i, j) for i in costs.index for j in costs.columns], lowBound=0, cat='Continuous')


            # Define the objective function
            prob += lpSum(costs.loc[(i, j)] * vars_dict[(i, j)] for i in costs.index for j in costs.columns)


            # Define the constraints
            for i in max_quantities.index:
                for j in max_quantities.columns:
                    prob += vars_dict[(i, j)] <= max_quantities.loc[i, j]

                    
            for i in Req_raw_materials.index:
                prob += lpSum(vars_dict[(i,j)] for j in costs.columns) == Req_raw_materials["Total_qty"].loc[i]

                
# Solve the problem
            prob.solve()



            data= []
            for i in costs.index:
                for j in costs.columns:
                    var = vars_dict[(i,j)]
                    if var.value() != 0:
                        data.append([i, j, var.value(), costs.loc[(i,j)] * var.value()])
            results = pd.DataFrame(data, columns=['Raw Material', 'Supplier', 'Quantity', 'Cost'])
            st.header('Supplier wise raw materials allocation and costs')
            st.write(results)


            # In[12]:

            html_str = f"""
                        <style>
                        p.b {{
                          font: bold {20}px Source Sans Pro;
                        }}
                        p.b {{
                          color: Green;
                        }}
                        </style>
                        <p class="b">The Total Cost for raw materials required is.</p>
                        <p class="b"> {pulp.value(prob.objective)}</p>
                        """
            st.markdown(html_str, unsafe_allow_html=True)
            #st.write("The Total Cost raw materials required is",pulp.value(prob.objective))





















# # Read the Excel file
# xlsx = pd.ExcelFile('New_Raw_Data.xlsx')

# # Get the sheet names
# sheet_names = xlsx.sheet_names

# max_quantities = pd.read_excel(xlsx, 'r_m_max',index_col = 0)
# max_quantities

# costs = pd.read_excel(xlsx, 'Costs',index_col = 0)
# costs
# Req_raw_materials= pd.DataFrame({
#      'Total_qty': [270,320,360,350,340]
#  }, index=['RM1', 'RM2', 'RM3', 'RM4', 'RM5'])


# # In[7]:


# max_quantities= max_quantities.T
# costs = costs.T


# # # In[8]:





# # In[9]:


# st.sidebar.header('Raw Materials and cost Data')

# col1, col2, col3 = st.columns(3)

# with col1:
#     if st.sidebar.checkbox('max_quantities'):
#         st.subheader('Raw materials data')
#         st.write(max_quantities)

# with col2:
#     if st.sidebar.checkbox('costs'):
#         st.subheader('costs')
#         st.write(costs)

# with col3:
#     if st.sidebar.checkbox('Req_raw_materials'):
#         st.subheader('Req_raw_materials')
#         st.write(Req_raw_materials)
# In[10]:





# # In[11]:


# import pandas as pd
# from pulp import LpProblem,LpVariable, LpMinimize, lpSum



# # Create the LP problem object
# prob = LpProblem('Raw Materials', LpMinimize)

# # Define the decision variables
# vars_dict = LpVariable.dicts('X', [(i, j) for i in costs.index for j in costs.columns], lowBound=0, cat='Continuous')


# # Define the objective function
# prob += lpSum(costs.loc[(i, j)] * vars_dict[(i, j)] for i in costs.index for j in costs.columns)


# # Define the constraints
# for i in max_quantities.index:
#     for j in max_quantities.columns:
#         prob += vars_dict[(i, j)] <= max_quantities.loc[i, j]

        
# for i in Req_raw_materials.index:
#     prob += lpSum(vars_dict[(i,j)] for j in costs.columns) == Req_raw_materials["Total_qty"].loc[i]

    
# # Solve the problem
# prob.solve()



# data= []
# for i in costs.index:
#     for j in costs.columns:
#         var = vars_dict[(i,j)]
#         if var.value() != 0:
#             data.append([i, j, var.value(), costs.loc[(i,j)] * var.value()])
# results = pd.DataFrame(data, columns=['Raw Material', 'Supplier', 'Quantity', 'Cost'])
# st.header('Supplier wise raw materials allocation and costs')
# st.write(results)


# # In[12]:


# st.write("The Total Cost raw materials required is",pulp.value(prob.objective))


# # In[ ]:














































