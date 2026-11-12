import streamlit as st
from zhipuai import ZhipuAI

st.set_page_config(page_title="包子", page_icon="🐱", layout="centered")

# ================= 1. 状态初始化（极其关键） =================
# 记录聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "主人你好！我是包子。"}]
# 记录可用次数（初始免费3次）
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 3 

# 读取后台 Key
try:
    api_key = st.secrets["ZHIPU_KEY"]
except:
    api_key = None

# ================= 侧边栏 =================
with st.sidebar:
    st.title("🐱 宠物档案")
    st.write("名字：包子")
    st.success("状态：已接入真实大模型大脑")
    
    st.divider()
    st.write(f"当前剩余对话额度：**{st.session_state.usage_count}** 次")
    
    # --- 卡密兑换区 ---
           card_code = st.text_input("输入你的卡密：", type="password")
        if st.button("立即兑换"):
            # 从云端保险柜读取卡密池
            valid_codes = st.secrets["VIP_CODES"]
            
            # 检查用户输入的卡密是否在保险柜的值里面
            if card_code in valid_codes.values():
                # 检查这个卡密是不是已经在这台电脑上用过了（防重复）
                if f"used_{card_code}" not in st.session_state:
                    st.session_state.usage_count += 999
                    st.session_state[f"used_{card_code}"] = True # 标记已使用
                    st.success("兑换成功！额度已充满！")
                else:
                    st.error("这个卡密已经被使用了哦！")
            else:
                st.error("卡密无效，请确认后重试！")
    
    st.divider()
    if st.button("🗑️ 清空聊天记忆", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "（包子甩了甩脑袋）我们重新认识一下吧！"}]
        st.session_state.usage_count = 3  # 清空记忆顺便重置额度
        st.rerun()
    
    system_prompt = st.text_area("设置 AI 角色（性格）：", value="你是一只可爱的、性格傲娇的电子宠物。", height=100)

# ================= 网页主体 =================
st.title("🐱 包子")
st.divider()

# 展示历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ================= 核心商业逻辑拦截 =================
if st.session_state.usage_count <= 0:
    # 额度用完了，拦截聊天
    st.warning("⚠️ 免费额度已耗尽。请查看左侧边栏，输入卡密解锁更多对话！")
    st.chat_input("余额不足...", disabled=True) # 输入框被禁用
else:
    # 还有额度，允许聊天
    if prompt := st.chat_input("和你的宠物说点什么吧..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        if not api_key:
            st.warning("找不到云端 Key，请检查 Secrets 配置。")
        else:
            with st.chat_message("assistant"):
                with st.spinner("包子思考中..."):
                    try:
                        client = ZhipuAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="glm-4-flash",
                            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                            stream=True
                        )
                        
                        def generate_chunks():
                            for chunk in response:
                                if chunk.choices[0].delta.content is not None:
                                    yield chunk.choices[0].delta.content
                        
                        ai_reply = st.write_stream(generate_chunks())
                        
                        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                        
                        # ✨ 极其关键：每次成功对话，扣除一次额度
                        st.session_state.usage_count -= 1 
                        st.rerun() # 刷新页面更新额度显示
                        
                    except Exception as e:
                        st.error(f"报错信息：{e}")
