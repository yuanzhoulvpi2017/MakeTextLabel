from dataclasses import dataclass, field
from enum import Enum
from typing import List

import pandas as pd
import os
from datetime import datetime

from pathlib import Path
import streamlit_authenticator as stauth
import yaml


class UserStatus(Enum):
    ACTIVATE = 1
    LEAVE = 2
    NOEXIST = 3

    def value2enum(value):
        if value == 1:
            return UserStatus.ACTIVATE
        else:
            return UserStatus.LEAVE


class ActiveStatus(Enum):
    SUCCESS = 1
    ERROR = 2


@dataclass
class ActiveOutput:
    status: ActiveStatus = field(default=ActiveStatus.SUCCESS)
    info: str = field(default="操作成功")


@dataclass
class DetectUserStatusOutput(ActiveOutput):
    userstatus: UserStatus = field(default=UserStatus.NOEXIST)


@dataclass
class UserInfo:
    name: str
    password: str
    status: UserStatus
    create_time: datetime
    leave_time: datetime

    def to_dataframe(self) -> pd.DataFrame:
        res = pd.DataFrame({'user_name': [self.name],
                            'password': [self.password],
                            'status': [self.status.value],
                            'create_time': [self.create_time],
                            'leave_time': [self.leave_time]})
        return res


class ManageUser:
    def __init__(self) -> None:
        user_path = Path(__file__).parent.parent.joinpath('users')
        self.user_df_file = user_path.joinpath("users.csv")
        os.makedirs(name=user_path, exist_ok=True)
        self.adminyaml()


        if self.user_df_file.exists():
            user_df = pd.read_csv(self.user_df_file)
            self.all_user_list: List[UserInfo] = []
            if user_df.shape[0] > 0:

                user_df = user_df.pipe(
                    lambda x: x.assign(**{
                        'create_time': pd.to_datetime(x['create_time']),
                        'leave_time': pd.to_datetime(x['leave_time'])})
                )
                for index, row in user_df.iterrows():
                    temp_user = UserInfo(name=row.user_name,
                                         password=row.password,
                                         status=UserStatus.value2enum(
                                             row.status),
                                         create_time=row.create_time,
                                         leave_time=row.leave_time
                                         )
                    self.all_user_list.append(temp_user)
            else:
                self.all_user_list: List[UserInfo] = []
                # pass
        else:
            self.all_user_list: List[UserInfo] = []

    def create_user(self, user_name: str, user_password: str):
        """
        创建一个用户:
        1. 需要传递 user_name
        2. 需要传递 user_password
        对user_name, user_password做校准
        1. user_name must be a str and length(user_name) >= 5
        2. user_password must be a str and length(user_password) >= 10 and user_name != user_password
        """

        if isinstance(user_name, str) and len(user_name) >= 5:
            if isinstance(user_password, str) and len(user_password) >= 10 and user_name != user_password:
                pass

            else:
                return ActiveOutput(status=ActiveStatus.ERROR, info="user_password must be a str and length(user_password) >= 10 and user_name != user_password")
        else:
            return ActiveOutput(status=ActiveStatus.ERROR, info="user_name must be a str and length(user_name) >= 5")

        if len(self.all_user_list) == 0:
            pass
        else:
            for temp_select in self.all_user_list:
                if temp_select.name == user_name:
                    return ActiveOutput(status=ActiveStatus.ERROR, info=f"the user_name: {user_name} has been used. Please use a new name")

        c_user = UserInfo(name=user_name, password=user_password,
                          status=UserStatus.ACTIVATE,
                          create_time=datetime.now(),
                          leave_time=datetime.now())

        self.all_user_list.append(c_user)
        self.reflashyamlfile

        self.data_2_file

        return ActiveOutput()

    def delete_user(self, user_name: str):
        """
        删除一个用户:修改这个用户的状态
        """

        if len(self.all_user_list) > 0:

            for temp_user in self.all_user_list:
                if temp_user.name == user_name:
                    if temp_user.status == UserStatus.ACTIVATE:
                        temp_user.status = UserStatus.LEAVE
                        temp_user.leave_time = datetime.now()
                        self.data_2_file
                        self.reflashyamlfile
                        return ActiveOutput()
                    else:
                        self.data_2_file
                        return ActiveOutput(status=ActiveStatus.ERROR, info="用户已经离开, 不可以再次让其离开")
            else:
                self.data_2_file
                return ActiveOutput(status=ActiveStatus.ERROR, info="未找到该用户")

        else:
            return ActiveOutput(status=ActiveStatus.ERROR, info="当前用户列表为空")

    def detect_user_status(self, user_name):
        """
        检测用户的状态
        """

        if len(self.all_user_list) > 0:

            for temp_u in self.all_user_list:
                if temp_u.name == user_name:
                    if temp_u.status == UserStatus.ACTIVATE:
                        return DetectUserStatusOutput(userstatus=UserStatus.ACTIVATE)
                    else:
                        return DetectUserStatusOutput(userstatus=UserStatus.LEAVE)
            else:
                return DetectUserStatusOutput(status=ActiveStatus.ERROR,info='不存在该用户')

        else:
            return DetectUserStatusOutput(status=ActiveStatus.ERROR, info='不存在该用户')

    @property
    def data_2_file(self) -> None:
        user_df_save = pd.concat(
            [i.to_dataframe() for i in self.all_user_list]).reset_index(drop=True)
        user_df_save.to_csv(self.user_df_file, index=False)

        self.reflashyamlfile

    @property
    def reflashyamlfile(self) -> None:

        with open(Path(__file__).parent.parent.joinpath('admin.yaml'), 'r') as f:
            admin_detail = yaml.load(f, Loader=yaml.SafeLoader)

        admin_name = admin_detail.get('admin').get('name')
        admin_password = admin_detail.get('admin').get('password')
        active_user_list = [
            i for i in self.all_user_list if i.status == UserStatus.ACTIVATE]

        if len(active_user_list) != 0:
            usernamelist = [admin_name] + [i.name for i in active_user_list]
            password = [admin_password] + \
                [i.password for i in active_user_list]

            user2yaml(userlist=usernamelist, password=password)
        else:
            usernamelist = [admin_name]
            password = [admin_password]
            user2yaml(userlist=usernamelist, password=password)

    def adminyaml(self):

        with open(Path(__file__).parent.parent.joinpath('admin.yaml'), 'r') as f:
            admin_detail = yaml.load(f, Loader=yaml.SafeLoader)

        admin_name = admin_detail.get('admin').get('name')
        admin_password = admin_detail.get('admin').get('password')

        userlist = [admin_name]
        hashed_passwords = stauth.Hasher(admin_password).generate()

        user_config = {
            'credentials': {
                'usernames': {

                    k: {
                        'email': f'{k}@xiaoshiwole.com',
                        'name': k,
                        'password': p
                    } for k, p in zip(userlist, hashed_passwords)
                }
            },
            'cookie': {
                'expiry_days': 9999,
                'key': 'some_signature_key',
                'name': 'some_cookie_name'
            },
            'preauthorized': {
                'emails': 'yuanzhoulvpi@outlook.com'
            }

        }
        f = open(Path(__file__).parent.parent.joinpath(
            'users/adminconfig.yaml'), 'w+')
        yaml.dump(user_config, f, allow_unicode=True)


