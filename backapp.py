from typing import List
from fastapi import FastAPI
import uvicorn
from  datetime import datetime
import yaml
from pathlib import Path
from dataclasses import asdict
from sentence_transformers import SentenceTransformer

from backend.User import ManageUser
from backend.Text import ManageText, SaveTextInput
from backend.Multitask import ManageTask, OperateOutput, OperateStatus
import logging
logger = logging.getLogger(__name__)



with open(Path(__file__).parent.joinpath('admin.yaml'), 'r') as f:
    admin_detail = yaml.load(f, Loader=yaml.SafeLoader)
    app_port = int(admin_detail.get('port'))

model = SentenceTransformer(
    model_name_or_path="hfl/chinese-roberta-wwm-ext", device='cpu')


manage_user = ManageUser()
manage_task = ManageTask(model=model)  # todo


app = FastAPI()


@app.get("/create_user")
def CreateUserApi(user_name: str, user_password: str):

    res = manage_user.create_user(
        user_name=user_name, user_password=user_password)
    logger.info(f"创建用户: {user_name}")
    return asdict(res)


@app.get('/delete_user')
def DeleteUserApi(user_name: str):
    res = manage_user.delete_user(user_name=user_name)
    logger.info(f"删除用户: {user_name}")
    return asdict(res)


@app.get('/detect_user_status')
def DetectUserStatusApi(user_name: str):
    res :OperateOutput= manage_user.detect_user_status(user_name)
    logger.info(f"检测用户状态: {user_name}")
    return asdict(res)


@app.get('/create_task')
def CreateTaskApi(taskname: str):
    logger.info(f"创建任务: {taskname}")
    res :OperateOutput= manage_task.AddNewTask(taskname=taskname)
    return asdict(res) # 这里需要改进


@app.get('/delete_task')
def DeleteTaskApi(taskname: str):
    logger.info(f"删除任务: {taskname}")
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        res :OperateOutput= manage_task.DeleteTask(taskname=taskname)
        return asdict(res)

@app.get('/TaskList')
def TaskListApi():
    logger.info(f"查看所有任务列表")
    res = list(manage_task.AllTask.keys())
    return res 


@app.post('/Init2task')
def Init2TaskApi(taskname: str, text: List[str], label: List[str]):

    logger.info(f"初始化任务, taskname : {taskname}, text_length: {len(text)}, label_length: {len(label)}")

    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname).manage_text
        temp_task.InitLabel(label)
        temp_task.init_text(text)
        s = OperateOutput()
        return asdict(s)


@app.post('/Addlabel2task')
def AddLabel2TaskApi(taskname: str, label: List[str]):
    logger.info(f"添加label, taskname : {taskname}, label_length : {label}")
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname).manage_text
        temp_task.add_label(label)
        s = OperateOutput()
        return asdict(s)


@app.post('/Deletelabel2task')
def DeleteLabel2TaskApi(taskname: str, label: List[str]):
    logger.info(f"删除label, taskname : {taskname}, label_length : {label}")
    if taskname not in manage_task.AllTask.keys():
        s = OperateOutput(status=OperateStatus.ERROR, info='没有这个项目')
        return asdict(s)
    else:
        temp_task: ManageText = manage_task.AllTask.get(taskname).manage_text
        temp_task.delete_label(label)
        s = OperateOutput()
        return asdict(s)


@app.get('/SendText4task')
def Sendtext4TaskApi(taskname: str):
    logger.info(f"发送文本 taskname : {taskname}")
    res: ManageText = manage_task.AllTask.get(taskname).manage_text

    return asdict(res.SendText)


@app.get('/SearchKey4task')
def SearchKey4taskApi(taskname: str, key: str):
    logger.info(f"搜索关键词, taskname : {taskname}, key : {key}")
    res: ManageText = manage_task.AllTask.get(taskname).manage_text
    res:List[str] = res.SearchKey(key=key)
    return res


@app.get("/SaveResult4Task")
def SaveResult4TaskApi(taskname: str,
                       text: str, 
                       label: str,
                       label_user: str):

    logger.info(f"保存数据: taskname : {taskname}, text : {text}, label : {label}, label_user: {label_user}")

    project: ManageText = manage_task.AllTask.get(taskname).manage_text
    textinput = SaveTextInput(project=taskname,
                              text=text, label=label, 
                              label_user=label_user, 
                              label_datetime=datetime.now())
    project.SaveResult(textinput)
    return asdict(OperateOutput(info='成功提交'))





@app.get("/")
async def root():
    return {"message": "Hello World", "datetime": datetime.now(), "test": 'this is a test'}

if __name__ == '__main__':
    print(app_port)
    uvicorn.run(app='backapp:app', host="0.0.0.0",
                port=app_port, reload=False, debug=True)
