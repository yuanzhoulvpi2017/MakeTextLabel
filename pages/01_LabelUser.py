from urllib import response
import streamlit as st
from datetime import datetime

import numpy as np
import pandas as pd
import random
import requests
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO

import yaml
from pathlib import Path
import socket
import requests
from typing import List

st.set_page_config(
    page_title="LabelUser",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("# 打标界面")


# import streamlit as st
# import streamlit_authenticator as stauth
# import yaml
# from pathlib import Path

# with open(Path(__file__).parent.parent.joinpath('users/labeluserconfig.yaml')) as file:
#     config = yaml.load(file, Loader=yaml.SafeLoader)

# # with open('../config.yaml') as file:
# #     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )


# name, authentication_status, username = authenticator.login('Login', 'main')

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

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
        获得项目列表
        """
        url = ''.join([self.url_base, "TaskList"])
        web = requests.get(url)
        return web.json()

    # @property
    def get_label(project_name: str, self) -> List[str]:
        """
        获得标签
        """
        headers = {
            'accept': 'application/json',
        }

        params = {
            'taskname': project_name,
            'key': 'love',
        }
        url = ''.join([self.url_base, 'SearchKey4task'])
        response = requests.get(url=url, params=params, headers=headers)
        res = response.json()
        return res

    # @property
    # def GetAllLabel(self) -> List[str]:
    #     """对外暴露的label"""
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

    def save_result(self, project_name: str, text: str, label: str):
        headers = {
            'accept': 'application/json',
        }

        params = {
            'taskname': project_name,
            'text': text,
            'label': label,
            'label_user': self.names
        }
        url = ''.join([self.url_base, 'SaveResult4Task'])
        response = requests.get(url=url, params=params, headers=headers)
        return response.json()


conback2 = ConnectBackLabel(names='hellouser1')

if st.session_state.get('conback2_value', None) is None:
    st.session_state.conback2 = conback2
    st.session_state.value_project_list = st.session_state.conback2.get_project_list

    # if st.session_state.get('04_modify_project_name', None) is None:
    #     project_name = 

    st.session_state.plt_value = st.session_state.conback2.get_text('proj2000')
    if st.session_state.plt_value.get('text_status', None) == 1:

        st.session_state.plt_value_text = st.session_state.plt_value.get(
            'need2labeltext', None)
        st.session_state.plt_vlaue_similist = st.session_state.plt_value.get(
            'similar_label', None)


def Update_Conback():
    st.session_state.plt_value = st.session_state.conback2.get_text('proj2000')
    if st.session_state.plt_value.get('text_status', None) == 1:

        st.session_state.plt_value_text = st.session_state.plt_value.get(
            'need2labeltext', None)
        st.session_state.plt_vlaue_similist = st.session_state.plt_value.get(
            'similar_label', None)


with st.form(key="login"):
    st.selectbox(label='项目名称', index=0,
                 options=st.session_state.value_project_list,
                 key='04_modify_project_name')

    # gl_project_name = st.session_state.get('04_modify_project_name', None)

    with st.expander(label="02_进入打标页面", expanded=True):
        st.text_area(label="show_text",
                     value=st.session_state.plt_value_text, key="text_02_needtext")

        tab1, tab2 = st.tabs(["算法推荐", "主动搜索"])
        with tab1:

            similar_text_list = st.session_state.plt_vlaue_similist
            st.radio(label="模型推荐", options=similar_text_list,
                     horizontal=True,
                     index=0, key="text_02_similar_list")

            def func_sub_modelsimi():
                Update_Conback()
                cur_need_text = st.session_state.get('text_02_needtext')
                cur_user_label = st.session_state.get('text_02_similar_list')

                print(f'text: {cur_need_text}, label: {cur_user_label}')

            st.form_submit_button(
                label="提交选择",
                on_click=func_sub_modelsimi
            )

        # with tab2:
        #     st.selectbox(label="搜索推荐", options=)
            # st.text_input(label="搜索推荐", value='',
            #               placeholder="输入搜索的关键词", key="text_02_search")