def user2yaml(userlist: List[str], password: List[str]):

    hashed_passwords = stauth.Hasher(password).generate()

    user_config = {
        'credentials': {
            'usernames': {

                k: {
                    'email': f'{k}@xiaoshiwole.com',
                    'name': k,
                    'password': p
                } for k, p in zip(userlist, hashed_passwords)
            }
        },
        'cookie': {
            'expiry_days': 9999,
            'key': 'some_signature_key',
            'name': 'some_cookie_name'
        },
        'preauthorized': {
            'emails': 'yuanzhoulvpi@outlook.com'
        }

    }
    f = open(Path(__file__).parent.parent.joinpath(
        'users/labeluserconfig.yaml'), 'w+')
    yaml.dump(user_config, f, allow_unicode=True)


if __name__ == '__main__':
    manage_user = ManageUser()
    manage_user.create_user(user_name='yuanz2021',
                            user_password='hangzhoudata2021')
    manage_user.create_user(user_name='yuanz2022',
                            user_password='hangzhoudata2021')
    manage_user.create_user(user_name='yuanz2023',
                            user_password='hangzhoudata2021')
    # manage_user.create_user(user_name='yuanz2022',
    #                         user_password='hangzhoudata2022')
    # manage_user.create_user(user_name='yuanz2023',
    #                         user_password='hangzhoudata2023')
    # manage_user.create_user(user_name='yuanz2024',
    #                         user_password='hangzhoudata2024')

    manage_user.delete_user(user_name='yuanz2021')
    manage_user.delete_user(user_name='yuanz2022')
    # manage_user.delete_user(user_name='yuanz2023')
