from modules import module

#Page symbol and Heading in browser
module.st.set_page_config(page_title = "Sales Prediction",page_icon=":loop:")
df = module.pd.read_csv('clean_data.csv')

if df.shape[1]<3:
    df = module.stand_data(df)
else:
    df = module.stand_data_cat(df)
    sub_Cat = module.st.selectbox('Please Select Sub Category for Prediction',(df['Category'].unique()))
    df = df[df['Category']==sub_Cat]

level = module.st.selectbox('Please Select Data level for Prediction',('Year','Month','Week'))

df_agg = module.agg_ts_data(df)
model = module.modeling(df_agg)
n_period = 12
sig_level = 0.05 
forecast = module.forecast(model,n_period,sig_level)
p2 = module.px.line(df_agg,df_agg.index,y='Sales')

module.st.subheader("Review Modeling Data")
module.st.subheader("------------------------------------------------------")
with module.st.container():
    if module.st.button("Preview Aggregated Data"):
        module.st.dataframe(df_agg.astype(str))

with module.st.container():
    if module.st.button("Review Time Series Data"):
        module.st.plotly_chart(p2,use_container_width=True)  

module.st.subheader("Modeling Results")
module.st.subheader("------------------------------------------------------")
with module.st.container():
    if module.st.button("Model Summary"):
        module.st.write(model.summary())

with module.st.container():
    if module.st.button("Model Accuracy"):
        module.st.write(model.plot_diagnostics())

with module.st.container():
    if module.st.button("See Predicted Values"):
        module.st.write(forecast)

csv_file = forecast.reset_index().to_csv()

module.st.download_button("Download Forecasted File",csv_file,"Forecasted_Data.csv","text/csv",key='download-csv')
