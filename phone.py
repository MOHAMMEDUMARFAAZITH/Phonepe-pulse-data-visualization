import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy


#df = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
df = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")
#state = pd.read_csv(r"E:\GUVI\phonepe\Longitude_Latitude_State_Table3.csv")
state = pd.read_csv("phonepe/Longitude_Latitude_State_Table3.csv")
#districts = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_Districts_Longitude_Latitude2.csv")
districts = pd.read_csv("phonepe/Data_Map_Districts_Longitude_Latitude2.csv")
#districts_tran = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_Transaction4.csv")
districts_tran = pd.read_csv("phonepe/Data_Map_Transaction4.csv")
#app_opening = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_User_Table5.csv")
app_opening = pd.read_csv("phonepe/Data_Map_User_Table5.csv")
#user_device = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_User_Table6.csv")
user_device = pd.read_csv("phonepe/Data_Aggregated_User_Table6.csv")


state = state.sort_values(by='state')
state = state.reset_index(drop=True)
df2 = df.groupby(['State']).sum()[["Total Transactions count","Total Amount"]]
df2 = df2.reset_index()

choropleth_data = state.copy()

for column in df2.columns:
    choropleth_data[column] = df2[column]
choropleth_data = choropleth_data.drop(labels='State', axis=1)

df.rename(columns={'State': 'state'}, inplace=True)
sta_list = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal']
state['state'] = pd.Series(data=sta_list)
state_final = pd.merge(df, state, how='outer', on='state')
districts_tran.rename(columns={'Place Name': 'District'}, inplace=True)
districts_final = pd.merge(districts_tran, districts,
                           how='outer', on=['State', 'District'])




st.balloons()
with st.container():
    st.title(':violet[PhonePe Pulse Data Visualization(2018-2022)📈]')
    #st.image('data/Data-Vizualisation.png')
    st.write(' ')
    st.subheader(
        ':violet[Registered user & App installed -> State and Districtwise:]')
    st.write(' ')
    scatter_year = st.selectbox('Please select the Year',
                                ('2018', '2019', '2020', '2021', '2022'))
    st.write(' ')
    scatter_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10)
    scatter_year = int(scatter_year)
    scatter_reg_df = app_opening[(app_opening['Year'] == scatter_year) & (app_opening['State'] == scatter_state)]

    scatter_register = px.scatter(scatter_reg_df, x="Place Name", y="Registered Users Count",  color="Place Name",
                                  hover_name="Place Name", hover_data=['Year', 'Quarter', 'App Openings'], size_max=60)
    st.plotly_chart(scatter_register)
st.write(' ')


geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(["Geographical analysis", "User device analysis", "Payment Types analysis", "Transacion analysis of States"])






