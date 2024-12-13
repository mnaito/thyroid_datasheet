import streamlit as st
import statistics
import pandas as pd
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import sqlite3
import os

def data_form():
    st.header('甲状腺簡易測定　データシート')

    flag=0
    Labels=['班番号', '測定日', '測定場所', '測定員/記録員', '機器番号', '校正日', '校正定数', 
            '時定数 (s)', '環境BG (usV/h)', '基準値 (uSv/h)', '開始時刻', '終了時刻', 
            '被検者ID', '被検者BG', '甲状腺位置測定値①', '甲状腺位置測定値②', '甲状腺位置測定値③', '中央値',
            '正味値', '補正値']

    if 'df' not in st.session_state:
        st.session_state.df=pd.DataFrame(columns=Labels)
        st.session_state.clear_data=False
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        st.session_state.Stime=now
        st.session_state.Etime=now

    Gnumber=0
    date_value='today'
    #meas_place=Labels[2]
    #player_members=Labels[3]
    #machine_label=Labels[4]
    calibrationD='today'
    calibrationV=1.00
    environment=0.05
    #now = datetime.now(ZoneInfo("Asia/Tokyo"))
    #Stime=now
    #Etime=now
    threshold_value=0.2
    IDs=['あ','い','う','え','お',
         'か','き','く','け','こ',
         'さ','し','す','せ','そ', 
         'A', 'B', 'C']


    colU1, colU2 = st.columns(2)

    with colU1:
        group_num=st.number_input(Labels[0], value=Gnumber)
        date = st.date_input(Labels[1], value=date_value)
        place = st.text_input(Labels[2], placeholder=Labels[2])
        players = st.text_input(Labels[3], placeholder=Labels[3])

        env_bg = st.number_input(Labels[8], value=environment)

    with colU2:
        machine_num = st.text_input(Labels[4], placeholder=Labels[4])
        calibration_date = st.date_input(Labels[5], value=calibrationD)
        calibration_value = st.number_input(Labels[6], value=calibrationV)
        time_const = st.selectbox(Labels[7], options=['3','10','30'], index=1)

        threshold = st.number_input(Labels[9], value=threshold_value)

    st.markdown('---')

    colB1, colB2 = st.columns(2)

    with colB1:
        if st.button('測定開始'):
            st.session_state.Stime= datetime.now(ZoneInfo("Asia/Tokyo")).time()
        start_time=st.time_input(Labels[10], value=st.session_state.Stime)
        obj_id = st.selectbox(Labels[12], options=IDs, placeholder=Labels[12], index=None, key="ID")
        meas1 = st.number_input(Labels[14])
        meas2 = st.number_input(Labels[15])
        meas3 = st.number_input(Labels[16])

    with colB2:
        if st.button('測定終了'):
            st.session_state.Etime= datetime.now(ZoneInfo("Asia/Tokyo")).time()
        end_time=st.time_input(Labels[11], value=st.session_state.Etime)

        obj_bg = st.number_input(Labels[13])
        median=statistics.median([meas1,meas2,meas3])
        st.write(Labels[17])
        st.text('%.3g'%median)
        med_sub=median-obj_bg
        st.write(Labels[18])
        st.text('%.3g'%med_sub)
        result =med_sub*calibration_value
        st.write(Labels[19])
        st.text('%.3g'%result)

    colA,colE,colC=st.columns((6,1.4,1.6))
    with colE:
        def input_and_next():
            if obj_id!=None:
                Data=[group_num,date,place,players,machine_num,calibration_date,calibration_value,time_const,
                    env_bg,threshold,start_time,end_time,obj_id,obj_bg,meas1,meas2,meas3,median,med_sub,result]
                df_add=pd.DataFrame([Data],columns=Labels)

                st.session_state.df=pd.concat([st.session_state.df, df_add], ignore_index=True)
                st.session_state["ID"]=None
            elif obj_id==None:
                @st.dialog('Error')
                def input_error():
                    st.error('被検者IDが選択されていません')
                input_error()

        input_button=st.button('入力/次へ', on_click=input_and_next)
            
    with colC:
        def save_and_finish():
            conn = sqlite3.connect('meas_database.db')
            c=conn.cursor()

            st.session_state.df.to_sql(str(date),conn,if_exists='append', index=False)

            conn.close()
            #st.session_state.df=pd.DataFrame(columns=Labels)
            @st.dialog('Success')
            def success_save():
                st.success('データ保存されました')
            success_save()

        submit_button=st.button('保存/終了', on_click=save_and_finish)

    with colA:
        if result > threshold:
            st.error(':red[補正値が基準値を超えています]')
#        if submit_button:
#            st.write('データ保存されました')

    st.markdown('---')

    editable_df=st.data_editor(st.session_state.df, num_rows='dynamic')
    st.session_state.df=editable_df

    return date