from modules import module

#Page symbol and Heading in browser
module.st.set_page_config(page_title = "Sales Prediction",page_icon=":loop:")

df = module.pd.read_csv('input.csv')
if df.shape[1]<3:
    df = module.stand_data(df)
else:
    df = module.stand_data_cat(df)

module.st.subheader("Data Cleaning")
module.st.subheader("------------------------------------------------------")

with module.st.container():
    module.st.write("Null Values Present",(df.isna().sum()).sum())
    null_option = module.st.radio("Remove null values",("Yes","No"))
    if null_option=="Yes":
        i = (df.isna().sum()).sum()
        df = df.dropna()
        j = (df.isna().sum()).sum()
        module.st.write('Successfully Removed Null Values')
        module.st.write('Removed % of rows', ((j-i)/i)*100)
        
with module.st.container():
    module.st.write("Negative Sales Present for rows",((df['Sales']<0).sum()))
    neg_option = module.st.radio("Remove Negative Sales",("Yes","No"))
    if neg_option=="Yes":
        df= df[df['Sales']>=0]
        module.st.write('Successfully Removed Negative Sales')

# st.session_state
with module.st.container():
    module.st.write("Maximum Sales",df['Sales'].max())
    outlier_option = module.st.radio("Remove Outliers in Sales",("Yes","No"))
    if outlier_option=="Yes":
        o1 = df.shape[0]
        df = module.outlier_rem(df,'Sales')
        o2 = df.shape[0]
        module.st.write('Successfully Removed Outliers')
        module.st.write('Removed % of rows', ((o1-o2)/o1)*100)

        
module.st.subheader("Data Preview")
module.st.subheader("------------------------------------------------------")
with module.st.container():
    if module.st.button("Preview Clean Data"):
        module.st.write(df.shape)
        module.st.dataframe(df.astype(str))


df.to_csv('clean_data.csv',index=False)

module.st.subheader('Data Visualization')
module.st.subheader("------------------------------------------------------")

if df.shape[1]<3:
    with module.st.container():
        num_feat = module.st.radio('Select Column for Histogram', df.columns)
        fig = module.px.histogram(df, x = num_feat)
        module.st.plotly_chart(fig, use_container_width=True)
else:
    col1,col2 = module.st.columns(2)
    with col1:
        num_feat = module.st.radio('Select Column for Histogram', df.columns)
        fig = module.px.histogram(df, x = num_feat)
        module.st.plotly_chart(fig, use_container_width=True)
    with col2:
        cat_feat = module.st.radio('Select Column for Category', df.columns)
        fig = module.px.histogram(df, x =cat_feat, color = 'Category' )
        module.st.plotly_chart(fig, use_container_width=True)


