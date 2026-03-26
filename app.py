"""
VIP Customer Deep-Link Generator
A premium tool for professional VIP managers to generate bulk Telegram deep-links.
Built with glassmorphism design principles and secure access control.
"""

import streamlit as st
import pandas as pd
import requests
import urllib.parse
import io
import time
from typing import Optional, Dict, List, Tuple

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# Security
ACCESS_PASSWORD = "BK8VIP2026"

# Short.io API Configuration
SHORTIO_API_KEY = "sk_F72LsjNnFX8DvHcD"
SHORTIO_DOMAIN = "vipcontact-us.short.gy"
SHORTIO_API_URL = "https://api.short.io/links"

# Default Manager Settings
DEFAULT_MANAGER_ID = "max_bkio"
DEFAULT_MANAGER_NAME = "Max"

# Language Templates
LANGUAGE_TEMPLATES: Dict[str, Dict[str, str]] = {
    "EN": {
        "name": "English",
        "template": "Hello {manager_name}, I need your assistance. My username is {username}."
    },
    "CN": {
        "name": "中文",
        "template": "你好 {manager_name}，我需要你的帮助，我的用户名是 {username}。"
    },
    "JP": {
        "name": "日本語",
        "template": "こんにちは {manager_name}、助けが必要です。私のユーザー名は {username} です。"
    },
    "KH": {
        "name": "ភាសាខ្មែរ",
        "template": "សួស្តី {manager_name} ខ្ញុំត្រូវការជំនួយរបស់អ្នក។ ឈ្មោះអ្នកប្រើប្រាស់របស់ខ្ញុំគឺ {username}。"
    },
    "VN": {
        "name": "Tiếng Việt",
        "template": "Xin chào {manager_name}, tôi cần sự hỗ trợ của bạn. Tên người dùng của tôi là {username}."
    },
    "ID": {
        "name": "Bahasa Indonesia",
        "template": "Halo {manager_name}, saya butuh bantuan Anda. Nama pengguna saya adalah {username}."
    }
}


# ============================================================================
# CUSTOM CSS - GLASSMORPHISM DESIGN SYSTEM
# ============================================================================

