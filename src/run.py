import sys
import json
import os
import numpy as np
from utils import *

def main(argv):
    main_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(main_path, 'app_config.json')
    with open(config_file, "r") as f:
        conf = json.load(f)
        conn_string =  conf['conn_string']
        columns = ['Item', 'Color', 'Size', 'Qty', 'STL_QTY', 'STL_L_QTY', 'OB_QTY', 'OB_L_QTY', 'Total_Avail']
        df_items = get_items_from_db(conn_string)
        df_items['Total_Avail'] = df_items['STL_QTY'] + df_items['STL_L_QTY'] + df_items['OB_QTY'] + df_items['OB_L_QTY']
        df_items.columns = columns
        df_zeroes = df_items[(df_items['STL_QTY'] <= 0.0) & (df_items['STL_L_QTY'] <= 0.0) & (df_items['OB_QTY'] <= 0.0) & (df_items['OB_L_QTY'] <= 0.0)]
        df_zeroes.to_excel('Items Zero qty.xlsx', index=False)
        
        df_stl_l = get_transfers_for_wh2(df_items,'STL_L_QTY', 'STL-L', 'STL')
        df_ob = get_transfers_for_wh(df_items,'OB_QTY', 'OB', 'STL-L')
        df_ob_l = get_transfers_for_wh(df_items,'OB_L_QTY', 'OB-L', 'STL-L')
        df_transfers = pd.concat([df_stl_l, df_ob, df_ob_l])
        df_transfers.to_csv('Transfers.csv', index=False)

        df_need = df_items[df_items['Qty'] > df_items['Total_Avail']]
        df_need_2 = df_need.merge(df_zeroes.drop_duplicates(), on=columns, how='left')
        df_need_2.columns = ['Item', 'Color', 'Size', 'Qty', 'STL_QTY', 'STL_L_QTY', 'OB_QTY', 'OB_L_QTY', 'Total_Avail']
        df_need_2['QtyDiff'] = df_need_2['Qty'] - df_need_2['Total_Avail']
        df_need_2 = df_need_2[['Item', 'Color', 'Size', 'QtyDiff']]
        df_need_2.to_excel('Items Need TJ.xlsx', index=False)

def get_transfers_for_wh(df_items, column, wh_name, to_wh_name):
    df = df_items[df_items[column] > 0].copy()
    columns = ['Item', 'Color', 'Size', 'Qty', 'STL_QTY', 'STL_L_QTY', 'OB_QTY', 'OB_L_QTY', 'Total_Avail']
    columns_final = ['FromSite', 'FromWh', 'Item', 'Color', 'Size', 'Qty', 'ToSite', 'ToWh']
    df.columns = columns
    df['FromSite'] = 'KT'
    df['FromWh'] = wh_name
    df['ToSite'] = 'KT'
    df['ToWh'] = to_wh_name
    df['Qty'] = df[column]
    df = df[columns_final]
    return df

def get_transfers_for_wh2(df_items, column, wh_name, to_wh_name):
    df = df_items.copy()
    columns = ['Item', 'Color', 'Size', 'Qty', 'STL_QTY', 'STL_L_QTY', 'OB_QTY', 'OB_L_QTY', 'Total_Avail']
    columns_final = ['FromSite', 'FromWh', 'Item', 'Color', 'Size', 'Qty', 'ToSite', 'ToWh']
    df.columns = columns
    df['Needed'] = df['Qty'] - df['STL_QTY']
    df = df[df['Needed'] > 0]
    df['FromSite'] = 'KT'
    df['FromWh'] = wh_name
    df['ToSite'] = 'KT'
    df['ToWh'] = to_wh_name
    df['Qty'] = np.where(df['Needed'] < df['STL_QTY'], df['Needed'], df['STL_QTY'])
    df = df[columns_final]
    return df

if __name__ == '__main__':
    main(sys.argv[1:])