import streamlit as st
import os
import random
import datetime
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"


def login(username, password):
    if username and password:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state.current_page = 'home'
    st.rerun()

def custom_layout():
    # CSS를 사용하여 모바일 스타일 적용
    st.markdown("""
    <style>
        .main {
            background-color: #FFFFFF;
            color: black;
        }
        .reportview-container .main .block-container {
            max-width: 375px;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .stButton>button {
            background-color: #91ED74;
            color: white;
            width: 100%;
            margin-bottom: 10px;
        }
        .stButton>button>div * {
            font-weight: 900;
        }
        div[data-testid='column'] * {
            font-weight: bold;
            background-color: transparent;
            color: #029e30;
        }    
        .stTextInput>div>div>input {
            background-color: #C0F2B0;
            color : black;
            width: 100%;
        }
        .stTextInput>label>div>p {
            color: green;
            font-weight: 900;
        }
        @media (max-width: 768px) {
            div[data-testid="column"] {
                width: 20% !important;
                flex: 1 1 calc(20% - 1rem) !important;
                min-width: 0;
            }
            div[data-testid="column"] button {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                text-align: right;
            }
            div[data-testid="stHorizontalBlock"] {
                height: 36px;
                margin: 0;
            }
    }
    div[data-baseweb="select"] > div {
        background-color: #f1f1f1;
        color: #333;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #4CAF50;
    }
    div[data-baseweb="select"] > div > div {
        padding: 8px;
    }
    .dataframe th {
        color: white;
        background-color: #4CAF50;
    }
    .dataframe td {
        color: black;
        background-color: white;
    }
    h3 {
        color: green;
    }        
        </style>
    """, unsafe_allow_html=True)

    # 상단 버튼
    def nav_button(label, page):
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()
    
    if st.session_state['logged_in']:
        col1, col2, col3 = st.columns(3)
        with col1:
            nav_button('It\'s FRU', 'home')
        with col2:
            nav_button('마이페이지', 'my_page')
        with col3:
            st.button('로그아웃', on_click=logout, type="secondary", use_container_width=True)
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            nav_button('It\'s FRU', 'home')
        with col2:
            nav_button('로그인', 'login')
        with col3:
            nav_button('회원가입', 'sign_up')
    
    st.markdown('<hr style="border:2px solid #029e30; margin-top:0px;">', unsafe_allow_html=True)
        
def home_page():

    st.image("logo.png", use_column_width=True)

    # 로그인 및 회원 가입 버튼 표시
    if st.button('로그인'):
        st.session_state.current_page = 'login'
        st.rerun()
    if st.button('회원 가입'):
        st.session_state.current_page = 'sign_up'
        st.rerun()

def login_page():
    with st.form("login_form"):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        submit_button = st.form_submit_button("로그인")

    if submit_button:
        if login(username, password):
            st.success(f"{username}님, 환영합니다!")
            st.session_state.current_page = 'main'
            st.rerun()
        else:
            st.error("로그인에 실패했습니다. 사용자 이름과 비밀번호를 확인하세요.")

def signup_page():
    with st.form("signup_form"):
        username = st.text_input("사용자 이름")
        password = st.text_input("비밀번호", type="password")
        confirm_password = st.text_input("비밀번호 확인", type="password")
        submit_button = st.form_submit_button("가입하기")

    if submit_button:
        st.success("가입에 성공했습니다!")
        st.session_state.current_page = 'login'
        st.rerun()

def main_page():
    st.image("logo.png", use_column_width=True)
    if st.button('과일 고르기'):
        st.session_state.current_page = 'fruit_recognition'
        st.rerun()

    if st.button('장바구니'):
        st.session_state.current_page = 'cart'
        st.rerun()

    if st.button('마이페이지'):
        st.session_state.current_page = 'my_page'
        st.rerun()

    if st.button('로그아웃'):
        logout()
        st.session_state.current_page = 'home'
        st.rerun()

