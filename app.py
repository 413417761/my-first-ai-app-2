import streamlit as st
from sklearn.linear_model import LogisticRegression

# 设置网页的标题和图标（在浏览器标签页上显示）
st.set_page_config(page_title="AI 及格预测器", page_icon="🎓", layout="centered")

# 训练模型
X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [0, 0, 0, 0, 1, 1, 1, 1]
model = LogisticRegression()
model.fit(X, y)

# ====== 左侧边栏 ======
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426651.png", width=100) # 放个小图标
    st.title("关于这个 App")
    st.info("这是一个基于逻辑回归的 AI 小工具，用来预测学生的及格概率。")
    st.write("👨‍💻 开发者：Alessioo Ng")
    st.write("🚀 用 Streamlit 极速构建")

# ====== 网页主体 ======
st.title("🎓 大学生及格概率预测器")
st.divider()

# 分两列显示输入和按钮
col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input("请输入你的学习时长（小时）：", min_value=0.0, max_value=24.0, value=3.5, step=0.5)

with col2:
    st.write("") # 占位，为了对齐
    st.write("") # 占位
    if st.button("🤖 开始 AI 预测", use_container_width=True):
        # 把结果存在 session_state 里，这样点完按钮不会消失
        st.session_state["prediction"] = model.predict([[study_hours]])[0]
        st.session_state["probability"] = model.predict_proba([[study_hours]])[0][1] * 100

# 如果已经有预测结果了，就展示出来
if "prediction" in st.session_state:
    st.divider()
    if st.session_state["prediction"] == 1:
        st.success("预测结果：恭喜，大概率及格！")
    else:
        st.error("预测结果：危险，大概率不及格。")
    
    # 这是 Streamlit 最装逼的组件：数据指标卡片
    st.metric(label="AI 算出的及格概率", value=f"{st.session_state['probability']:.1f}%")
