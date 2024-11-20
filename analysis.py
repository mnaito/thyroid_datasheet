import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import sqlite3
import statistics
from datetime import datetime

def comparison():
    if 'df_total' not in st.session_state:
        st.session_state.df_analysis=pd.DataFrame()
        st.session_state.df_total=pd.DataFrame()
        st.session_state.clear_data=False
    file = st.date_input('**測定日**', value='today')
    total = st.number_input('**班数**', value=12)

    db_file='meas_database.db'
    colDupdate,colDdownload,colDummy=st.columns((1.3,1.1,5))
    with colDupdate:
        if st.button('**データ更新**'):
            st.session_state.df_analysis=pd.DataFrame()
            st.session_state.df_total=pd.DataFrame()
            conn = sqlite3.connect(db_file)
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

    with colDdownload:
        with open(db_file,'rb') as db:
            db_data=db.read()

        st.download_button(
            label="**全DB出力**",
            data=db_data,
            file_name=db_file
        )


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

    means=[]
    stdevs=[]
    for k in range(st.session_state.df_total.shape[0]):
        mean=statistics.mean(st.session_state.df_total.iloc[k])
        means.append(mean)
        stdev=statistics.stdev(st.session_state.df_total.iloc[k])
        stdevs.append(stdev)

    fig,ax=plt.subplots()
    ax.scatter(means,stdevs)
    ax.set_xlabel('平均値')
    ax.set_ylabel('標準偏差 (1$\\sigma$)')
    st.pyplot(fig)
    