def fruit_recognition_page():
    # 카메라 입력 위젯
    img_file_buffer = st.camera_input("사진을 찍어주세요")
    use_photo = None

    # 사진이 찍혔을 때
    if img_file_buffer is not None:
        # 이미지 읽기
        img = Image.open(img_file_buffer)
        # 이미지 표시
        st.image(img, caption="찍은 사진", use_column_width=True)
        # 사진 사용 여부 묻기
        use_photo = st.radio(
            "이 사진을 사용하시겠습니까?",
            ('예', '아니오')
        )
    
        # 사용 여부에 따른 동작
        if use_photo == '예':
            # examples 폴더에서 jpg 파일 중 하나를 랜덤하게 선택
            examples_dir = "examples"
            jpg_files = [f for f in os.listdir(examples_dir) if f.endswith(".jpg")]
            selected_image = random.choice(jpg_files)
            image_path = os.path.join(examples_dir, selected_image)
            fruit_name = os.path.splitext(selected_image)[0]
            quality_options = ['상', '중', '하']
            quality = random.choice(quality_options)

            if quality == '상':
                discount = f"{random.randint(1, 5)}%"
            elif quality == '중':
                discount = f"{random.randint(10, 15)}%"
            else:
                discount = f"{random.randint(20, 30)}%"
            
            # 판매가 및 할인가 계산
            sale_price = random.randint(10, 80) * 100
            discount_price = int(sale_price * (1 - int(discount[:-1]) / 100))

            st.session_state['new_item'] = {
                'fruit_name': fruit_name,
                'quality': quality,
                'discount': discount,
                'sale_price' : sale_price,
                'discount_price' : discount_price,
                'image_path': image_path
            }
            st.session_state.current_page = 'fruit_info'
            st.rerun()
        else:
            st.rerun()

def fruit_info_page():
    selected_fruit = st.session_state['new_item']
    fruit_name = selected_fruit['fruit_name']
    quality = selected_fruit['quality']
    discount = selected_fruit['discount']
    image_path = selected_fruit['image_path']

    # 과일 이름 표시
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 50px; border: 2px solid black; margin-bottom: 20px;">
            <strong>{fruit_name}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 이미지 중앙에 표시
    st.image(image_path, use_column_width=True)

    # 과일 정보 표시
    st.write(f"**과일 이름:** {fruit_name}")
    st.write(f"**품질:** {quality}")
    st.write(f"**할인율:** {discount}")

    # 버튼들
    if st.button('장바구니에 담기'):
        st.session_state.current_page = 'cart'
        st.rerun()

    if st.button('다시 고르기'):
        del st.session_state['new_item']
        st.session_state.current_page = 'fruit_recognition'
        st.rerun()

def cart_page():
    # 초기화
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []

    # 장바구니에 담기 버튼을 눌러서 이 페이지로 이동할 때, 행 하나가 추가됨
    if 'new_item' in st.session_state:
        st.session_state['cart'].append(st.session_state['new_item'])
        del st.session_state['new_item']
    
    table_data = []
    total_price = 0
    total_discount_price = 0

    for item in st.session_state['cart']:
        fruit_name = item['fruit_name']
        sale_price = item['sale_price']
        discount_price = item['discount_price']
        image_path = item['image_path']

        # 이미지 썸네일 생성
        image = Image.open(image_path)
        image.thumbnail((50, 50))

        # 테이블 행 추가
        table_data.append([image, fruit_name, f"{sale_price}원", f"{discount_price}원"])

        # 총 판매가 및 총 할인가 계산
        total_price += sale_price
        total_discount_price += discount_price

    # 테이블 표시
    for row in table_data:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        col1.image(row[0])
        col2.write(row[1])
        col3.write(row[2])
        col4.write(row[3])
        if col5.button('x', key=row[3]):
            st.session_state['cart'] = [item for item in st.session_state['cart'] if item['discount_price'] != row[3]]
            st.rerun()
    
    if not st.session_state['cart']:
        st.write("장바구니가 비어 있습니다.")

    st.write(" ")
    # 총계 표시
    st.write(f"""\n판매가: {total_price}원\n
할인가: {total_discount_price}원\n
적립 마일리지: {int(total_discount_price * 0.05)}p""")

    # 결제하기 및 과일 고르기 버튼
    if st.button('결제하기'):
        if st.session_state['cart']:
            now = datetime.datetime.now()
            payment_info = {
                'date': now.strftime("%Y-%m-%d"),
                'time': now.strftime("%H:%M:%S"),
                'items': st.session_state['cart'],
                'total_discount_price': total_discount_price
            }

            if 'payment_history' not in st.session_state:
                st.session_state['payment_history'] = []

            st.session_state['payment_history'].append(payment_info)
            del st.session_state['cart']

            st.session_state.current_page = 'payment_complete'
            st.rerun()
        else:
            st.warning("장바구니가 비어 있습니다.")
            st.rerun()
    
    if st.button('계속 고르기'):
        st.session_state.current_page = "fruit_recognition"
        st.rerun()
    
    if st.button("메인으로"):
        st.session_state.current_page = "main"
        st.rerun()

