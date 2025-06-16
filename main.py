import streamlit as st
import os

# 🌐 페이지 설정
st.set_page_config(page_title="무림 캐릭터 생성기", page_icon="🗡️")

# 세션 초기화
if "step" not in st.session_state:
    st.session_state.step = 1

# 🌟 제목
st.title("⚔️ 당신의 무림 캐릭터는?")
st.markdown("간단한 질문에 답하면 AI가 당신만의 캐릭터를 만들어줍니다!")

# 📍 STEP 1: 성향 질문
if st.session_state.step == 1:
    gender = st.radio("당신의 성별은?", ["남성", "여성", "기타"])
    q1 = st.radio("성격은 어떤 편인가요?", ["침착하고 냉철함", "열정적이고 직선적임", "부드럽고 사려 깊음"])
    q2 = st.radio("결정을 내릴 때?", ["직감", "논리", "타인의 감정"])
    q3 = st.radio("무림에서 맡고 싶은 역할은?", ["전투의 최전선", "정보 수집과 전략", "치유와 조율"])

    if st.button("캐릭터 생성하기"):
        st.session_state.gender = gender
        st.session_state.answers = [q1, q2, q3]
        st.session_state.step = 2

# 📍 STEP 2: 캐릭터 생성 & 출력
if st.session_state.step == 2:
    with st.spinner("🧠 당신의 캐릭터를 만드는 중입니다..."):

        # 🎯 GPT에게 이름 + 소개 + 이야기 생성 요청
        def get_character_info(gender, answers):
            prompt = f"""
            사용자의 성별은 {gender}이고, 성향은 다음과 같다:
            1. {answers[0]}
            2. {answers[1]}
            3. {answers[2]}
            
            이 정보를 바탕으로 다음을 만들어줘:
            - 무협 세계에 어울리는 고유한 캐릭터 이름 (한글, 최대 5자)
            - 간단한 캐릭터 소개 (3문장 이내)
            - 이 캐릭터가 주인공인 짧은 이야기 (5~6문장, 무협 스타일)

            출력 형식:
            이름: ...
            소개: ...
            이야기: ...
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            return response["choices"][0]["message"]["content"]

        character_info = get_character_info(
            st.session_state.gender, st.session_state.answers
        )

        # 결과 파싱
        try:
            lines = character_info.strip().split("\n")
            name = lines[0].replace("이름: ", "").strip()
            intro = lines[1].replace("소개: ", "").strip()
            story = "\n".join([line.replace("이야기: ", "") for line in lines[2:]]).strip()
        except:
            name = "이름 생성 오류"
            intro = "소개 생성 오류"
            story = "이야기 생성 오류"

        # 🖼️ 캐릭터 이미지 생성 (DALL·E)
        dalle_prompt = f"무협 세계의 {st.session_state.gender} 캐릭터, 이름은 {name}, {intro} 느낌, 웹툰 스타일, 디테일한 일러스트"
        image_response = openai.Image.create(
            prompt=dalle_prompt,
            n=1,
            size="512x512"
        )
        image_url = image_response["data"][0]["url"]

    # 출력
    st.success(f"🎉 당신의 캐릭터 이름: **{name}**")
    st.image(image_url, caption="AI가 그린 무림 캐릭터", use_column_width=True)
    st.subheader("🧬 캐릭터 소개")
    st.write(intro)
    st.subheader("📖 이야기")
    st.write(story)

    # 다시 시작 버튼
    if st.button("다시 해보기"):
        st.session_state.step = 1
