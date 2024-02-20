
import pandas as pd
import plotly.express as px  # 画图
import streamlit as st  # 可视化


### 将csv文件导入，进行数据分析，并使用streamlit可视化，并在streamlit云分享


st.set_page_config(page_title="淘宝销量数据", page_icon=":flag_china:", layout="wide")  # 设置streamlit基础页面信息，只能放在开头，且只能执行一次

table_csv = "mao_zi.csv" #在此处修改要分析的文件

df = pd.read_csv(table_csv, encoding='gbk')
data_table = open("mao_zi.csv","r")



df.info() # 查看表总体信息


# 数据清洗
df['number_purchaser'] = df['number_purchaser'].str.replace('+人收货', '')  # 去除多余字符
df['number_purchaser'] = df['number_purchaser'].str.replace('万', '0000') 
df['number_purchaser'] = df['number_purchaser'].apply(int) # 转换为数字类型

df['price_product'] = df['price_product'].str.replace('.00','')    # 去除多余字符      
df['price_product'] = df['price_product'].str.replace('元', '')
df['price_product'] = df['price_product'].astype('float')  # 转换为数字类型
df.info() # 查看表总体信息


# 可视化页面，左边栏设置
st.sidebar.header("请在这里筛选:") # 主标题

city = st.sidebar.multiselect(     # 侧边栏
    "选择城市:",
    options=df["address"].unique(), # 选项
    default=df["address"].unique()  # 默认选项
)  # 相当于前端呈现

df_selection = df.query('address == @city')  # 对原数据集进行处理，化为可交互数据



# 可视化页面，主页面设置
st.title("🆎 销售数据大屏") # 主标题
st.markdown("##") # markdowm文本格式，##表示二级标题

number_max = max(df['number_purchaser'])  # 最大销量，这里由于是总的数据呈现，所以不用df_selection，而用df
nunber_mean = int(df['number_purchaser'].mean())  # 平均销量
price_mean = round(df['price_product'].mean(),1)  # 平均价格


# 3列布局
left_column, middle_column, right_column = st.columns(3)

# 添加相关信息
with left_column:
    st.subheader("最大销量:")
    st.subheader(f"{number_max} 件")
with middle_column:
    st.subheader("平均销量:")
    st.subheader(f"{nunber_mean} 件")
with right_column:
    st.subheader("平均价格:")
    st.subheader(f"RMB {price_mean}")

# 分隔符
st.markdown("""---""")




# 各类商品销售情况(柱状图)
sales_by_product = df_selection.groupby(by=["address"]).sum()[["number_purchaser"]].sort_values(by="number_purchaser") # 对可交互数据集按地区销量进行计数，排序
# sales_by_product_line = df_selection.groupby(by=["address"]).sum().sort_values(by="number_purchaser") # 是否指定number_purchaser均可

fig_product_sales = px.bar(
    sales_by_product ,   # 这里是处理过的可交互数据集
    y = 'number_purchaser',  # y坐标，为可交互数据集的值
    x = sales_by_product.index, # x坐标，为数据集的索引
    title="<b>每个城市销售数量</b>", # 表标题
    text = 'number_purchaser',  # 柱子内标注，最好是y轴值
    color_discrete_sequence=["#0083B8"] * len(sales_by_product),
    template="plotly_white",
)
# 添加坐标注释
fig_product_sales.update_layout(xaxis_title='省份',
                 yaxis_title='销量')

#柱形图文字格式
fig_product_sales.update_traces(
                 textposition='outside',
                 texttemplate='%{text:,.2s}')

st.plotly_chart(fig_product_sales)  # 该代码仅用于plotly画图方法


# fig_product_sales.show() # 用于检验图表
