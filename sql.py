import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy

#Mysql server connection using sqlalchemy
#user = 'root'
#password = 'razith10113a'
#host = 'localhost'
#port = 3306
#database = 'dt4'
#connection = sqlalchemy.create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))

#Fetching datas from various resources

#query1 = 'select * from data_aggregated_transaction_table1'
#df = pd.read_sql(query1, con=connection)
#df = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
df = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")

#query2 = 'select * from longitude_latitude_state_table3'
#state = pd.read_sql(query2, con=connection)
#state = pd.read_csv(r"E:\GUVI\phonepe\Longitude_Latitude_State_Table3.csv")
state = pd.read_csv("phonepe/Longitude_Latitude_State_Table3.csv")

#query3 = 'select * from data_map_districts_longitude_latitude2'
#districts = pd.read_sql(query3, con=connection)
#districts = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_Districts_Longitude_Latitude2.csv")
districts = pd.read_csv("phonepe/Data_Map_Districts_Longitude_Latitude2.csv")

#query4 = 'select * from data_map_transaction4'
#districts_tran = pd.read_sql(query4, con=connection)
#districts_tran = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_Transaction4.csv")
districts_tran = pd.read_csv("phonepe/Data_Map_Transaction4.csv")

#query5 = 'select * from data_map_user_table5'
#app_opening = pd.read_sql(query5, con=connection)
#app_opening = pd.read_csv(r"E:\GUVI\phonepe\Data_Map_User_Table5.csv")
app_opening = pd.read_csv("phonepe/Data_Map_User_Table5.csv")

#query6 = 'select * from data_aggregated_user_table6'
#user_device = pd.read_sql(query6, con=connection)
#user_device = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_User_Table6.csv")
user_device = pd.read_csv("phonepe/Data_Aggregated_User_Table6.csv")


#Data Preprocessing for visualization

state = state.sort_values(by='state')
state = state.reset_index(drop=True)
df2 = df.groupby(['State']).sum()[["Total Transactions count","Total Amount"]]
df2 = df2.reset_index()
choropleth_data = state.copy()

for column in df2.columns:
    choropleth_data[column] = df2[column]
choropleth_data = choropleth_data.drop(labels='State', axis=1)

df.rename(columns={'State': 'state'}, inplace=True)
sta_list = ['andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar','chandigarh',
           'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana','himachal-pradesh',
           'jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep','madhya-pradesh','maharashtra',
           'manipur','meghalaya','mizoram','nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
           'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal']
state['state'] = pd.Series(data=sta_list)
state_final = pd.merge(df, state, how='outer', on='state')
districts_tran.rename(columns={'Place Name': 'District'}, inplace=True)
districts_final = pd.merge(districts_tran, districts,how='outer', on=['State', 'District'])

with st.container():
    st.title('PhonePe Pulse Data Visualization(2018-2022)')
    st.subheader('Registered user & App installed -> State and Districtwise')
    col1,col2,col3= st.columns(3)
    with col1:    
            scatter_year = int(st.selectbox('Please select the Year',('2018', '2019', '2020', '2021', '2022')))
    with col2:    
            scatter_quarter = int(st.selectbox('Please select the Quarter',('1', '2', '3', '4')))
    with col3:    
            scatter_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi','goa', 'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan','sikkim','tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=30)
    scatter_reg_df = app_opening[(app_opening['Year'] == scatter_year) & (app_opening['State'] == scatter_state) & (app_opening['Quarter'] == scatter_quarter)]
    #Scatter = px.scatter(scatter_reg_df, x="Place Name", y="Registered Users Count",  color="Place Name",hover_name="Place Name", hover_data=['Year', 'Quarter', 'App Openings'], size_max=60)
    Bar = px.bar(scatter_reg_df, x="Place Name", y="Registered Users Count",  color="Place Name",hover_name="Place Name", hover_data=['Year', 'Quarter', 'App Openings'])    
    Bar.update_layout(height=400,width=1500)    
    st.plotly_chart(Bar)

geo_analysis, Device_analysis, payment_analysis, transac_yearwise,Overall_India_Analysisst = st.tabs(["Geographical analysis","Overall_India_Analysisst","User device analysis", "Payment Types analysis", "Transacion analysis of States"])

