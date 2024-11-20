import streamlit as st
import statistics
import pandas as pd
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
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
    meas_place='meas_place'
    player_members='/'
    machine_label='machine_number'
    calibrationD='today'
    calibrationV=1.00
    environment=0.05
    #now = datetime.now(ZoneInfo("Asia/Tokyo"))
    #Stime=now
    #Etime=now
    threshold_value=0.2
    ID='被検者ID'


    colU1, colU2 = st.columns(2)

    with colU1:
        group_num=st.number_input(Labels[0], value=Gnumber)
        date = st.date_input(Labels[1], value=date_value)
        place = st.text_input(Labels[2], value=meas_place)
        players = st.text_input(Labels[3], value=player_members)

        env_bg = st.number_input(Labels[8], value=environment)

    with colU2:
        machine_num = st.text_input(Labels[4], value=machine_label)
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
        obj_id = st.text_input(Labels[12], value=ID)
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
        st.text(median)
        med_sub=median-obj_bg
        st.write(Labels[18])
        st.text(med_sub)
        result =med_sub*calibration_value
        st.write(Labels[19])
        st.text(result)

    colD,colE,colC=st.columns((6,1.4,1.6))
    with colD:
        if result > threshold:
            st.error(':red[補正値が基準値を超えています]')

    with colE:
        if st.button('保存/次へ'):
            Data=[group_num,date,place,players,machine_num,calibration_date,calibration_value,time_const,
                env_bg,threshold,start_time,end_time,obj_id,obj_bg,meas1,meas2,meas3,median,med_sub,result]
            df_add=pd.DataFrame([Data],columns=Labels)

            st.session_state.df=pd.concat([st.session_state.df, df_add], ignore_index=True)
            flag=1

            output_file=str(date)+'.csv'
            if os.path.exists(output_file):
                st.session_state.df.to_csv(output_file, index=False, mode='a', header=False)
            else:
                st.session_state.df.to_csv(output_file, index=False, mode='a', header=True)
            #st.session_state.df=pd.DataFrame(columns=Labels)

    with colC:
        if st.button('クリア/終了'):
            st.session_state.df=pd.DataFrame(columns=Labels)

    st.markdown('---')

    editable_df=st.data_editor(st.session_state.df, num_rows='dynamic')
    st.session_state.df=editable_df

    return date