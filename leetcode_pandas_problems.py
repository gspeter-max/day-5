'''1484. Group Sold Products By The Date
'''
https://leetcode.com/problems/group-sold-products-by-the-date/

import pandas as pd

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
 
    temp_df = activities.groupby('sell_date')['product'].nunique().reset_index()
    temp_df.columns = ['sell_date', 'num_sold']

    temp_dic = []
    for sell_date, products in activities.groupby('sell_date')['product'].unique().items():
        temp_dic.append((sell_date, ",".join(sorted(products))))  
        
    temp_dic_df = pd.DataFrame(temp_dic, columns=['sell_date', 'products'])

    merge_df = pd.merge(temp_df, temp_dic_df, on='sell_date', how='inner')

    return merge_df[['sell_date', 'num_sold', 'products']]


'''407. Top Travellers'''
https://leetcode.com/problems/top-travellers/


import pandas as pd
def top_travellers(users: pd.DataFrame, rides: pd.DataFrame) -> pd.DataFrame:
    df_temp = rides.groupby('user_id')['distance'].sum().reset_index() 
    
    df_temp.columns = ['id','travelled_distance']

    merge = pd.merge(
        users, df_temp , on = 'id', how ='left'
    )
    
    merge = merge.sort_values(
        by = ['travelled_distance','name'],
        ascending = [False,True]
    ).fillna(0)
    
    return merge[['name','travelled_distance']]



'''1393. Capital Gain/Loss'''
https://leetcode.com/problems/capital-gainloss/

import pandas as pd

def capital_gainloss(stocks: pd.DataFrame) -> pd.DataFrame:
    df_buy = stocks[stocks['operation'] == 'Buy']
    df_buy = df_buy.groupby('stock_name')['price'].sum().reset_index() 
    df_buy.columns = ['stock_name','buy_price']

    df_sell = stocks[stocks['operation'] == 'Sell']
    df_sell = df_sell.groupby('stock_name')['price'].sum().reset_index() 
    df_sell.columns = ['stock_name','sell_price']

    merge = pd.merge( df_sell , df_buy , on = 'stock_name', how = 'inner')
    merge['capital_gain_loss'] = merge['sell_price'] - merge['buy_price']
    return merge[['stock_name','capital_gain_loss']]