with geo_analysis:
    st.subheader(':violet[Transaction analysis->State and Districtwise:]')
    st.write(' ')
    Year = st.radio('Please select the Year',
                    ('2018', '2019', '2020', '2021', '2022'), horizontal=True)
    st.write(' ')
    Quarter = st.radio('Please select the Quarter',
                       ('1', '2', '3', '4'), horizontal=True)
    st.write(' ')
    Year = int(Year)
    Quarter = int(Quarter)
    plot_district = districts_final[(districts_final['Year'] == Year) & (districts_final['Quarter'] == Quarter)]
    plot_state = state_final[(state_final['Year'] == Year)
                             & (state_final['Quarter'] == Quarter)]
    plot_state_total = plot_state.groupby(
        ['state', 'Year', 'Quarter', 'Latitude', 'Longitude']).sum()
    plot_state_total = plot_state_total.reset_index()
    state_code = ['AN', 'AD', 'AR', 'AS', 'BR', 'CH', 'CG', 'DNHDD', 'DL', 'GA',
                  'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'LA', 'LD', 'MP', 'MH',
                  'MN', 'ML', 'MZ', 'NL', 'OD', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TS',
                  'TR', 'UP', 'UK', 'WB']
    plot_state_total['code'] = pd.Series(data=state_code)
    fig1 = px.scatter_geo(plot_district,
                          lon=plot_district['Longitude'],
                          lat=plot_district['Latitude'],
                          color=plot_district['Total Amount'],
                          size=plot_district['Total Transactions count'],
                          hover_name="District",
                          hover_data=["State", 'Total Amount', 'Total Amount',
                                      'Total Transactions count', 'Year', 'Quarter'],
                          title='District',
                          size_max=22,)
    fig1.update_traces(marker={'color': "#CC0044",
                               'line_width': 1})
    fig2 = px.scatter_geo(plot_state_total,
                          lon=plot_state_total['Longitude'],
                          lat=plot_state_total['Latitude'],
                          hover_name='state',
                          text=plot_state_total['code'],
                          hover_data=['Total Transactions count',
                                      'Total Amount', 'Year', 'Quarter'],
                          )
    fig2.update_traces(marker=dict(color="#D5FFCC", size=0.3))
    fig = px.choropleth(
        choropleth_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='Total Amount',
        color_continuous_scale='twilight',
        hover_data=['Total Transactions count', 'Total Amount']
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig2.data[0])
    fig.update_layout(height=1000, width=1000)
    st.write(' ')
    st.write(' ')
    st.plotly_chart(fig)


with Device_analysis:
     st.subheader(':violet[User Device analysis->Statewise:]')
     tree_map_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                          'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                          'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                          'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                          'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                          'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                          'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                          'uttarakhand', 'west-bengal'), index=10, key='tree_map_state')
     tree_map_state_year = int(st.radio('Please select the Year',
                                       ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='tree_map_state_year'))
     tree_map_state_quater = int(st.radio('Please select the Quarter',
                                         ('1', '2', '3', '4'), horizontal=True, key='tree_map_state_quater'))
     user_device_treemap = user_device[(user_device['State'] == tree_map_state) & (user_device['Year'] == tree_map_state_year) &
                                      (user_device['Quarter'] == tree_map_state_quater)]
     user_device_treemap['Brand_count'] = user_device_treemap['Registered Users Count'].astype(
        str)


     user_device_treemap_fig = px.treemap(user_device_treemap, path=['State', 'Brand Name'], values='Percentage Share of Brand', hover_data=['Year', 'Quarter'],
                                         color='Brand_count',
                                         title='User device distribution in ' + tree_map_state +
                                         ' in ' + str(tree_map_state_year)+' at '+str(tree_map_state_quater)+' quater',)
     st.plotly_chart(user_device_treemap_fig)
    

     bar_user = px.bar(user_device_treemap, x='Brand Name', y='Brand_count', color='Brand Name',
                      title='Bar chart analysis', color_continuous_scale='sunset',)
     st.plotly_chart(bar_user)




with payment_analysis:
    st.subheader(':violet[Payment type Analysis -> 2018 - 2022:]')
    # querypa = 'select * from agg_transaction_table'
    # payment_mode = pd.read_sql(querypa, con=connection)
    #payment_mode = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
    payment_mode = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")
    pie_pay_mode_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                              'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                              'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                              'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                              'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                              'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                              'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                              'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                              'uttarakhand', 'west-bengal'), index=10, key='pie_pay_mode_state')
    pie_pay_mode_year = int(st.radio('Please select the Year',
                                     ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='pie_pay_year'))
    pie_pay_mode__quater = int(st.radio('Please select the Quarter',
                                        ('1', '2', '3', '4'), horizontal=True, key='pie_pay_quater'))
    pie_pay_mode_values = st.selectbox(
        'Please select the values to visualize', ('Total Transactions count', 'Total Amount'))
    pie_payment_mode = payment_mode[(payment_mode['Year'] == pie_pay_mode_year) & (
        payment_mode['Quarter'] == pie_pay_mode__quater) & (payment_mode['State'] == pie_pay_mode_state)]
    


    pie_pay_mode = px.pie(pie_payment_mode, values=pie_pay_mode_values,
                          names='Payment Mode', hole=.5, hover_data=['Year'])
    


    pay_bar = px.bar(pie_payment_mode, x='Payment Mode',
                     y=pie_pay_mode_values, color='Payment Mode')
    st.plotly_chart(pay_bar)
    st.plotly_chart(pie_pay_mode)