with geo_analysis:
    st.subheader('Transaction analysis->State and Districtwise')
    col1,col2= st.columns(2)
    with col1:
            Year = int(st.selectbox('Please select the Year',('2018', '2019', '2020', '2021', '2022'),key='Year'))
    with col2:    
            Quarter = int(st.selectbox('Please select the Quarter',('1', '2', '3', '4'),key='Quarter'))
    plot_district = districts_final[(districts_final['Year'] == Year) & (districts_final['Quarter'] == Quarter)]
    plot_state = state_final[(state_final['Year'] == Year)& (state_final['Quarter'] == Quarter)]
    plot_state_total = plot_state.groupby(['state', 'Year', 'Quarter', 'Latitude', 'Longitude']).sum()
    plot_state_total = plot_state_total.reset_index()
    state_code = ['AN','AD','AR','AS','BR','CH','CG','DNHDD','DL','GA','GJ','HR','HP','JK','JH','KA','KL','LA','LD','MP','MH',
                  'MN','ML','MZ','NL','OD','PY','PB','RJ','SK','TN','TS','TR','UP','UK','WB']
    plot_state_total['code'] = pd.Series(data=state_code)
    fig1 = px.scatter_geo(plot_district,lon=plot_district['Longitude'],lat=plot_district['Latitude'],
                          color=plot_district['Total Amount'],size=plot_district['Total Transactions count'],
                          hover_name="District",hover_data=["State", 'Total Amount', 'Total Amount',
                          'Total Transactions count', 'Year', 'Quarter'],title='District',size_max=22,)
    fig1.update_traces(marker={'color': "#FFFF40",'line_width': 2})
    fig2 = px.scatter_geo(plot_state_total,lon=plot_state_total['Longitude'],lat=plot_state_total['Latitude'],
                          hover_name='state',text=plot_state_total['code'],
                          hover_data=['Total Transactions count','Total Amount', 'Year', 'Quarter'],)
    fig2.update_traces(marker=dict(color="black", size=0.5))
    fig = px.choropleth(choropleth_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',locations='state',color='Total Amount',color_continuous_scale='twilight',hover_data=['Total Transactions count', 'Total Amount'])
    fig.update_geos(fitbounds="locations",visible=False)
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig2.data[0])
    fig.update_layout(height=1000,width=1500)
    st.plotly_chart(fig)

with Device_analysis:
     st.subheader('User Device analysis->Statewise')
     col1,col2,col3= st.columns(3)
     with col1:
             tree_map_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                          'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                          'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim','tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                          'uttarakhand', 'west-bengal'), index=30, key='tree_map_state')
     with col2:     
             tree_map_state_year = int(st.selectbox('Please select the Year',('2018', '2019', '2020', '2021', '2022'), key='tree_map_state_year'))
     with col3:     
             tree_map_state_quater = int(st.selectbox('Please select the Quarter',('1', '2', '3', '4'),key='tree_map_state_quater'))
     user_device_treemap = user_device[(user_device['State'] == tree_map_state) & (user_device['Year'] == tree_map_state_year) &(user_device['Quarter'] == tree_map_state_quater)]
     user_device_treemap['Brand_count'] = user_device_treemap['Registered Users Count'].astype(str)
     user_device_treemap_fig = px.treemap(user_device_treemap, path=['State', 'Brand Name'], values='Percentage Share of Brand', hover_data=['Year', 'Quarter'],
                                         color='Brand_count',title='User device distribution in ' + tree_map_state +' in ' + str(tree_map_state_year)+' at '+str(tree_map_state_quater)+' quater')    
     bar_user = px.bar(user_device_treemap, x='Brand Name', y='Brand_count',color='Brand Name',title='Bar chart analysis',pattern_shape_sequence=["\\", "\\", "\\","\\","\\","\\", "\\", "\\","\\","\\","\\"],pattern_shape='Brand Name')
     bar_user.update_layout(height=500,width=500) 
     user_device_treemap_fig.update_layout(height=500,width=500)    
     col1,col2,col3= st.columns(3)
     with col1:     
             st.plotly_chart(user_device_treemap_fig)
     with col3:
             st.plotly_chart(bar_user)

