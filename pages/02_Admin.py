import streamlit as st
import numpy as np
import pandas as pd
st.set_page_config(
    page_title="Admin",
    page_icon="🤨",
    layout="wide",
    initial_sidebar_state="expanded",
)




st.markdown("# 管理界面")

st.markdown("## 管理人员")

with st.expander(label="1.创建打标人员账号", expanded=True):
    with st.form(key='01_new_people_form'):
        st.text_input(label="名称", value='', key='01_new_pn',
                      placeholder="新打标人员的登录名称")
        st.text_input(label="密码", value='', key='01_new_pp',
                      placeholder="新打标人员的登录密码")

        def create_label_user_callback():
            pass
        st.form_submit_button(
            label="确认创建", on_click=create_label_user_callback)


with st.expander(label="2.失效打标人员账号", expanded=True):
    with st.form(key='02_drop_people_form'):
        st.text_input(label="名称", value='', key='02_drop_pn',
                      placeholder='请输入要失效的打标人员的登录名称')
        st.text_input(label="密码", value='', key='02_drop_ps',
                      placeholder="请输入要失效的打标人员的登录密码")

        def drop_label_user_callback():
            pass
        st.form_submit_button(label="确认失效", on_click=drop_label_user_callback)


st.markdown("## 管理项目")

with st.expander(label="3.创建项目", expanded=True):
    with st.form(key='03_create_project'):
        st.text_input(label='项目名称', value='', key='03_create_project_name',
                      placeholder='可以试一试: 地球计划20221015。最好项目名称显眼')
        file_ul_03_cp_text = st.file_uploader(
            label="上传待打标语料", type="csv", key="f_ul_03_cp_text")
        file_ul_03_cp_label = st.file_uploader(
            label="上传待匹配标签", type="csv", key='f_ul_03_cp_label')

        def create_project_callback():
            ful03cptext = st.session_state.get('f_ul_03_cp_text', None)
            if ful03cptext is not None:
                ful03cptext = pd.read_csv(ful03cptext)
                print(ful03cptext.shape)
            # pass
        st.form_submit_button(label='确认创建项目', on_click=create_project_callback)


with st.expander(label="4.修改项目", expanded=True):
    with st.form(key='04_modify_project'):
        st.text_input(label='项目名称', value='',
                      key='04_modify_project_name', placeholder='输入已经需要修改的项目名称')
        tab1, tab2 = st.tabs(['添加标签', '删除标签'])
        with tab1:
            st.text_area(label='需要添加的标签', value='', height=200,
                         key='key04_add_label', placeholder="如果有多条标签，使用'#'隔开")
        # st.file_uploader(label="")
        with tab2:
            st.text_area(label="需要删除的标签", value='', height=200,
                         key='key04_delete_label', placeholder="如果有多条标签，使用'#'隔开")

        def modify_project_callback():
            pass
        st.form_submit_button(label='确认创建项目', on_click=modify_project_callback)
