from modules import module

#Page symbol and Heading in browser
module.st.set_page_config(page_title = "Sales Prediction",page_icon=":loop:")
lottie_coding = module.load_lottie("https://assets2.lottiefiles.com/packages/lf20_7c1e8erd.json")

module.st.subheader("Data Input")
module.st.subheader("------------------------------------------------------")
#getting input from user
with module.st.container():
    c1,c2=module.st.columns(2)
    with c1:
        file = module.st.file_uploader("Upload Input Data", type = ["csv"])
        if file is not None:
            input_data = module.pd.read_csv(file)
        else:
            module.st.write("Please Upload the dataset before proceeding for forecasting")
    with c2:
        module.st_lottie(lottie_coding,key = "coding",height = 200,width = 400)

module.st.subheader("Choosing Data Analysis Columns")
module.st.subheader("------------------------------------------------------")
date_col = module.st.selectbox('Please Select Date Column',input_data.columns)

sales_col = module.st.selectbox('Please Select Sales Column',input_data.columns)

cat = module.st.radio("Please Select Overall Category",('National', 'Custom'))
if cat == 'Custom':
    cat_col = module.st.selectbox('Please Select Categorical Column',(input_data.columns))
else:
    cat_col="National"

if cat_col == "National":
    df = input_data[[date_col,sales_col]]
    df.columns = ['Date','Sales']
    df = module.stand_data(df)
    df = df.sort_values(by = 'Date',ascending = True)
else:
    df = input_data[[date_col,sales_col,cat_col]]
    df.columns = ['Date','Sales','Category']
    df = module.stand_data_cat(df)
    df = df.sort_values(by = ['Date','Category'],ascending=True) 

module.st.subheader("Input data time frame")
module.st.subheader("------------------------------------------------------")
#dt_range = module.st.slider("Select i/p Date range for Prediction",value=[df['Date'].min(),df['Date'].max()])
#df = df[(df['Date']>=dt_range[0])&(df['Date']<=dt_range[1])]


module.st.subheader("Preview Input Raw Data")
module.st.subheader("------------------------------------------------------")
with module.st.container():
    if df.shape[1]<3:
        if module.st.button("Input Data Metrics"):
            module.st.write("Total Data Rows = ",df.shape[0])
            module.st.write("Total Data Columns = ",df.shape[1])
            module.st.write("Total Sales = ",df['Sales'].sum())
            module.st.write("Average Sales = ",df['Sales'].mean()) 
    else:
        if module.st.button("Input Data Metrics"):
            module.st.write("Total Data Rows = ",df.shape[0])
            module.st.write("Total Data Columns = ",df.shape[1])
            module.st.write("Data Sub Categories are: ",df['Category'].unique())
            module.st.write("Total Sales = ",df['Sales'].sum())
            module.st.write("Average Sales = ",df['Sales'].mean())          
    if module.st.button("Preview Input Raw Data"):
        module.st.dataframe(df.astype(str))

df.to_csv('input.csv',index=False)
