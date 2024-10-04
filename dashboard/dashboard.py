import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

all_data = pd.read_csv("dashboard/all_data.csv")

#define dataframe
def selling_categories():
    selling_categories_df = all_data.groupby('product_category_name_english').agg({
        'order_item_id': 'sum',   
        'price': 'sum'            
    }).reset_index()
    return selling_categories_df

def sales_reviews():
    sales_reviews_df = all_data.groupby('product_category_name_english').agg({
    'order_item_id': 'sum',
    'price': 'sum',
    'review_score': 'mean'
    }).reset_index()
    return sales_reviews_df

#call function
selling_categories_df = selling_categories()
sales_reviews_df = sales_reviews()

#dashboard
st.set_page_config(layout="wide")
st.title('E-Commerce Data Analysis Dashboard')

with st.sidebar:
    st.sidebar.title("Dashboard Options")
    options = st.sidebar.selectbox("Choose Options", ("Overview", 
                                                      "Top and Worst Performing Products", 
                                                      "Sales and Review Scores Average"
                                                      ))
if options == "Overview":
    st.header("Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Selling by Revenues ")
        top_selling_df = selling_categories_df.sort_values(by='price', ascending=False).set_index('product_category_name_english').reset_index()
        top_selling_df.index += 1
        st.dataframe(top_selling_df)
    with col2:
        st.subheader("Worst Selling by Revenues ")
        worst_selling_df = selling_categories_df.sort_values(by='price', ascending=True).set_index('product_category_name_english').reset_index()
        worst_selling_df.index += 1
        st.dataframe(worst_selling_df)
    st.subheader("Worst Selling and Review Scores Average")
    sort_sales_reviews = sales_reviews_df.sort_values(by="order_item_id", ascending=True).set_index('product_category_name_english').reset_index()
    sort_sales_reviews.index += 1
    st.dataframe(sort_sales_reviews)

elif options == "Top and Worst Performing Products":
    st.header("Best & Worst Performing Product")
    #show chart by revenue
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

    colors = ["#72BCD4"] + ["#D3D3D3"] * 9

    sns.barplot(
        x="price", 
        y="product_category_name_english", 
        data=selling_categories_df.sort_values(by="price", ascending=False).head(10), 
        hue='product_category_name_english', 
        dodge=False, 
        palette=colors, 
        ax=ax[0]
        )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Top 10 Product Categories by Revenues", loc="center", fontsize=18)
    ax[0].tick_params(axis ='y', labelsize=15)
    for bar in ax[0].containers:
        ax[0].bar_label(bar, fmt='%.0f', label_type='edge', padding=3)

    sns.barplot(
        x="price", 
        y="product_category_name_english", 
        data=selling_categories_df.sort_values(by="price", ascending=True).head(10), 
        hue='product_category_name_english', 
        dodge=False, 
        palette=colors, 
        ax=ax[1]
        )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Bottom 10 Product Categories by Revenues", loc="center", fontsize=18)
    ax[1].tick_params(axis='y', labelsize=15)
    for bar in ax[1].containers:
        ax[1].bar_label(bar, fmt='%.0f', label_type='edge', padding=3)

    plt.suptitle("Best and Worst Selling Product Categories by Revenues\n", fontsize=20, y=1)
    st.pyplot(fig)

    #show chart by total sales
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

    colors = ["#72BCD4"] + ["#D3D3D3"] * 9

    sns.barplot(
        x="order_item_id", 
        y="product_category_name_english", 
        data=selling_categories_df.sort_values(by="order_item_id", ascending=False).head(10), 
        hue='product_category_name_english', 
        dodge=False, 
        palette=colors, 
        ax=ax[0]
        )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Top 10 Product Categories by Total Sales", loc="center", fontsize=18)
    ax[0].tick_params(axis ='y', labelsize=15)
    for bar in ax[0].containers:
        ax[0].bar_label(bar, fmt='%.0f', label_type='edge', padding=3)

    sns.barplot(
        x="order_item_id", 
        y="product_category_name_english", 
        data=selling_categories_df.sort_values(by="order_item_id", ascending=True).head(10), 
        hue='product_category_name_english', 
        dodge=False, 
        palette=colors, 
        ax=ax[1]
        )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Bottom 10 Product Categories by Total Sales", loc="center", fontsize=18)
    ax[1].tick_params(axis='y', labelsize=15)
    for bar in ax[1].containers:
        ax[1].bar_label(bar, fmt='%.0f', label_type='edge', padding=3)

    plt.suptitle("Best and Worst Selling Product Categories by Total Sales\n", fontsize=20, y=1)
    st.pyplot(fig)

elif options == "Sales and Review Scores Average":
    st.header("Sales and Review Scores Average")
    sales_threshold = sales_reviews_df['order_item_id'].quantile(0.25)
    sales_reviews_df['sales_category'] = sales_reviews_df['order_item_id'].apply(
        lambda x: 'Low Sales' if x < sales_threshold else 'High Sales'
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='order_item_id', 
                    y='review_score', 
                    hue='sales_category', 
                    data=sales_reviews_df, 
                    palette='coolwarm', 
                    alpha=0.7, 
                    ax=ax
                    )
    ax.set_title('Sales vs. Review Scores (Low vs High Sales)')
    ax.set_xlabel('Total Number of Items Sold')
    ax.set_ylabel('Average Review Score')
    ax.legend(title='Sales Category')
    st.pyplot(fig)

    st.caption('Bangkit Academy 2024 H2')
