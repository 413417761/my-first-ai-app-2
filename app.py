import streamlit as st
from zhipuai import ZhipuAI
from supabase import create_client, Client
import uuid

st.set_page_config(page_title="包子", page_icon="🐱", layout="centered")

# ================= 1. 连接云端数据库 =================
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(supabase_url, supabase_key)
    zhipu_api_key = st.secrets["ZHIPU_KEY"]
except Exception as e:
    st.error(f"云端配置读取失败: {e}")
    st.stop()

# ================= 2. 识别用户并读取云端额度 =================
# 我们用浏览器的 URL 参数来生成一个永久用户 ID（模拟登录）
if "user_id" not in st.query_params:
    # 如果是新访客，生成一个唯一ID，并写入数据库
    new_id = str(uuid.uuid4())
    st.query_params["user_id"] = new_id
    supabase.table("user_quotas").insert({"user_id": new_id, "quota": 3}).execute()
    user_quota = 3
else:
    # 如果是老访客，去数据库里把他的额度查出来
    user_id = st.query_params["user_id"]
    response = supabase.table("user_quotas").select("quota").eq("user_id", user_id).execute()
    
    if not response.data:
        # 防错机制：如果数据库里没这个ID了，重新建
        supabase.table("user_quotas").insert({"user_id": user_id, "quota": 3}).execute()
        user_quota = 3
    else:
        user_quota = response.data[0]["quota"]


# ================= 侧边栏 =================
with st.sidebar:
    st.title("🐱 宠物档案")
    st.write("名字：包子")
    st.success("状态：已接入云端数据库")
    
    st.divider()
    # 这里显示的是从数据库拉取的真实额度
    st.write(f"当前云端剩余额度：**{user_quota}** 次")
    
    with st.expander("💳 额度用完了？点击解锁"):
        card_code = st.text_input("输入你的卡密：", type="password")
        if st.button("立即兑换"):
            valid_codes = st.secrets["VIP_CODES"]
            if card_code in valid_codes.values():
                # 兑换成功，直接去数据库里加上 999 额度
                new_quota = user_quota + 999
                supabase.table("user_quotas").update({"quota": new_quota}).eq("user_id", user_id).execute()
                st.success("兑换成功！刷新页面即可看到新额度！")
                st.rerun()
            else:
                st.error("卡密无效！")
    
    st.divider()
    if st.button("🗑️ 清空聊天记忆", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "（包子甩了甩脑袋）我们重新认识一下吧！"}]
        st.rerun()
    
    system_prompt = st.text_area("设置 AI 角色（性格）：", value="你是一只可爱的、性格傲娇的电子宠物。", height=100)

# ================= 网页主体 =================
st.title("🐱 包子")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "主人你好！我已经接入了真实的大模型，现在我很聪明啦！"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ================= 核心商业逻辑拦截 =================
if user_quota <= 0:
    st.warning("⚠️ 云端免费额度已耗尽。请查看左侧边栏，输入卡密解锁！")
    st.chat_input("余额不足...", disabled=True)
else:
    if prompt := st.chat_input("和你的宠物说点什么吧..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("包子思考中..."):
                try:
                    client = ZhipuAI(api_key=zhipu_api_key)
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
                    
                    # ✨ 扣减云端额度
                    new_quota = user_quota - 1
                    supabase.table("user_quotas").update({"quota": new_quota}).eq("user_id", user_id).execute()
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"报错信息：{e}")
