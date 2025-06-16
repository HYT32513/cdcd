import streamlit as st
import random

st.set_page_config(page_title="무림 캐릭터 추천기", page_icon="⚔️")

st.title("⚔️ 무림 캐릭터 추천기 (질문 확대판)")

# 1. 사용자 입력 질문 추가
gender = st.radio("성별을 선택하세요", ["남성", "여성", "기타"])

personality = st.radio(
    "당신의 성격은 어떤 편인가요?",
    ["침착하고 냉철함", "열정적이고 직선적임", "부드럽고 사려 깊음"],
)

value = st.radio(
    "무림에서 가장 중요하게 생각하는 가치는 무엇인가요?",
    ["명예", "힘", "자유", "지혜"],
)

weapon = st.radio(
    "가장 선호하는 무기는 무엇인가요?",
    ["검", "활", "주먹/망치", "도끼", "창"],
)

# 2. 기본 이름 후보 (성별별)
base_names = {
    "남성": ["검사", "도사", "객", "무사", "서생"],
    "여성": ["검사", "도인", "선녀", "협객", "마녀"],
    "기타": ["검객", "도인", "협객", "무사", "선녀"]
}

# 3. 접두어(수식어) 리스트
prefixes = [
    "청운", "빙설", "흑풍", "철권", "서광", "한기",
    "불꽃", "천둥", "혈풍", "폭염", "전광", "적풍",
    "바람", "달빛", "청류", "선비", "명운", "청송",
    "흑월", "빙화", "야광", "월광", "서리", "풍운",
    "화염", "천화", "혈검", "폭풍", "적화", "번개",
    "달빛", "연화", "청풍", "서리", "청연", "비취",
    "명", "은월", "빙하", "흑철", "서리", "폭풍",
    "불꽃", "혈풍", "천뢰", "적화", "구름", "청송",
    "맑은샘", "산들바람", "은하", "한별", "태풍", "유성"
]

# 4. 캐릭터 설명 예시 (질문 조합별)
# 키는 (성격, 가치, 무기)
descriptions = {
    ("침착하고 냉철함", "명예", "검"): "명예로운 냉철한 검사. 조용하지만 강한 의지를 가진 무림의 지킴이.",
    ("침착하고 냉철함", "힘", "주먹/망치"): "강인한 힘과 냉철한 판단력을 가진 무사, 전장을 지배한다.",
    ("열정적이고 직선적임", "자유", "활"): "자유를 사랑하는 열정적인 궁수, 바람처럼 빠르고 예리하다.",
    ("부드럽고 사려 깊음", "지혜", "도끼"): "지혜롭고 온화한 도인, 도끼를 들고 평화를 지킨다.",
    # ... 여기에 더 다양한 조합 추가 가능
}

# 기본 설명 (조합에 없을 경우)
default_description = "신비로운 무림 고수로서 모든 어려움을 극복하는 강인한 인물입니다."

# 5. 캐릭터 이름 생성 함수
def make_character_name(gender):
    prefix = random.choice(prefixes)
    base = random.choice(base_names.get(gender, base_names["기타"]))
    return prefix + base

# 6. 캐릭터 설명 선택 함수
def get_character_description(personality, value, weapon):
    return descriptions.get((personality, value, weapon), default_description)

# 7. 버튼 클릭 시 결과 출력
if st.button("캐릭터 생성하기"):
    character_name = make_character_name(gender)
    character_desc = get_character_description(personality, value, weapon)
    
    st.subheader