with transac_yearwise:
    st.subheader(':violet[Transaction analysis->Statewise:]')
    transac_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10, key='transac')
    transac__quater = int(st.radio('Please select the Quarter',
                                   ('1', '2', '3', '4'), horizontal=True, key='trans_quater'))
    transac_type = st.selectbox('Please select the Mode',
                                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transactype')
    transac_values = st.selectbox(
        'Please select the values to visualize', ('Total Transactions count', 'Total Amount'), key='transacvalues')
    #payment_mode_yearwise = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
    payment_mode_yearwise = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")

    # querypay_year = 'select * from agg_transaction_table'
    # payment_mode_yearwise = pd.read_sql(querypay_year, con=connection)

    new_df = payment_mode_yearwise.groupby(
        ['State', 'Year', 'Quarter', 'Payment Mode']).sum()
    new_df = new_df.reset_index()
    chart = new_df[(new_df['State'] == transac_state) &
                   (new_df['Payment Mode'] == transac_type) & (new_df['Quarter'] == transac__quater)]


    year_fig = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',
                      title='Transacion analysis '+transac_state + ' regarding to '+transac_type)
    st.plotly_chart(year_fig)
    
    pay_bar = px.bar(pie_payment_mode, x='Payment Mode',
                     y=pie_pay_mode_values, color='Payment Mode')
    st.plotly_chart(pay_bar)


# -------------------------------------------- Sidebar --> for overall india Data comparisons -------------------------------------------------
with st.sidebar:
    # -------------------------- Bar chart ofoverall india transacion data  -----------------------------------------------------------------
    st.subheader(':violet[Overall India Analysis:]')
    overall_values = st.selectbox(
        'Please select the values to visualize', ('Total Transactions count', 'Total Amount'), key='values')
    overall = new_df.groupby(['Year']).sum()
    overall.reset_index(inplace=True)

    overall = px.bar(overall, x='Year', y=overall_values, color=overall_values,
                     title='Overall pattern of Transacion all over India', color_continuous_scale='sunset',)
    overall.update_layout(height=350, width=350)
    st.plotly_chart(overall)
   


    # --------------------------Bar chart of overall india user device analysis --------------------------------------------------------------
    # query_device = 'select * from agg_userbydevice_table'
    # user_device_overall = pd.read_sql(query_device, con=connection)
    #user_device_overall = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_User_Table6.csv", index_col=0)
    user_device_overall = pd.read_csv("phonepe/Data_Aggregated_User_Table6.csv", index_col=0)
    overall_device = user_device_overall.groupby(['Brand Name', 'Year']).sum()
    overall_device.reset_index(inplace=True)

    overall_dev_fig = px.bar(overall_device, x='Year', y='Registered Users Count',
                             color='Registered Users Count', title='Customer Device pattern from 2018 - 2022')
    overall_dev_fig.update_layout(height=350, width=350)
    st.plotly_chart(overall_dev_fig)


    # --------------------------Bar chart of overall india registered and app opening --------------------------------------------------------
    # query_reg = 'select * from district_map_registering_table'
    # overall_reg = pd.read_sql(query5, con=connection)
    #overall_reg = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_User_Table5.csv")
    overall_reg = pd.read_csv("phonepe/Data_Map_User_Table5.csv")
    overall_reg = overall_reg.groupby(['State', 'Year']).sum()
    overall_reg.reset_index(inplace=True)

    overall_reg = px.bar(overall_reg, x='Year', y=['Registered Users Count',"App Openings"], barmode='group', title='Phonepe installation from 2018 - 2022')
    overall_reg.update_layout(height=350, width=350)
    st.plotly_chart(overall_reg)
