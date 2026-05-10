import streamlit as st
import pandas as pd
from datetime import datetime
from database import fetch_posts, create_post

# --- Page Config ---
st.set_page_config(
    page_title="LegaPhoto ",
    page_icon="📸",
    layout="wide",
)

# --- Design Customization (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .hero-section {
        padding: 60px 20px;
        background-color: #ffffff;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background: linear-gradient(45deg, #1DA1F2, #0d8bd9);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(29, 161, 242, 0.4);
    }
    
    .post-card {
        padding: 30px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        margin-bottom: 25px;
        border-top: 4px solid #1DA1F2;
        transition: transform 0.2s ease;
    }
    
    .post-card:hover {
        transform: scale(1.01);
    }
    
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin-right: 8px;
        background-color: #e1f5fe;
        color: #0288d1;
        font-weight: bold;
    }
    
    .x-link-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #000000;
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 25px;
        font-weight: bold;
        margin-top: 15px;
        font-size: 0.9em;
    }
    
    .x-link-button:hover {
        background-color: #333333;
    }

    .sidebar-info {
        padding: 15px;
        background-color: #fff9c4;
        border-radius: 10px;
        font-size: 0.85em;
        color: #5d4037;
        border: 1px solid #fff176;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Prefecture List ---
PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

# --- Navigation ---
page = st.sidebar.radio("メニュー", ["ホーム（募集一覧）", "新規投稿"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-info">
    <b>💡 ご利用案内</b><br>
    本サイトはX（Twitter）を通じたマッチングを支援します。
    連絡は各投稿のボタンからXへ移動し、直接DMをお送りください。<br><br>
    ※個人情報の取り扱いにご注意ください。
</div>
""", unsafe_allow_html=True)

# --- Page Logic ---

if page == "ホーム（募集一覧）":
    st.markdown("""
    <div class="hero-section">
        <h1 style="color: #1DA1F2; margin-bottom: 10px;">📸 LegaPhoto</h1>
        <p style="color: #666; font-size: 1.2em;">カメラマンとモデルの新しい出会いを、もっと身近に。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search / Filter Sidebar
    st.sidebar.subheader("🔍 絞り込み検索")
    search_pref = st.sidebar.selectbox("地域", ["すべて"] + PREFECTURES)
    search_costume = st.sidebar.selectbox("衣装", ["すべて", "私服", "制服", "コスプレ"])
    
    # DBからデータ取得
    try:
        posts = fetch_posts(pref=search_pref, costume=search_costume)
    except Exception as e:
        st.error(f"データの取得に失敗しました: {e}")
        posts = []
    
    # Display Posts
    if not posts:
        st.info("該当する募集が見つかりませんでした。")
    else:
        st.write(f"現在 {len(posts)} 件の募集があります")
        for post in posts:
            with st.container():
                st.markdown(f"""
                <div class="post-card">
                    <span class="tag">{post['prefecture']}</span>
                    <span class="tag">{post['costume']}</span>
                    <h3 style="margin-top: 15px;">{post['place']}</h3>
                    <p style="color: #555;"><b>撮影希望日:</b> {post['shoot_date']}</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
                    <p><b>詳細:</b><br>{post['detail']}</p>
                    <a class="x-link-button" href="https://x.com/{post['username']}" target="_blank">
                        𝕏 @{post['username']} にDMを送る
                    </a>
                </div>
                """, unsafe_allow_html=True)

elif page == "新規投稿":
    st.title("📝 募集を投稿する")
    st.info("X（旧Twitter）のアカウント名をIDとして使用します。")
    
    with st.form("post_form", clear_on_submit=True):
        username = st.text_input("X username (例: LegaPhoto)", help="＠は不要です")
        col1, col2 = st.columns(2)
        with col1:
            shoot_date = st.date_input("撮影希望日")
            prefecture = st.selectbox("地域", PREFECTURES)
        with col2:
            place = st.text_input("具体的な場所", placeholder="例：〇〇公園、都内スタジオ")
            costume = st.selectbox("衣装", ["私服", "制服", "コスプレ"])
        
        detail = st.text_area("詳細・条件など", placeholder="例：相互無償でお願いします。交通費は自己負担で...")
        
        submit = st.form_submit_button("投稿する")
        
        if submit:
            if not username or not place or not detail:
                st.error("すべての項目を入力してください。")
            else:
                new_post_data = {
                    "username": username.replace("@", ""),
                    "shoot_date": str(shoot_date),
                    "prefecture": prefecture,
                    "place": place,
                    "costume": costume,
                    "detail": detail
                }
                try:
                    create_post(new_post_data)
                    st.success("投稿が完了しました！ホーム画面で確認できます。")
                    st.balloons()
                except Exception as e:
                    st.error(f"投稿に失敗しました: {e}")
