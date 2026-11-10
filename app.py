import streamlit as st
import time
import random

# 设置网页标题
st.set_page_config(page_title="我的 AI 宠物", page_icon="🐱", layout="centered")

# 侧边栏
with st.sidebar:
    st.title("🐱 宠物档案")
    st.write("名字：Alessioo 的小助手")
    st.write("状态：正在学习中...")
    st.info("这是一个没有接大模型 API 的纯前端演示版。")

# 网页主体
st.title("小包子")
st.divider()

# 初始化聊天记录（存在浏览器的内存里）
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "主人你好！我是你的 AI 宠物，今天想聊点什么？"}]

# 循环展示历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收用户输入（这就是 Streamlit 专属的聊天输入框）
if prompt := st.chat_input("和你的宠物说点什么吧..."):
    
    # 1. 先把用户的话存进记录并显示出来
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. 模拟 AI 思考和回复的过程
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # 用来占位
        with st.spinner("AI 宠物正在思考中..."):
            time.sleep(1) # 假装思考 1 秒
            
            # 这里是“模拟大脑”，用简单的规则代替真正的大模型
            if "你好" in prompt or "hello" in prompt.lower():
                ai_reply = "喵喵！主人好呀！"
            elif "吃" in prompt:
                ai_reply = "我饿了！想吃小鱼干或者喂我一点数据垃圾~"
            elif "你是谁" in prompt:
                ai_reply = "我是你亲手写代码创造出来的第一只 AI 宠物！"
            else:
                replies = ["听起来很有趣！", "我不太懂，但我大受震撼。", "如果接入了真实的大模型，我会回答得更聪明哦！"]
                ai_reply = random.choice(replies)
            
            # 显示回复
            message_placeholder.write(ai_reply)
    
    # 3. 把 AI 的回复也存进记录
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
