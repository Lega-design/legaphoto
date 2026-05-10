import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む（ローカル開発用）
load_dotenv()

# Supabaseの接続情報（一時的に直接指定）
URL = "https://ikwoqawdbdvotjygybtks.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlrd29xYXdkYmR2b3RqeWdidGtzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgzOTkxNTYsImV4cCI6MjA5Mzk3NTE1Nn0.4E0jmaf5UPQ4iJ0t9G87T74SYB3wl1SLe1B-QqybV6A"

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
