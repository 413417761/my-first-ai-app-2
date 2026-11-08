import streamlit as st
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="AI 及格预测器", page_icon="🎓", layout="centered")

X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [0, 0, 0, 0, 1, 1, 1, 1]
model = LogisticRegression()
model.fit(X, y)

# 左侧边栏不变
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426651.png", width=100)
    st.title("关于这个 App")
    st.info("这是一个基于逻辑回归的 AI 小工具，用来预测学生的及格概率。")
    st.write("👨‍💻 开发者：Alessioo Ng")
    st.write("🚀 用 Streamlit 极速构建")

# 网页主体
st.title("🎓 大学生及格概率预测器")
st.divider()

# 直接竖排，取消分列（这样手机端完美显示）
study_hours = st.number_input("请输入你的学习时长（小时）：", min_value=0.0, max_value=24.0, value=3.5, step=0.5)

# 按钮占满全宽
if st.button("🤖 开始 AI 预测", use_container_width=True):
    prediction = model.predict([[study_hours]])[0]
    probability = model.predict_proba([[study_hours]])[0][1] * 100
    
    st.divider()
    if prediction == 1:
        st.success("预测结果：恭喜，大概率及格！")
    else:
        st.error("预测结果：危险，大概率不及格。")
    
    st.metric(label="AI 算出的及格概率", value=f"{probability:.1f}%")
