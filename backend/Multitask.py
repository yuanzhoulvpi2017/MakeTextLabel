from typing import Dict, List
from Text import ManageText

from datetime import datetime

from dataclasses import dataclass, field

from sentence_transformers import SentenceTransformer


@dataclass
class Task:
    name: str
    create_time: datetime
    manage_text: ManageText


@dataclass
class OperateStatus:
    SUCCESS = 1
    ERROR = 2


@dataclass
class OperateOutput:
    status: OperateStatus = field(default=OperateStatus.SUCCESS)
    info: str = field(default='操作成功')


class ManageTask:
    def __init__(self, model: SentenceTransformer) -> None:
        self.model = model

        self.AllTask: Dict[str, Task] = {}

    def AddNewTask(self, taskname: str) -> OperateOutput:
        if isinstance(taskname, str) and len(taskname) != 0:

            if taskname not in self.AllTask.keys():

                self.AllTask.update({taskname: Task(
                    name=taskname,
                    create_time=datetime.now(),
                    manage_text=ManageText(project_name=taskname,
                                           model=self.model))})

                return OperateOutput()
            else:
                OperateOutput(
                    status=OperateStatus.ERROR,
                    info='项目名称已经存在,不可再创建'
                )

        else:
            return OperateOutput(
                status=OperateStatus.ERROR,
                info='项目名称必须为英文且字符长度大于等于5'
            )

    def DeleteTask(self, taskname: str) -> OperateOutput:
        if isinstance(taskname, str) and len(taskname) != 0:

            if taskname not in self.AllTask.keys():

                return OperateOutput(
                    status=OperateStatus.ERROR,
                    info='未找到此项目')
            else:
                self.AllTask.pop(taskname)
                OperateOutput(
                    status=OperateStatus.SUCCESS,
                    info='已成功删除项目'
                )

        else:
            return OperateOutput(
                status=OperateStatus.ERROR,
                info='项目名称必须为英文且字符长度大于等于5'
            )

