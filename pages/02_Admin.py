from sqlite3 import connect
from typing_extensions import Self
import streamlit as st
import numpy as np
import pandas as pd
import yaml
from pathlib import Path
import socket
import requests
from typing import List


class ConnectBack:
    def __init__(self) -> None:

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
        # print(self.url_base)

    def create_label_user(self, username: str, password: str):
        """创建打标用户"""
        # print(self.url_base)
        url = ''.join([self.url_base, 'create_user'])
        params = {
            'user_name': username,
            'user_password': password
        }
        web = requests.get(url=url, params=params)
        return web.json()

    def delete_label_user(self, username: str):
        """
        删除打标用户
        """
        url = ''.join([self.url_base, 'delete_user'])
        params = {
            'user_name': username,
            # 'user_password': password
        }
        web = requests.get(url=url, params=params)
        return web.json()

    def delete_project(self, project_name: str):
        """
        删除项目
        """
        url = ''.join([self.url_base, 'delete_task'])
        params = {'taskname': project_name}
        web = requests.get(url=url, params=params)
        return web.json()

    def create_new_project_name(self, project_name: str):
        """
        创建新项目
        """
        url = ''.join([self.url_base, 'create_task'])
        params = {'taskname': project_name}
        web = requests.get(url=url, params=params)
        return web.json()

    def init_project(self, project_name: str, text: List[str], label: List[str]):
        """
        初始化项目
        """
        url = ''.join([self.url_base, 'Init2task'])
        params = {
            'taskname': project_name,

        }
        headers = {
            'accept': 'application/json',
            # Already added when you pass json= but not when you pass data=
            # 'Content-Type': 'application/json',
        }

        body = {
            'text': text,
            'label': label
        }
        web = requests.post(url=url, params=params, headers=headers, json=body)
        return web.json()

    @property
    def get_project_list(self) -> List[str]:
        """
        获得项目列表
        """
        url = ''.join([self.url_base, "TaskList"])
        web = requests.get(url)
        return web.json()

    def addlabel2project(self, project_name: str, label: List[str]):
        """
        向项目添加label
        """
        url = ''.join([self.url_base, "Addlabel2task"])
        params = {
            'taskname': project_name,

        }
        headers = {
            'accept': 'application/json',
        }

        body = {
            'label': label
        }
        web = requests.post(url=url, params=params, headers=headers, json=body)
        return web.json()

    def deletelabel2project(self, project_name: str, label: List[str]):
        """
        删除项目中的某些label
        """
        url = ''.join([self.url_base, "Deletelabel2task"])
        params = {
            'taskname': project_name,

        }
        headers = {
            'accept': 'application/json',
        }

        body = {
            'label': label
        }
        web = requests.post(url=url, params=params, headers=headers, json=body)
        return web.json()


conback = ConnectBack()

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
            # print(st.session_state.get('01_new_pn'),st.session_state.get('01_new_pp'))
            status = conback.create_label_user(
                username=st.session_state.get('01_new_pn'),
                password=st.session_state.get('01_new_pp'))

            # print(status)
            if status.get('status') == 1:
                st.success(status.get('info'))
            else:
                st.warning(status.get('info'))
        st.form_submit_button(
            label="确认创建", on_click=create_label_user_callback)


with st.expander(label="2.失效打标人员账号", expanded=True):
    with st.form(key='02_drop_people_form'):
        st.text_input(label="名称", value='', key='02_drop_pn',
                      placeholder='请输入要失效的打标人员的登录名称')
        # st.text_input(label="密码", value='', key='02_drop_ps',
        #               placeholder="请输入要失效的打标人员的登录密码")

        def drop_label_user_callback():
            status = conback.delete_label_user(
                username=st.session_state.get('02_drop_pn')
            )
            if status.get('status') == 1:
                st.success(status.get('info'))
            else:
                st.warning(status.get('info'))

            # pass
        st.form_submit_button(label="确认失效", on_click=drop_label_user_callback)


st.markdown("## 管理项目")