def payment_complete_page():
    # 결제 성공 메시지
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 50px; border: 2px solid black; margin-bottom: 20px;">
            <strong>결제에 성공했습니다!</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 장바구니 정보 초기화
    if 'cart' in st.session_state:
        del st.session_state['cart']

    # 버튼들
    if st.button('메인으로'):
        st.session_state.current_page = 'main'
        st.rerun()

    if st.button('계속 고르기'):
        st.session_state.current_page = 'fruit_recognition'
        st.rerun()

def my_info_page():
    # 프로필 사진 (기존 코드 유지)
    st.markdown(
        """
        <div style="display: flex; justify-content: center;"> 
        <div style="display: flex; justify-content: center; align-items: center; height: 100px; width: 100px; background-color: black; color: white; margin-bottom: 20px;">
            <strong>photo</strong>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 이름
    st.write("이름: 홍길동")

    # 마일리지
    total_mileage = sum([int(payment['total_discount_price'] * 0.05) for payment in st.session_state.get('payment_history', [])])
    st.write(f"마일리지: {total_mileage}p")

    st.subheader("구매 목록")
    if 'payment_history' in st.session_state and st.session_state['payment_history']:
        payment_table = []
        payment_detail_list = []
        for idx, payment in enumerate(st.session_state['payment_history']):
            purchase_date = f"{payment['date']}"
            purchase_time = f"{payment['time'][:5]}"
            first_item = payment['items'][0]['fruit_name']
            additional_items = len(payment['items']) - 1
            product_info = f"{first_item} 외 {additional_items}개" if additional_items > 0 else first_item
            total_discount_price = payment['total_discount_price']

            payment_row = {
                "id": idx+1,  # Add an id for each row
                "구매 일시": purchase_date + '\n' + purchase_time,
                "상품": product_info,
                "구매 가격": total_discount_price
            }
            payment_table.append(payment_row)

            payment_detail_table = [{
                "상품": item['fruit_name'],
                "판매가": item['sale_price'],
                "구매가": item['discount_price']
            } for item in payment['items']]
            payment_detail_list.append(pd.DataFrame(payment_detail_table))

        payment_df = pd.DataFrame(payment_table)
        
        # 메인 테이블 스타일링 및 표시
        styled_main_table = payment_df.style.set_properties(**{
            'color': 'black',
            'background-color': 'white',
            'border-color': 'darkgray'
        }).set_table_styles([
            {'selector': 'th', 'props': [('color', 'white'), ('background-color', '#4CAF50'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('border', '1px solid lightgray')]},
            {'selector': '', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
        ]).hide(axis="index")

        st.write(styled_main_table.to_html(), unsafe_allow_html=True)

        st.subheader("상세 구매 내역 조회")
        # Check if there are any selected rows
        selected_display = st.selectbox("", payment_df['구매 일시'].tolist())
        selected_id = payment_df['구매 일시'].tolist().index(selected_display)

        if selected_id is not None:
            # 상세 정보 표시
            with st.expander("상세 구매 내역", expanded=True):
                if 0 <= selected_id < len(payment_detail_list):
                    detail_df = payment_detail_list[selected_id]
                    
                    # 스타일이 적용된 HTML 표 생성
                    styled_table = detail_df.style.set_properties(**{
                        'color': 'black',
                        'background-color': 'white',
                        'border-color': 'darkgray'
                    }).set_table_styles([
                        {'selector': 'th', 'props': [('color', 'white'), ('background-color', '#4CAF50'), ('font-weight', 'bold')]},
                        {'selector': 'td', 'props': [('border', '1px solid lightgray')]},
                        {'selector': '', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
                    ]).hide(axis="index")

                    # 스타일이 적용된 HTML을 Streamlit에 표시
                    st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)
                else:
                    st.write("선택한 구매 내역에 대한 상세 정보가 없습니다.")
        else:
            st.write("구매 내역을 선택하세요.")
    else:
        st.subheader("구매 내역이 없습니다.")
    
    if st.button('메인으로'):
        st.session_state.current_page = 'main'
        st.rerun()

# 메인 앱 로직
def main():
    custom_layout()

    if not st.session_state.logged_in:
        if st.session_state.current_page == "home":
            home_page()
        elif st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "sign_up":
            signup_page()
    else:
        if st.session_state.current_page == "main":
            main_page()
        elif st.session_state.current_page == "home":
            main_page()
        elif st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "sign_up":
            signup_page()
        elif st.session_state.current_page == "my_page":
            my_info_page()
        elif st.session_state.current_page == "fruit_recognition":
            fruit_recognition_page()
        elif st.session_state.current_page == "fruit_info":
            fruit_info_page()
        elif st.session_state.current_page == "payment_complete":
            payment_complete_page()
        elif st.session_state.current_page == "cart":
            cart_page()

if __name__ == "__main__":
    main()


