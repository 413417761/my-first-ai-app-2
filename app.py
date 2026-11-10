import streamlit as st
from zhipuai import ZhipuAI

# 设置网页标题
st.set_page_config(page_title="我的 AI 宠物", page_icon="🐱", layout="centered")

# 侧边栏
with st.sidebar:
    st.title("🐱 宠物档案")
    st.write("名字：Alessioo 的小助手")
    st.success("状态：已接入真实大模型大脑 🧠")
    
    # ⚠️ 这里需要输入你的 API Key
    api_key = st.text_input("请输入你的智谱 API Key：", type="password")
    st.info("你的 Key 只会在本地浏览器中运行，不会上传到服务器，放心使用。")

# 网页主体
st.title("🐱 我的 AI 电子宠物")
st.divider()

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "主人你好！我已经接入了真实的大模型，现在我很聪明啦！"}]

# 循环展示历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收用户输入
if prompt := st.chat_input("和你的宠物说点什么吧..."):
    
    # 1. 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. 调用真实大模型
    if not api_key:
        st.warning("请先在左侧边栏输入你的智谱 API Key 哦！")
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("AI 宠物思考中..."):
                try:
                    # 连接大模型
                    client = ZhipuAI(api_key=api_key)
                    # 调用免费模型
                    response = client.chat.completions.create(
                        model="glm-4-flash", # 这是完全免费的模型
                        messages=[{"role": "system", "content": "你是一只可爱的、性格有点傲娇的电子宠物。请用简短、活泼的语气和主人聊天。"}] + st.session_state.messages,
                        stream=False
                    )
                    ai_reply = response.choices[0].message.content
                    message_placeholder.write(ai_reply)
                    
                    # 3. 保存回复
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    st.error(f"AI 连不上网啦，报错信息：{e}")
