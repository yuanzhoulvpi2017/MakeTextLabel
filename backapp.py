from typing import List
from fastapi import FastAPI
import uvicorn
import datetime
import yaml
from pathlib import Path
from dataclasses import asdict
from sentence_transformers import SentenceTransformer

from backend.User import ManageUser
from backend.Text import ManageText, SaveTextInput
from backend.Multitask import ManageTask, OperateOutput, OperateStatus


with open(Path(__file__).parent.joinpath('admin.yaml'), 'r') as f:
    admin_detail = yaml.load(f, Loader=yaml.SafeLoader)
    app_port = int(admin_detail.get('port'))


manage_user = ManageUser()
manage_task = ManageTask(model=None)  # todo


app = FastAPI()


@app.get("/create_user")
def CreateUserApi(user_name: str, user_password: str):
    res = manage_user.create_user(
        user_name=user_name, user_password=user_password)
    return asdict(res)


@app.get('/delete_user')
def DeleteUserApi(user_name: str):
    res = manage_user.delete_user(user_name=user_name)
    return asdict(res)


@app.get('/detect_user_status')
def DetectUserStatusApi(user_name: str):
    res = manage_user.detect_user_status(user_name)
    return asdict(res)


@app.get('/create_task')
def CreateTaskApi(taskname: str):
    res = manage_task.AddNewTask(taskname=taskname)
    return asdict(res)


@app.get('/delete_task')
def DeleteTaskApi(taskname: str):
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        res = manage_task.DeleteTask(taskname=taskname):
        return asdict(res)


@app.get('/Init2task')
def Init2TaskApi(taskname: str, text: List[str], label: List[str]):

    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname)
        temp_task.InitLabel(label)
        temp_task.init_text(text)
        s = OperateOutput()
        return asdict(s)


@app.get('/Addlabel2task')
def AddLabel2TaskApi(taskname: str, label: List[str]):
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname)
        temp_task.add_label(label)
        s = OperateOutput()
        return asdict(s)


@app.get('/Deletelabel2task')
def DeleteLabel2TaskApi(taskname: str, label: List[str]):
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname)
        temp_task.delete_label(label)
        s = OperateOutput()
        return asdict(s)


@app.get('/SendText4task')
def Sendtext4TaskApi(taskname: str):
    res: ManageText = manage_task.AllTask.get(taskname)
    return res.SendText


@app.get('/SearchKey4task')
def SearchKey4taskApi(taskname: str, key: str):
    res: ManageText = manage_task.AllTask.get(taskname)
    res:List[str] = res.SearchKey(key=key)
    return res


@app.get("/SaveResult4Task")
def SaveResult4TaskApi(taskname: str,
                       text: str, label: str,
                       label_user: str):

    project: ManageText = manage_task.AllTask.get(taskname)
    textinput = SaveTextInput(project=taskname,
                              text=text, label=label, label_user=label, label_datetime=datetime.now())
    project.SaveResult(textinput)
    return OperateOutput(info='成功提交')


@app.get("/")
async def root():
    return {"message": "Hello World", "datetime": datetime.datetime.now(), "test": 'this is a test'}

if __name__ == '__main__':
    print(app_port)
    uvicorn.run(app='backapp:app', host="0.0.0.0",
                port=app_port, reload=True, debug=True)