with st.expander(label="3.创建项目", expanded=True):
    with st.form(key='03_create_project'):
        st.text_input(label='项目名称', value='', key='03_create_project_name',
                      placeholder='可以试一试: earthplan20221015。最好项目名称显眼且英文名称加字符')
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

        def create_project_callback2():
            project_name: str = st.session_state.get(
                '03_create_project_name', None)
            if project_name is not None:
                project_name: str = project_name.replace(' ', '')

                if isinstance(project_name, str) and len(project_name) > 5:
                    cur_project_list = conback.get_project_list
                    if project_name in cur_project_list:
                        st.warning('项目名称已经存在不可以使用已存在的项目名称,请重试')
                    else:
                        try:

                            ful03cptext = st.session_state.get(
                                'f_ul_03_cp_text', None)
                            if ful03cptext is not None:
                                ful03cptext = pd.read_csv(ful03cptext)
                                ful03cptext = ful03cptext.iloc[:, 0].tolist()
                                ful03cptext = list(set(ful03cptext))

                            ful03cplabel = st.session_state.get(
                                'f_ul_03_cp_label', None)
                            if ful03cplabel is not None:
                                ful03cplabel = pd.read_csv(ful03cplabel)
                                ful03cplabel = ful03cplabel.iloc[:, 0].tolist()
                                ful03cplabel = list(set(ful03cplabel))

                            ful03cptext: List[str] = [
                                i.replace(' ', '') for i in ful03cptext if i.replace(' ', '') != 0]
                            ful03cplabel: List[str] = [
                                i.replace(' ', '') for i in ful03cplabel if i.replace(' ', '') != 0]

                            if len(ful03cplabel) != 0 and len(ful03cptext) != 0:

                                conback.create_new_project_name(
                                    project_name=project_name)
                                conback.init_project(
                                    project_name=project_name, text=ful03cptext, label=ful03cplabel)
                                st.success(
                                    f"创建项目成功, 项目名称: {project_name}, 待标记数量: {len(ful03cptext)}, 总标签数量: {len(ful03cplabel)}")

                        except Exception as e:
                            st.error(e)
                else:
                    st.warning("项目名称长度必须大于等于5,请重试")
            else:
                st.warning('务必填写一个项目名称')
        st.form_submit_button(label='确认创建项目', on_click=create_project_callback)


with st.expander(label="4.修改项目", expanded=True):
    with st.form(key='04_modify_project'):
        st.selectbox(label='项目名称', index=0,
                     options=conback.get_project_list, key='04_modify_project_name')
        # st.text_input(label='项目名称', value='',
        #               key='04_modify_project_name', placeholder='输入已经需要修改的项目名称')
        tab1, tab2 = st.tabs(['添加标签', '删除标签'])
        with tab1:
            st.text_area(label='需要添加的标签', value='', height=200,
                         key='key04_add_label', placeholder="如果有多条标签，使用'#'隔开")

            def modify_project_callback1():
                project_name = st.session_state.get(
                    '04_modify_project_name', None)
                if project_name is not None:
                    try:
                        label = st.session_state.get('key04_add_label', None)
                        if label is not None and isinstance(label, str) and len(label) > 0:
                            label: List[str] = label.split('#')
                            label = list(
                                set([i for i in label if len(i) != 0]))
                            conback.addlabel2project(project_name=project_name,
                                                     label=label)
                        else:
                            st.warning('添加标签失败')
                    except Exception as e:
                        st.error(e)

                else:
                    st.warning('务必填写一个项目名称')

                # pass

            st.form_submit_button(
                label='确认添加', on_click=modify_project_callback1)

        with tab2:
            st.text_area(label="需要删除的标签", value='', height=200,
                         key='key04_delete_label', placeholder="如果有多条标签，使用'#'隔开")

            def modify_project_callback2():
                project_name = st.session_state.get(
                    '04_modify_project_name', None)
                if project_name is not None:
                    try:
                        label = st.session_state.get(
                            'key04_delete_label', None)
                        if label is not None and isinstance(label, str) and len(label) > 0:
                            label: List[str] = label.split('#')
                            label = list(
                                set([i for i in label if len(i) != 0]))
                            conback.deletelabel2project(project_name=project_name,
                                                        label=label)
                        else:
                            st.warning('删除标签失败')
                    except Exception as e:
                        st.error(e)

                else:
                    st.warning('务必填写一个项目名称')
            st.form_submit_button(
                label='确认删除', on_click=modify_project_callback2)
