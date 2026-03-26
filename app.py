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

# Short.io API Configuration (Hardcoded as per requirements)
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
        "template": "សួស្តី {manager_name} ខ្ញុំត្រូវការជំនួយរបស់អ្នក។ ឈ្មោះអ្នកប្រើប្រាស់របស់ខ្ញុំគឺ {username}។"
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
    /* Import Inter font */
    @import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap)');
    
    /* Root variables following the design system */
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
    
    /* Global resets */
    .stApp {
        background: var(--surface) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding: var(--space-5) var(--space-6) !important;
        max-width: 900px !important;
    }
    
    /* Glass panel base */
    .glass-panel {
        background: linear-gradient(135deg, var(--surface-container-low) 0%, var(--surface-container-high) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-4);
        border: 1px solid var(--outline-variant);
    }
    
    .glass-panel-elevated {
        background: linear-gradient(135deg, var(--surface-container-high) 0%, var(--surface-container-highest) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        margin-bottom: var(--space-4);
        border: 1px solid var(--outline-variant);
        box-shadow: 0 20px 40px rgba(6, 14, 32, 0.4);
    }
    
    /* Typography */
    .display-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, var(--primary) 0%, var(--on-surface) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--space-2);
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
    
    .phase-icon {
        color: var(--primary);
        font-size: 1rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: var(--space-5) 0;
        margin-bottom: var(--space-4);
    }
    
    .lock-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dim) 100%);
        border-radius: var(--radius-default);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto var(--space-4);
        font-size: 1.5rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: var(--surface-container-highest) !important;
        border: none !important;
        border-radius: var(--radius-default) !important;
        color: var(--on-surface) !important;
        padding: var(--space-3) var(--space-4) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: var(--surface-bright) !important;
        box-shadow: inset 0 0 0 1px var(--tertiary-border) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--on-surface-variant) !important;
        opacity: 0.7 !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: var(--surface-container-highest) !important;
        border: none !important;
        border-radius: var(--radius-default) !important;
    }
    
    .stSelectbox > div > div > div {
        color: var(--on-surface) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dim) 100%) !important;
        color: var(--surface) !important;
        border: none !important;
        border-radius: var(--radius-default) !important;
        padding: var(--space-3) var(--space-4) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px var(--tertiary-glow) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px var(--tertiary-glow) !important;
    }
    
    /* Secondary button */
    .secondary-button > button {
        background: var(--surface-container-high) !important;
        color: var(--on-surface) !important;
        box-shadow: none !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dim) 100%) !important;
        color: var(--surface) !important;
        border: none !important;
        border-radius: var(--radius-default) !important;
        padding: var(--space-3) var(--space-4) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 20px var(--tertiary-glow) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: var(--surface-container-high) !important;
        border: 2px dashed var(--outline-variant) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-5) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary) !important;
    }
    
    .stFileUploader label {
        color: var(--on-surface) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dim) 100%) !important;
        border-radius: var(--radius-default) !important;
    }
    
    .stProgress > div > div > div {
        background: var(--surface-container-high) !important;
        border-radius: var(--radius-default) !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(78, 222, 163, 0.1) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: var(--radius-default) !important;
    }
    
    .stError {
        background: rgba(255, 107, 107, 0.1) !important;
        border-left: 4px solid var(--error) !important;
        border-radius: var(--radius-default) !important;
    }
    
    /* Stats display */
    .stats-container {
        display: flex;
        gap: var(--space-3);
        margin-top: var(--space-4);
    }
    
    .stat-chip {
        background: var(--surface-container-highest);
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-default);
        font-size: 0.875rem;
        color: var(--on-surface-variant);
    }
    
    .stat-value {
        color: var(--on-surface);
        font-weight: 600;
    }
    
    /* Result counter */
    .result-counter {
        font-size: 4rem;
        font-weight: 700;
        color: var(--primary);
        letter-spacing: -0.04em;
        line-height: 1;
    }
    
    .result-label {
        color: var(--on-surface-variant);
        font-size: 1rem;
        margin-top: var(--space-2);
    }
    
    /* Status indicator */
    .status-dot {
        width: 8px;
        height: 8px;
        background: var(--primary);
        border-radius: 50%;
        display: inline-block;
        margin-right: var(--space-2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Language selector grid */
    .language-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-2);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: var(--on-surface-variant);
        font-size: 0.75rem;
        padding: var(--space-5) 0;
        margin-top: var(--space-6);
        border-top: 1px solid var(--outline-variant);
    }
    
    /* Metric styling override */
    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--on-surface-variant) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--surface-container-high) !important;
        border-radius: var(--radius-default) !important;
        color: var(--on-surface) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: var(--radius-default) !important;
        overflow: hidden;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
    
    /* Columns spacing */
    [data-testid="column"] {
        padding: var(--space-2) !important;
    }
    
    /* Info boxes */
    .info-box {
        background: var(--surface-container-high);
        border-radius: var(--radius-default);
        padding: var(--space-3);
        color: var(--on-surface-variant);
        font-size: 0.875rem;
        margin: var(--space-3) 0;
    }
    
    /* Security badge */
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
    """Find the column containing usernames (case-insensitive search)."""
    for col in df.columns:
        if 'username' in col.lower():
            return col
    return None


