import streamlit as st

st.set_page_config(
    page_title="Fast Label",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

sidebar_intro = """
## 介绍🐤
1. 🔧 这是一个轻量化的文本打标工具
2. 🐣 目前还只支持文本打标签任务
3. 📮 [快来分享你宝贵的建议](https://github.com/yuanzhoulvpi2017/MakeTextLabel)
"""

main_intro = """
# Fast Label
## 使用介绍
本工具🔧主要分成三个板块:
1. `webapp`: 欢迎页，主要展示本工具的概况和使用步骤。
2. `LabelUser`: 打标页，进行打标的人员的主要操作页面。
3. `Admin`: 管理页面，包括创建项目、添加条目、添加标签、管理打标等操作。

## 页面介绍
### 1. `LabelUser`
1. 需要通过用户名和密码登录。
2. 打标人员在查看问题后，可以通过点击算法推荐的匹配项、可以通过关键词搜索，找到最适合的标签。
3. 打标人员可以看到自己的数据统计


### 2. `Admin`
1. 本系统最高级的权限。需要通过一串随机密钥登录。
2. 可以增加、移除打标人员，可以查看所有打标人员的数据统计，包括导出数据等。
3. 可以创建新打标任务，添加、删除、待打标的标签以及文本等。
4. 可以导出并下载打标后的数据。
"""

st.sidebar.markdown(sidebar_intro)

st.markdown(main_intro)
