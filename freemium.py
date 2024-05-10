import streamlit as st
import pandas as pd
import time
import itertools

st.set_page_config(
        page_title="StockPulse",
        page_icon="coin",
        layout="wide"
    )

df=pd.read_csv('portfolioSymbol.csv')
st.write(df)

'''def modified_string(original_string):
    index = original_string.find('\\')
    result_string = original_string[index + 1:]
    return result_string

def add_industry(df,time):
    for i in df.columns:
        file=i+"_output_"+time+".csv"
        data=pd.read_csv(file)
        data["Industry"]=i
        data.to_csv(file,index=False)

def csv_to_dict(df,time):
    data_dict = {}
    for index, row in df.iterrows():
        industry = row['Industry']
        name = row['Name']
        price = float(row['Price'])
        profit = float(row[time])
        if industry in data_dict:
            data_dict[industry].append([name,price,profit,1])
        else:
            data_dict[industry] = [[name,price,profit,1]]
    return data_dict

def create_data(df,time):
    list=[]
    for i in df.columns:
        folder_name=i
        s=i+"_output_"+time+".csv"
        list.append(s)

    dfs=[]
    for file in list:
        di=pd.read_csv(file)
        dfs.append(di)
    combined_df=pd.concat(dfs, ignore_index=True)
    return combined_df

def find_max_profit(stocks_data, budget):
    max_profit = 0
    selected_stocks = None

    # Generate combinations of stocks, one from each industry
    combinations = itertools.product(*stocks_data.values())

    for combination in combinations:
        total_price = sum(stock[1] for stock in combination)
        if total_price <= budget:
            total_profit = sum(stock[2] for stock in combination)
            if total_profit > max_profit:
                max_profit = total_profit
                selected_stocks = combination
    return max_profit, selected_stocks

def quantity_check(amount,invsetment,y):
    remaining=amount-invsetment
    while (remaining >= invsetment):
        for i in y:
            i[3]=i[3]+1
            remaining=remaining-i[1]
    least_cost=999999
    for i in y:
        least_cost=min(least_cost,i[1])
    while(remaining>=least_cost):
        for i in y:
            if remaining>=i[1]:
                i[3] = i[3] + 1
                remaining = remaining - i[1]
    total = amount - remaining
    return total, y

def working(df,a,t):
    amount=a
    time=t
    add_industry(df,time)
    df=create_data(df,time)
    df=df.sort_values(by=time,ascending=False,ignore_index=True)
    dict=csv_to_dict(df,time)
    x,y=find_max_profit(dict,amount)
    print(+x/8)
    total_price = sum(stock[1] for stock in y)
    total_price,y=quantity_check(amount,total_price,y)
    return total_price,y

def update_metric(m1,m2,m3,pn,pc,r):
    m1.metric("Number", pn)
    m2.metric("Coins", pc)
    m3.metric("Coins", r)

portfolio_number=0
pulsecoin=0.00
remaining=10000.00
col1,col2,col3,col4,col5,col6,col7=st.columns([7,1,1,1,1,1,3])
with col1:
    st.markdown('<h1 style="color: #00ffff;">😎 Freemium</h1>', unsafe_allow_html=True)
with col7:
    st.markdown('<style>img {border-radius: 200px;}</style>', unsafe_allow_html=True)
    st.image("dp.jpg", width=50)
st.markdown("""---""")

st.markdown('<h3> On this page, you can create a sample portfolio using our virtual currency to see how it functions.</h3>',unsafe_allow_html=True)

col1,col2,col3=st.columns(3)
with col1:
    st.info("📊 Portfolios")
    metric1=st.metric(label="Number",value=portfolio_number)
with col2:
    st.success("💵 Total Investment")
    metric2=st.metric(label="Coins",value=pulsecoin)
with col3:
    st.warning("🪙 Amount Remaining")
    metric3=st.metric(label="Coins",value=remaining)

st.markdown('''---''')
with st.form(key='form1'):
    col1, col2 = st.columns(2)
    with col1:
        amount=st.number_input("Enter the Amount You want to Invest (Min 500 Coins) :",min_value=500.00,key=int,)
        if amount<500:
            st.error("Minimum 500 Coins should be invested")
    with col2:
        value=st.select_slider("How Much Risk You Want :",options=["Low","Low","Low","Low","High","High","High","High"])
    col1,col2=st.columns(2)
    with col1:
        selected_value = st.selectbox("Select how You want it to buy",["Market Price","Limit Price","SIP"])
    with col2:
        unique_id=st.text_input("Enter your PAN number to confirm: ")
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        tc=st.checkbox("I agree to the terms and conditions")
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([2.5,2,2])
    with col2:
        submit_form=st.form_submit_button(label="Create Portfolio")
    flag=False
    if submit_form:
        if tc and amount and unique_id and selected_value:
            col1, col2, col3 = st.columns([1.5, 2, 2])
            with col2:
                flag=True
                st.success("Process Initiated")
        elif amount and unique_id and selected_value:
            col1, col2, col3 = st.columns([1.5, 2, 2])
            with col2:
                st.warning("Please check Terms and Conditions")
        else:
            col1, col2, col3 = st.columns([1.3, 2, 2])
            with col2:
                st.error("Please Fill the Form Properly")

if submit_form and flag:
    with st.spinner('Wait For It...'):
        time.sleep(5)
    data1 = pd.read_csv('company_s.csv')
    df = pd.read_csv('portfolioSymbol.csv')
    if value=="Low":
        ti="Year"
    elif value=="High":
        ti="Day"
    total, y = working(df,amount,ti)
    portfolio_number=portfolio_number+1
    pulsecoin="{:.2f}".format(total)
    remaining="{:.2f}".format(remaining-total)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.info("Company Name: ")
    with col2:
        st.warning("Quantity")
    with col3:
        st.success("Current Price")
    with col4:
        st.error("Purchase Price")
    for i in y:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        s = i[0]
        result = data1[data1['Symbol'] == s]
        if not result.empty:
            price = result['Price'].iloc[0]
            name = result['Company'].iloc[0]
        with col1:
            st.write(name)
        with col2:
            st.write(f"<span style='color:yellow'>{i[3]}</span>", unsafe_allow_html=True)
        with col3:
            if price < round(i[1]):
                st.write(f"<span style='color:red'>{price}</span>", unsafe_allow_html=True)
            else:
                st.write(f"<span style='color:green'>{price}</span>", unsafe_allow_html=True)
        with col4:
            if price < round(i[1]):
                st.write(f"<span style='color:orange'>{round(i[1], 2)}</span>", unsafe_allow_html=True)
            else:
                st.write(f"<span style='color:red'>{round(i[1], 2)}</span>", unsafe_allow_html=True)


update_metric(metric1, metric2, metric3,portfolio_number,pulsecoin,remaining)'''
