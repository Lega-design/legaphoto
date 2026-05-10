import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカル開発用）
load_dotenv()

# Supabaseの接続情報
# Community Cloudでは st.secrets を使用し、ローカルでは環境変数を使用する
URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

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
