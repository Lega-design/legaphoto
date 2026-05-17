import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカル開発用）
load_dotenv()

# Supabaseの接続情報（環境変数またはStreamlit Secretsから安全に取得）
try:
    # Streamlit環境下でのキー取得
    URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
except Exception:
    # st.secretsが利用できない一般のPythonスクリプト実行時などのフォールバック
    URL = os.environ.get("SUPABASE_URL")
    KEY = os.environ.get("SUPABASE_KEY")

def get_supabase() -> Client:
    """Supabaseクライアントを初期化して返します。"""
    if not URL or not KEY:
        st.error("SupabaseのURLまたはKeyが設定されていません。")
        st.stop()
    return create_client(URL, KEY)

def fetch_posts(pref=None, costume=None):
    """DBから投稿一覧を取得します。"""
    supabase = get_supabase()
    query = supabase.table("posts").select("*").order("created_at", desc=True)
    
    if pref and pref != "すべて":
        query = query.eq("prefecture", pref)
    if costume and costume != "すべて":
        query = query.eq("costume", costume)
        
    response = query.execute()
    return response.data

def create_post(data):
    """新しい募集をDBに保存します。"""
    supabase = get_supabase()
    response = supabase.table("posts").insert(data).execute()
    return response.data

def fetch_setting(key: str) -> str:
    """DBのsettingsテーブルから指定された設定値（パスワードなど）を取得します。"""
    try:
        supabase = get_supabase()
        # maybe_single() を使うことで、データが存在しない場合もエラーにならずに安全に取得できます
        response = supabase.table("settings").select("value").eq("key", key).maybe_single().execute()
        if response and response.data:
            return response.data.get("value")
    except Exception:
        # テーブル未作成時やDBエラー時のセーフティネット
        pass
    return None

