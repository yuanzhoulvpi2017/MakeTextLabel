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

with st.form(key="login_01"):
    with st.expander(label="01_登录&选择项目", expanded=True):

        st.text_input(label="💁‍♂️ 打标人员用户姓名", value="",
                      key="login_01_username", placeholder="输入用户名称")
        st.text_input(label="💁‍♂️ 打标人员用户密码", value="",
                      key="login_01_password", placeholder="输入用户密码", type="password")

        def func_login_01():
            get_un = st.session_state.get('login_01_username', None)
            get_pw = st.session_state.get('login_01_password', None)

            if get_un is not None and get_pw is not None and \
                    len(get_un) != 0 and len(get_pw) != 0:
                if 'user_valid' not in st.session_state:
                    st.session_state['login_01_user_valid'] = 'ok'

        submit_button = st.form_submit_button(
            label='👨‍💻点击登录', on_click=func_login_01)

    if st.session_state.get('login_01_user_valid', None) != 'ok':
        st.warning("登录失败, 请联系管理员")
    else:
        with st.expander(label="02_进入打标页面", expanded=True):
            st.text_area(label="show_text",
                         value="您好，我是一个需要被打标签的文本", key="text_02_needtext")

            tab1, tab2 = st.tabs(["算法推荐", "主动搜索"])
            with tab1:

                similar_text_list = [f'label_{i}' for i in range(40)]
                st.radio(label="模型推荐", options=similar_text_list,
                         horizontal=True,
                         index=0, key="text_02_similar_list")

                def func_sub_modelsimi():
                    cur_need_text = st.session_state.get('text_02_needtext')
                    cur_user_label = st.session_state.get('text_02_similar_list')
                    
                    print(f'text: {cur_need_text}, label: {cur_user_label}')

                st.form_submit_button(
                    label="提交选择",
                    on_click=func_sub_modelsimi
                )

                

            with tab2:
                st.text_input(label="搜索推荐", value='',
                              placeholder="输入搜索的关键词", key="text_02_search")


    def func_leave_02():
        st.success("成功离开,幸苦啦")
    submit_button = st.form_submit_button(
        label='离开', on_click=func_leave_02)