def inject_custom_css():
    """Inject premium glassmorphism CSS based on the design system."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --surface: #0b1326;
        --surface-container-low: #131b2e;
        --surface-container-high: #222a3d;
        --surface-container-highest: #2d3449;
        --surface-bright: #3a4259;
        --primary: #4edea3;
        --primary-dim: #3bc48a;
        --on-surface: #dae2fd;
        --on-surface-variant: #c6c6cd;
        --outline-variant: rgba(198, 198, 205, 0.15);
        --tertiary: #4edea3;
        --tertiary-glow: rgba(78, 222, 163, 0.2);
        --tertiary-border: rgba(78, 222, 163, 0.3);
        --error: #ff6b6b;
        --radius-default: 1rem;
        --radius-lg: 1.5rem;
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 1rem;
        --space-4: 1.5rem;
        --space-5: 2rem;
        --space-6: 3rem;
    }
    
    .stApp {
        background: var(--surface) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .glass-panel {
        background: linear-gradient(135deg, var(--surface-container-low) 0%, var(--surface-container-high) 100%);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-4);
        border: 1px solid var(--outline-variant);
    }
    
    .glass-panel-elevated {
        background: linear-gradient(135deg, var(--surface-container-high) 0%, var(--surface-container-highest) 100%);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-4);
        border: 1px solid var(--outline-variant);
        box-shadow: 0 20px 40px rgba(6, 14, 32, 0.4);
    }
    
    .display-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, var(--primary) 0%, var(--on-surface) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .subtitle {
        color: var(--on-surface-variant);
        font-size: 0.875rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: var(--space-5);
    }
    
    .phase-label {
        color: var(--on-surface-variant);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: var(--space-3);
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dim) 100%) !important;
        color: var(--surface) !important;
        border: none !important;
        border-radius: var(--radius-default) !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px var(--tertiary-glow) !important;
    }
    
    .result-counter {
        font-size: 4rem;
        font-weight: 700;
        color: var(--primary);
        letter-spacing: -0.04em;
    }
    
    .stat-chip {
        background: var(--surface-container-highest);
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-default);
        font-size: 0.875rem;
        color: var(--on-surface-variant);
    }
    
    .security-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-1);
        background: var(--surface-container-highest);
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-default);
        font-size: 0.75rem;
        color: var(--on-surface-variant);
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def find_username_column(df: pd.DataFrame) -> Optional[str]:
    for col in df.columns:
        if 'username' in col.lower():
            return col
    return None

def generate_telegram_message(username: str, manager_name: str, language_code: str) -> str:
    template = LANGUAGE_TEMPLATES.get(language_code, LANGUAGE_TEMPLATES["EN"])["template"]
    return template.format(manager_name=manager_name, username=username)

def create_telegram_deeplink(manager_id: str, message: str) -> str:
    """
    FIXED: Returns a pure URL string. 
    Removing Markdown brackets to avoid Short.io API 400 Errors.
    """
    encoded_message = urllib.parse.quote(message, safe='')
    return f"https://t.me/{manager_id}?text={encoded_message}"

def shorten_url(long_url: str) -> Tuple[Optional[str], Optional[str]]:
    headers = {
        "Authorization": SHORTIO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "domain": SHORTIO_DOMAIN,
        "originalURL": long_url
    }
    try:
        response = requests.post(SHORTIO_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201]:
            data = response.json()
            return data.get("shortURL"), None
        else:
            return None, f"API Error: {response.status_code}"
    except Exception as e:
        return None, str(e)

def process_usernames(usernames, manager_id, manager_name, language_code, progress_bar, status_text):
    results = []
    total = len(usernames)
    successful, failed = 0, 0
    start_time = time.time()
    
    for idx, username in enumerate(usernames):
        username = str(username).strip()
        if not username or username.lower() == 'nan': continue
        
        message = generate_telegram_message(username, manager_name, language_code)
        long_url = create_telegram_deeplink(manager_id, message)
        short_url, error = shorten_url(long_url)
        
        if short_url:
            successful += 1
            status = "Success"
        else:
            failed += 1
            status = f"Failed: {error}"
            short_url = long_url
        
        results.append({
            "Username": username,
            "Original Link": long_url,
            "Short Link": short_url,
            "Status": status
        })
        
        progress_bar.progress((idx + 1) / total)
        status_text.markdown(f"Processing {idx + 1}/{total}...")
        time.sleep(0.05)
        
    return pd.DataFrame(results), successful, failed, time.time() - start_time

def convert_df_to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Links')
    return output.getvalue()

# ============================================================================
# MAIN APPLICATION flow
# ============================================================================

def main():
    st.set_page_config(page_title="Username Tool", page_icon="🔐", layout="centered")
    inject_custom_css()
    
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    
    # Header
    st.markdown('<div class="display-title">Username Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Secure Bulk Deep-Link Generator</div>', unsafe_allow_html=True)

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pwd = st.text_input("Vault Key", type="password")
            if st.button("Unlock"):
                if pwd == ACCESS_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("Invalid Key")
        return

    # App Logic
    if st.session_state.get('processing_complete'):
        res_df = st.session_state.results_df
        stats = st.session_state.stats
        
        st.markdown('<div class="glass-panel-elevated">', unsafe_allow_html=True)
        st.markdown(f'<div class="result-counter">{stats["successful"]}</div>', unsafe_allow_html=True)
        st.markdown('<p>Links Ready for Distribution</p>', unsafe_allow_html=True)
        
        st.download_button("📥 Export to Excel", convert_df_to_excel(res_df), "links.xlsx", use_container_width=True)
        if st.button("🔄 New Batch"):
            st.session_state.processing_complete = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(res_df)
    else:
        m_id = st.text_input("Telegram ID", value=DEFAULT_MANAGER_ID)
        m_name = st.text_input("Manager Name", value=DEFAULT_MANAGER_NAME)
        lang = st.selectbox("Language", list(LANGUAGE_TEMPLATES.keys()))
        
        file = st.file_uploader("Upload File", type=['csv', 'xlsx'])
        if file:
            df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
            user_col = find_username_column(df)
            if user_col and st.button("🚀 Process Batch"):
                p_bar = st.progress(0)
                s_txt = st.empty()
                res, s, f, t = process_usernames(df[user_col].tolist(), m_id, m_name, lang, p_bar, s_txt)
                st.session_state.results_df = res
                st.session_state.stats = {'successful': s, 'failed': f, 'time': t}
                st.session_state.processing_complete = True
                st.rerun()

if __name__ == "__main__":
    main()
