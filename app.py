import streamlit as st
from zhipuai import ZhipuAI

# 设置网页标题
st.set_page_config(page_title="包子", page_icon="🐱", layout="centered")

# ================= 侧边栏 =================
with st.sidebar:
    st.title("🐱 宠物档案")
    st.write("名字：包子")
    st.success("状态：已接入真实大模型大脑 (安全模式)")
    
    # 这里的代码都在 with st.sidebar: 的缩进里，完美对齐
    st.divider()
    system_prompt = st.text_area(
        "设置 AI 角色（性格）：", 
        value="你是一只可爱的、性格有点傲娇的电子宠物。请用简短、活泼的语气和主人聊天。",
        height=100
    )
    
    st.divider()
    if st.button("🗑️ 清空聊天记忆", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "（包子甩了甩脑袋）主人，我什么都不记得了，我们重新认识一下吧！"}]
        st.rerun()

# 从云端保险箱读取 Key
# 注意：如果你在本地跑，可能会报错，因为在云端设置了 Secrets 才有
try:
    api_key = st.secrets["ZHIPU_KEY"]
except:
    api_key = None

# ================= 网页主体 =================
st.title("🐱 包子")
st.divider()

# 1. 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "主人你好！我已经接入了真实的大模型，现在我很聪明啦！"}]

# 2. 循环展示历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. 接收用户输入
if prompt := st.chat_input("和你的宠物说点什么吧..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 调用真实大模型
    if not api_key:
        st.warning("找不到云端 Key 哦！请确认后台 Secrets 是否配置正确。")
    else:
        with st.chat_message("assistant"):
            with st.spinner("包子思考中..."):
                try:
                    client = ZhipuAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="glm-4-flash",
                        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                        stream=True  # 开启流式输出
                    )
                    
                    # 用生成器把字一个一个吐出来
                    def generate_chunks():
                        for chunk in response:
                            # 防止有些空包报错
                            if chunk.choices[0].delta.content is not None:
                                yield chunk.choices[0].delta.content
                    
                                        # st.write_stream 展现打字机效果
                    ai_reply = st.write_stream(generate_chunks())
                    
                    # 把 AI 的回复存进记录里
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                                        # 触发一个底部弹窗提示
                    st.toast('包子发来了一条新消息！', icon='🐱')
                    st.error(f"AI 连不上网啦，报错信息：{e}")
