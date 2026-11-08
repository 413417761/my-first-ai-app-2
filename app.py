import streamlit as st
from sklearn.linear_model import LogisticRegression

# ================= 1. 后台逻辑（训练 AI 模型） =================
# 为了网页能独立运行，我们在后台悄悄把数据喂给 AI
X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [0, 0, 0, 0, 1, 1, 1, 1]

model = LogisticRegression()
model.fit(X, y)

# ================= 2. 前端页面（用 Streamlit 画 UI） =================
# 网页的大标题
st.title("🎓 大学生及格概率预测器")
st.write("这是我独立开发的第一个 AI 网页应用！")

# 这行代码相当于你以前写的 <input type="number">
study_hours = st.number_input("请输入你的学习时长（小时）：", min_value=0.0, max_value=24.0, value=3.5, step=0.5)

# 这行代码相当于你以前写的 <button>
if st.button("🤖 开始 AI 预测"):
    # 当按钮被点击时，触发以下逻辑
    # 把用户输入的数字传给 AI 模型
    prediction = model.predict([[study_hours]])
    probability = model.predict_proba([[study_hours]])
    
    # 提取及格概率并格式化
    pass_rate = probability[0][1] * 100
    
    # 在网页上展示结果
    st.divider() # 画一条分割线
    if prediction[0] == 1:
        st.success(f"🎉 预测结果：**及格**！\n\n AI 算出的及格概率高达：**{pass_rate:.1f}%**")
    else:
        st.error(f"⚠️ 预测结果：**不及格**。\n\n AI 算出的及格概率仅为：**{pass_rate:.1f}%**")
