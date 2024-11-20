import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import sqlite3
from datetime import datetime

def comparison():
    if 'df_total' not in st.session_state:
        st.session_state.df_analysis=pd.DataFrame()
        st.session_state.df_total=pd.DataFrame()
        st.session_state.clear_data=False
    file = st.date_input('**測定日**', value='today')
    total = st.number_input('**班数**', value=12)
    if st.button('**データ更新**'):
        st.session_state.df_analysis=pd.DataFrame()
        st.session_state.df_total=pd.DataFrame()
        conn = sqlite3.connect('meas_database.db')
        c=conn.cursor()
        
        st.session_state.df_analysis=pd.read_sql_query('SELECT * FROM `%s`'% str(file), conn)

        conn.close()

        df_a=pd.DataFrame()
        df_i=pd.DataFrame()
        for i in range(total):
            obj_id_add=[]
            results_add=[]
            dic={}
            dic_sorted=[]
            df_a=st.session_state.df_analysis[st.session_state.df_analysis['班番号']==i]
            obj_id=df_a['被検者ID'].to_list()
            results=df_a['正味値'].to_list()
            if obj_id == []:
                continue
            dic.update(zip(obj_id,results))
            dic_sorted = sorted(dic.items(), key=lambda x:x[0])
            for dataset in dic_sorted:
                obj_id_add.append(dataset[0])
                if i==0:
                    st.session_state.df_total=pd.DataFrame(index=obj_id_add)
                results_add.append(dataset[1])
            data=pd.Series(results_add,index=obj_id_add, name=i)
            st.session_state.df_total=pd.concat([st.session_state.df_total,data], axis=1)


    st.subheader('**Data**')
    st.dataframe(st.session_state.df_analysis,hide_index=True)
    csv_data=st.session_state.df_analysis.to_csv(index=True, mode='w', header=True).encode('utf-8_sig')
    st.download_button(
        label='**csv保存**',
        data=csv_data,
        file_name=str(file)+'.csv', 
    )

    st.subheader('**Summary**')
    st.dataframe(st.session_state.df_total)
    csv_summary=st.session_state.df_total.to_csv(index=True, mode='w', header=True).encode('utf-8_sig')
    st.download_button(
        label='**csv保存**',
        data=csv_summary,
        file_name=str(file)+'_summary.csv', 
    )

    st.pyplot(st.session_state.df_total.plot.bar(ylabel='正味値', xlabel='被検者ID', rot=0).figure)