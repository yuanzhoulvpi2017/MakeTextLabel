from asyncio import selector_events
from urllib import response
import streamlit as st
from datetime import datetime

import numpy as np
import pandas as pd
import random
import requests
import os
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from io import BytesIO

import yaml
from pathlib import Path
import socket
import requests
from typing import List

# import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path

# st.set_page_config(
#     page_title="LabelUser",
#     page_icon="๐",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )
with open(Path(__file__).parent.parent.joinpath('users/labeluserconfig.yaml')) as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.markdown("# ๆๆ ็้ข")


class ConnectBackLabel:
    def __init__(self, names: str) -> None:
        # self.project_name = project_name
        self.names = names
        # get port
        with open(Path(__file__).parent.parent.joinpath('admin.yaml'), 'r') as f:
            admin_detail = yaml.load(f, Loader=yaml.SafeLoader)
            app_port = int(admin_detail.get('port'))
            self.app_port = app_port

        # get address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip_host = s.getsockname()[0]
        # self.ip_host = '0.0.0.0'

        self.url_base = f"http://{self.ip_host}:{self.app_port}/"

        # self.ALL_Label = self.get_label_

    @property
    def get_project_list(self) -> List[str]:
        """
        ่ทๅพ้กน็ฎๅ่กจ
        """
        url = ''.join([self.url_base, "TaskList"])
        web = requests.get(url)
        return web.json()

    # @property
    def get_label(self, project_name: str) -> List[str]:
        """
        ่ทๅพๆ ็ญพ
        """
        headers = {
            'accept': 'application/json',
        }

        params = {
            'taskname': project_name,
        }
        url = ''.join([self.url_base, 'SearchKey4task'])
        response = requests.get(url=url, params=params, headers=headers)
        res = response.json()
        return res

    # @property
    # def GetAllLabel(self) -> List[str]:
    #     """ๅฏนๅคๆด้ฒ็label"""
    #     return self.ALL_Label

    def get_text(self, project_name: str):
        headers = {
            'accept': 'application/json',
        }

        params = {
            'taskname': project_name
        }
        url = ''.join([self.url_base, 'SendText4task'])
        response = requests.get(url=url, params=params, headers=headers)
        return response.json()

    def save_result(self, project_name: str, text: str, label: str, username: str):
        headers = {
            'accept': 'application/json',
        }

        params = {
            'taskname': project_name,
            'text': text,
            'label': label,
            'label_user': username
        }
        url = ''.join([self.url_base, 'SaveResult4Task'])
        response = requests.get(url=url, params=params, headers=headers)
        return response.json()


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    if st.session_state.get('global_username', None) is None:
        st.session_state.global_username = name
    if st.session_state.get('conback2_value', None) is None:
        st.session_state.conback2_value = ConnectBackLabel(names=st.session_state.get('global_username'))

    if st.session_state.get('text_button_01') is None:
        st.session_state.text_button_01 = ''
    if st.session_state.get('simi_button_02') is None:
        st.session_state.simi_button_02 = []

    if st.session_state.get('pair_text_label') is None:
        st.session_state.pair_text_label = {
            'need2labeltext': '', 'similar_label': []}

    if st.session_state.get('alllabel') is None:
        st.session_state.alllabel = []

    project_name_list = st.session_state.conback2_value.get_project_list

    if project_name_list is not None and len(project_name_list) == 0:
        st.success('่ๆน~ ๅฝๅๆฒกๆไปปไฝ้กน็ฎ')
    else:

        with st.form(key="dabiao"):

            st.markdown("## 1. ้กน็ฎ้จๅ")
            st.selectbox(label='้ๆฉ้กน็ฎ', options=project_name_list,
                         key='01select_project_value')


            def pjl():
                # ้ๅฅฝ้กน็ฎ๏ผ็นๅป็กฎๅฎ๏ผ็ถๅๆดๆฐๆๆฌๅๅฎน
                st.session_state.pair_text_label = st.session_state.conback2_value.get_text(
                    project_name=st.session_state.get('01select_project_value')
                )
                st.session_state.text_button_01 = st.session_state.pair_text_label.get(
                    'need2labeltext', '')
                st.session_state.simi_button_02 = st.session_state.pair_text_label.get(
                    'similar_label', [])
                print(st.session_state.get('global_username'))

                st.session_state.alllabel = st.session_state.conback2_value.get_label(
                    project_name=st.session_state.get('01select_project_value')
                )


            st.form_submit_button(label='็กฎๅฎ้กน็ฎ', on_click=pjl)

            st.markdown("## 2. ๆๆ ้จๅ")
            st.text_input(
                label='ๅพๆๆ ๆ ็ญพ', value=st.session_state.text_button_01, key='b1_value')

            tab1, tab2 = st.tabs(['ๆจกๅๆจ่ๅ่กจ', 'ๅจ้จๆ ็ญพ'])

            with tab1:
                st.radio(label='ๆจกๅๆจ่',
                         options=st.session_state.simi_button_02, key='b2_value')


                def submitResult_callback():
                    text = st.session_state.get('b1_value')
                    label = st.session_state.get('b2_value')
                    project_name = st.session_state.get('01select_project_value')
                    # names = 'yuanz'

                    st.session_state.conback2_value.save_result(
                        project_name=project_name,
                        text=text,
                        label=label,
                        username=st.session_state.get('global_username'))

                    # ๅๆฌกๆดๆฐ้่ฆๆๆ ็ๅๅฎน
                    st.session_state.pair_text_label = st.session_state.conback2_value.get_text(
                        project_name=st.session_state.get('01select_project_value')
                    )
                    st.session_state.text_button_01 = st.session_state.pair_text_label.get(
                        'need2labeltext', '')
                    st.session_state.simi_button_02 = st.session_state.pair_text_label.get(
                        'similar_label', [])


                st.form_submit_button(
                    label='ๆไบคๆๆ ็ปๆ', on_click=submitResult_callback)

            with tab2:
                st.selectbox(label='ๆๆๆ ็ญพ',
                             options=st.session_state.alllabel,
                             key='tuijianlabel')


                def submitResult_callback2():
                    select_input = st.session_state.get('tuijianlabel', None)
                    if select_input is not None:
                        text = st.session_state.get('b1_value')
                        label = select_input
                        project_name = st.session_state.get('01select_project_value')
                        # names = name
                        st.session_state.conback2_value.save_result(
                            project_name=project_name,
                            text=text,
                            label=label,
                            username=st.session_state.get('global_username'))

                        # ๅๆฌกๆดๆฐ้่ฆๆๆ ็ๅๅฎน
                        st.session_state.pair_text_label = st.session_state.conback2_value.get_text(
                            project_name=st.session_state.get('01select_project_value')
                        )
                        st.session_state.text_button_01 = st.session_state.pair_text_label.get(
                            'need2labeltext', '')
                        st.session_state.simi_button_02 = st.session_state.pair_text_label.get(
                            'similar_label', [])


                st.form_submit_button(label='ๆไบค่ชๅทฑๆ็ดข็ปๆ', on_click=submitResult_callback2)

    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