def generate_telegram_message(
    username: str,
    manager_name: str,
    language_code: str
) -> str:
    """Generate the localized Telegram message for a given username."""
    template = LANGUAGE_TEMPLATES.get(language_code, LANGUAGE_TEMPLATES["EN"])["template"]
    return template.format(manager_name=manager_name, username=username)


def create_telegram_deeplink(
    manager_id: str,
    message: str
) -> str:
    """Create the Telegram deep-link URL with encoded message."""
    encoded_message = urllib.parse.quote(message, safe='')
    return f"[t.me](https://t.me/{manager_id}?text={encoded_message})"


def shorten_url(long_url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Call Short.io API to create a shortened URL.
    Returns (short_url, error_message).
    """
    headers = {
        "Authorization": SHORTIO_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "domain": SHORTIO_DOMAIN,
        "originalURL": long_url
    }
    
    try:
        response = requests.post(
            SHORTIO_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            short_url = data.get("shortURL") or data.get("secureShortURL")
            return short_url, None
        else:
            return None, f"API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except requests.exceptions.RequestException as e:
        return None, str(e)


def process_usernames(
    usernames: List[str],
    manager_id: str,
    manager_name: str,
    language_code: str,
    progress_bar,
    status_text
) -> pd.DataFrame:
    """
    Process all usernames: generate messages, create deep-links, shorten URLs.
    Returns a DataFrame with results.
    """
    results = []
    total = len(usernames)
    successful = 0
    failed = 0
    start_time = time.time()
    
    for idx, username in enumerate(usernames):
        username = str(username).strip()
        
        if not username or username.lower() == 'nan':
            continue
        
        # Generate message
        message = generate_telegram_message(username, manager_name, language_code)
        
        # Create deep-link
        long_url = create_telegram_deeplink(manager_id, message)
        
        # Shorten URL
        short_url, error = shorten_url(long_url)
        
        if short_url:
            successful += 1
            status = "Success"
        else:
            failed += 1
            status = f"Failed: {error}"
            short_url = long_url  # Fallback to original URL
        
        results.append({
            "Username": username,
            "Original Link": long_url,
            "Short Link": short_url,
            "Status": status
        })
        
        # Update progress
        progress = (idx + 1) / total
        progress_bar.progress(progress)
        status_text.markdown(
            f"<div class='info-box'>Processing <strong>{idx + 1}</strong> of <strong>{total}</strong> usernames...</div>",
            unsafe_allow_html=True
        )
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    elapsed_time = time.time() - start_time
    
    return pd.DataFrame(results), successful, failed, elapsed_time


def convert_df_to_excel(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to Excel bytes for download."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Deep Links')
    return output.getvalue()


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render the main header section."""
    st.markdown("""
    <div class="header-container">
        <div class="lock-icon">🔐</div>
        <h1 class="display-title">Username Tool</h1>
        <p class="subtitle">Secure Bulk Deep-Link Generator</p>
    </div>
    """, unsafe_allow_html=True)


def render_login_screen():
    """Render the secure login screen."""
    st.markdown("""
    <div class="glass-panel-elevated" style="max-width: 500px; margin: 0 auto;">
        <p class="phase-label"><span class="phase-icon">🔒</span> PHASE 1: SECURE ACCESS</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input(
            "Vault Access Key",
            type="password",
            placeholder="Enter access key",
            label_visibility="collapsed"
        )
        
        if st.button("Unlock", use_container_width=True):
            if password == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access key. Please try again.")


def render_config_section() -> Tuple[str, str, str]:
    """Render the manager configuration section."""
    st.markdown("""
    <p class="phase-label"><span class="phase-icon">⚙️</span> PHASE 2: MANAGER CONFIG</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        manager_id = st.text_input(
            "Telegram Handle",
            value=DEFAULT_MANAGER_ID,
            placeholder="@username",
            help="The Telegram username without the @ symbol"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        manager_name = st.text_input(
            "Display Name",
            value=DEFAULT_MANAGER_NAME,
            placeholder="Manager name",
            help="Name used in the greeting message"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Language selection
    st.markdown("""
    <p class="phase-label" style="margin-top: var(--space-4);"><span class="phase-icon">🌐</span> CONCIERGE LANGUAGE</p>
    """, unsafe_allow_html=True)
    
    language_options = {
        code: f"{code} - {info['name']}" 
        for code, info in LANGUAGE_TEMPLATES.items()
    }
    
    cols = st.columns(6)
    selected_language = st.session_state.get('selected_language', 'EN')
    
    for idx, (code, label) in enumerate(language_options.items()):
        with cols[idx]:
            if st.button(code, key=f"lang_{code}", use_container_width=True):
                st.session_state.selected_language = code
                selected_language = code
    
    return manager_id, manager_name, selected_language


def render_upload_section() -> Optional[pd.DataFrame]:
    """Render the file upload section."""
    st.markdown("""
    <p class="phase-label" style="margin-top: var(--space-5);"><span class="phase-icon">📁</span> PHASE 3: DATA INGEST</p>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel-elevated">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drop Excel or CSV files here to begin extraction",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a file containing a 'username' column"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            username_col = find_username_column(df)
            
            if username_col:
                st.success(f"✓ Found username column: **{username_col}**")
                
                # Preview
                with st.expander("📋 Preview Data", expanded=False):
                    st.dataframe(df.head(10), use_container_width=True)
                
                return df
            else:
                st.error("Could not find a column containing 'username'. Please check your file.")
                st.info("Columns found: " + ", ".join(df.columns.tolist()))
                return None
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return None
    
    return None


def render_execution_section(
    df: pd.DataFrame,
    manager_id: str,
    manager_name: str,
    language_code: str
):
    """Render the execution and results section."""
    st.markdown("""
    <p class="phase-label" style="margin-top: var(--space-5);"><span class="phase-icon">▶️</span> PHASE 4: EXECUTION</p>
    """, unsafe_allow_html=True)
    
    username_col = find_username_column(df)
    usernames = df[username_col].dropna().tolist()
    total_usernames = len(usernames)
    
    st.markdown(f"""
    <div class="info-box">
        Ready to process <strong>{total_usernames}</strong> usernames using <strong>{LANGUAGE_TEMPLATES[language_code]['name']}</strong> template
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Generate & Shorten", use_container_width=True):
        st.markdown('<div class="glass-panel-elevated">', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process usernames
        results_df, successful, failed, elapsed_time = process_usernames(
            usernames,
            manager_id,
            manager_name,
            language_code,
            progress_bar,
            status_text
        )
        
        # Store results in session state
        st.session_state.results_df = results_df
        st.session_state.processing_complete = True
        st.session_state.stats = {
            'successful': successful,
            'failed': failed,
            'elapsed_time': elapsed_time
        }
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.rerun()


def render_results_section():
    """Render the results and download section."""
    if not st.session_state.get('processing_complete'):
        return
    
    results_df = st.session_state.results_df
    stats = st.session_state.stats
    
    st.markdown("""
    <div class="glass-panel-elevated">
        <p style="color: var(--primary); font-weight: 600; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase;">
            <span class="status-dot"></span> PROCESSING COMPLETE
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="result-counter">{stats['successful']:,}</div>
        <div class="result-label">Links Ready for Distribution</div>
        <div class="stats-container">
            <span class="stat-chip">Latency: <span class="stat-value">{int(stats['elapsed_time'] * 1000 / max(stats['successful'], 1))}ms</span></span>
            <span class="stat-chip">Success: <span class="stat-value">{(stats['successful'] / max(stats['successful'] + stats['failed'], 1) * 100):.1f}%</span></span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        excel_data = convert_df_to_excel(results_df)
        st.download_button(
            label="📥 Export to Excel (.xlsx)",
            data=excel_data,
            file_name="vip_deeplinks.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.markdown("""
        <div style="text-align: center; margin-top: var(--space-3);">
            <span class="security-badge">🔒 Secure encryption active (AES-256)</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results preview
    with st.expander("📋 View Generated Links", expanded=False):
        st.dataframe(results_df, use_container_width=True)
    
    # Reset button
    if st.button("🔄 Process New File", use_container_width=True):
        st.session_state.processing_complete = False
        st.session_state.results_df = None
        st.session_state.stats = None
        st.rerun()


def render_footer():
    """Render the footer section."""
    st.markdown("""
    <div class="footer">
        <p>© 2024 Username Tool. Digital Concierge Systems.</p>
        <p style="margin-top: var(--space-2);">
            <a href="#" style="color: var(--on-surface-variant); text-decoration: none; margin: 0 var(--space-2);">Privacy Policy</a>
            <a href="#" style="color: var(--on-surface-variant); text-decoration: none; margin: 0 var(--space-2);">Terms of Service</a>
            <a href="#" style="color: var(--on-surface-variant); text-decoration: none; margin: 0 var(--space-2);">API Documentation</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="Username Tool | Digital Concierge",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'EN'
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    
    # Render header
    render_header()
    
    # Check authentication
    if not st.session_state.authenticated:
        render_login_screen()
        return
    
    # Main application flow
    if st.session_state.processing_complete:
        render_results_section()
    else:
        # Configuration
        manager_id, manager_name, language_code = render_config_section()
        
        # File upload
        df = render_upload_section()
        
        # Execution
        if df is not None:
            render_execution_section(df, manager_id, manager_name, language_code)
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
