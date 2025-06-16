import streamlit as st
import openai

# OpenAI API 키 설정 (본인 키로 교체 or secrets.toml 사용)
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="무림 캐릭터 생성기", page_icon="🗡️")

st.title("⚔️ 무림 캐릭터 생성기")
st.write("성별과 성향을 선택하면 무림 캐릭터 이름과 외형을 만들어 드립니다.")

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    gender = st.radio("성별을 선택하세요", ["남성", "여성", "기타"])
    personality = st.radio(
        "당신의 성향은?",
        ["침착하고 냉철함", "열정적이고 직선적임", "부드럽고 사려 깊음"],
    )
    if st.button("캐릭터 생성"):
        st.session_state.gender = gender
        st.session_state.personality = personality
        st.session_state.step = 2

if st.session_state.step == 2:
    with st.spinner("캐릭터 이름과 외형을 생성 중입니다..."):
        prompt = f"""
        당신은 무협 소설 작가입니다.
        사용자 성별: {st.session_state.gender}
        사용자 성향: {st.session_state.personality}

        이 정보를 바탕으로,
        1) 무협 세계에 어울리는 독특한 캐릭터 이름 (한글, 최대 5글자)
        2) 캐릭터의 외형을 3~4문장으로 묘사

        아래 형식으로 출력해 주세요:

        이름: <캐릭터 이름>
        외형: <외형 묘사>
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8,
        )
        text = response.choices[0].message.content.strip()

        # 이름과 외형 분리
        name, appearance = "", ""
        for line in text.split("\n"):
            if line.startswith("이름:"):
                name = line.replace("이름:", "").strip()
            elif line.startswith("외형:"):
                appearance = line.replace("외형:", "").strip()
            elif name and not appearance and line.strip():
                appearance += " " + line.strip()

        st.header(f"🗡️ 캐릭터 이름: {name}")
        st.subheader("👁️ 캐릭터 외형")
        st.write(appearance)

        if st.button("다시 생성하기"):
            st.session_state.step = 1
            st.experimental_rerun()