with payment_analysis:
    st.subheader('Payment type Analysis -> 2018 - 2022')
    #payment_mode = pd.read_sql(query1, con=connection)
    #payment_mode = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
    payment_mode = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
	    pie_pay_mode_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                              'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                              'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                              'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim','tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                              'uttarakhand', 'west-bengal'), index=30, key='pie_pay_mode_state')
    with col2:    
	    pie_pay_mode_year = int(st.selectbox('Please select the Year',('2018', '2019', '2020', '2021', '2022'),key='pie_pay_year'))
    with col3:    
	    pie_pay_mode__quater = int(st.selectbox('Please select the Quarter',('1', '2', '3', '4'),key='pie_pay_quater'))
    with col4:    
	    pie_pay_mode_values = st.selectbox('Please select the values to visualize', ('Total Transactions count', 'Total Amount'))
    pie_payment_mode = payment_mode[(payment_mode['Year'] == pie_pay_mode_year) & (payment_mode['Quarter'] == pie_pay_mode__quater) & (payment_mode['State'] == pie_pay_mode_state)]
    pie_pay_mode = px.pie(pie_payment_mode, values=pie_pay_mode_values,names='Payment Mode', hole=.6, hover_data=['Year'])
    pay_bar = px.bar(pie_payment_mode, x='Payment Mode',y=pie_pay_mode_values, color='Payment Mode',pattern_shape_sequence=[".", ".", ".",".","."],pattern_shape='Payment Mode')
    col1,col2 = st.columns(2) 
    with col1:   	
	    st.plotly_chart(pay_bar)
    with col2:
    	    st.plotly_chart(pie_pay_mode)

with transac_yearwise:
    st.subheader('Transaction analysis->Statewise')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
            transac_state = st.selectbox('Please select State',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim','tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=30, key='transac')
    with col2:    
            transac__quater = int(st.selectbox('Please select the Quarter',('1', '2', '3', '4'),key='trans_quater'))
    with col3:    
            transac_type = st.selectbox('Please select the Mode',('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transactype')
    with col4:    
            transac_values = st.selectbox('Please select the values to visualize', ('Total Transactions count', 'Total Amount'), key='transacvalues')
    #payment_mode_yearwise = pd.read_sql(query1, con=connection)
    #payment_mode_yearwise = pd.read_csv(r"E:\GUVI\phonepe\Data_Aggregated_Transaction_Table1.csv")
    payment_mode_yearwise = pd.read_csv("phonepe/Data_Aggregated_Transaction_Table1.csv")
    new_df = payment_mode_yearwise.groupby(['State', 'Year', 'Quarter', 'Payment Mode']).sum()
    new_df = new_df.reset_index()
    chart = new_df[(new_df['State'] == transac_state) &(new_df['Payment Mode'] == transac_type) & (new_df['Quarter'] == transac__quater)]
    year_bar = px.bar(chart, x=['Year'], y=transac_values, color=transac_values, color_continuous_scale='armyrose',title='Transacion analysis '+transac_state + ' regarding to '+transac_type)
    year_fig = px.pie(chart, values=transac_values,hover_data=['Year'])  
    col1,col2 = st.columns(2)
    with col1:
            st.plotly_chart(year_bar)
    with col2:
            st.plotly_chart(year_fig)

with Overall_India_Analysisst:
    st.subheader("Overall India Analysis")
    overall_values = st.selectbox('Please select the values to visualize', ('Total Transactions count', 'Total Amount'), key='values')    
    col1,col2= st.columns(2)
    #Bar chart ofoverall india transacion data
    with col1:
    	overall = new_df.groupby(['Year']).sum()
    	overall.reset_index(inplace=True)
    	overall = px.bar(overall, x='Year', y=overall_values, color=overall_values,title='Overall pattern of Transacion all over India', color_continuous_scale='sunset')
    	st.plotly_chart(overall)
    with col2:
    	#Bar chart of overall india registered and app opening
    	#overall_reg = pd.read_sql(query5,con=connection)
    	#overall_reg= pd.read_csv(r"E:\GUVI\phonepe\Data_Map_User_Table5.csv")
    	overall_reg = pd.read_csv("phonepe/Data_Map_User_Table5.csv")
    	overall_reg = overall_reg.groupby(['State','Year']).sum()
    	overall_reg.reset_index(inplace=True)
    	overall_reg = px.bar(overall_reg, x='Year',y=['Registered Users Count',"App Openings"],barmode='group',title='Phonepe installation from 2018 - 2022')
    	st.plotly_chart(overall_reg)
