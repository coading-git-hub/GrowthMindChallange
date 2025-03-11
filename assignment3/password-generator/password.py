import streamlit as st
import random
import string
import re
import pyperclip

def check_password_strength(password):
    score = 0
    messages = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        messages.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        messages.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        messages.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        messages.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", messages, "success"
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", messages, "warning"
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", messages, "error"

def generate_password(length, use_digits, use_special_chars):
    charactors = string.ascii_letters

    if use_digits:
        charactors += string.digits

    if use_special_chars:
        charactors += string.punctuation

    return ''.join(random.choice(charactors) for _ in range(length))

st.set_page_config(
    page_title="Password Generator",
    page_icon="🔐",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        border-radius: 10px;
        background: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Password Generator")
st.markdown("### Create strong and secure passwords instantly!")

with st.container():
    # Password Strength Checker Section
    st.markdown("### 💪 Check Password Strength")
    st.markdown("Enter your password to check how strong it is:")
    
    password_to_check = st.text_input(
        "Enter password:", 
        value=st.session_state.get('generated_password', ''),
        type="password",
        key="password_input"
    )
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🔍 Check Strength", key="check_button"):
            if password_to_check:
                result, messages, status = check_password_strength(password_to_check)
                if status == "success":
                    st.success(result)
                elif status == "warning":
                    st.warning(result)
                else:
                    st.error(result)
                
                if messages:
                    for msg in messages:
                        st.markdown(msg)
            else:
                st.error("Please enter a password to check!")

    st.markdown("---")

    # Password Generator Section
    st.markdown("### 🎲 Generate New Password")
    st.markdown("Create a strong password with your preferred settings:")
    
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("Password Length 📏", min_value=6, max_value=32, value=12)
    
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        use_digits = st.checkbox("Include Digits (0-9)")
    with subcol2:
        use_special_chars = st.checkbox("Include Special Characters (!@#$)")

    if st.button("Generate Password", type="primary"):
        generated_password = generate_password(length, use_digits, use_special_chars)
        st.session_state.generated_password = generated_password
        
        # Display password with copy button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code(generated_password, language=None)
        with col2:
            st.button("📋 Copy", key="copy_button", on_click=lambda: st.write("Password copied to clipboard!"))
            
        # Add copy functionality using pyperclip
        pyperclip.copy(generated_password)
        
        # Show success message
        st.success("Password generated and copied to clipboard!")
        
        # Automatically check strength of generated password
        result, messages, status = check_password_strength(generated_password)
        if status == "success":
            st.success(result)
        elif status == "warning":
            st.warning(result)
        else:
            st.error(result)

# Update JavaScript for better copy functionality and animations
st.markdown("""
    <script>
        function copyPassword() {
            const passwordText = document.getElementById('password-display').textContent.trim();
            const button = document.getElementById('copyButton');
            
            navigator.clipboard.writeText(passwordText).then(function() {
                // Visual feedback for successful copy
                button.classList.add('copied');
                button.innerHTML = '✅ Copied! (Ctrl+V to paste)';
                
                // Add temporary tooltip or message
                const tooltip = document.createElement('div');
                tooltip.style.position = 'absolute';
                tooltip.style.background = '#333';
                tooltip.style.color = 'white';
                tooltip.style.padding = '5px 10px';
                tooltip.style.borderRadius = '4px';
                tooltip.style.fontSize = '12px';
                tooltip.style.top = (button.offsetTop - 30) + 'px';
                tooltip.style.left = button.offsetLeft + 'px';
                tooltip.innerHTML = 'Password copied! Use Ctrl+V to paste';
                document.body.appendChild(tooltip);
                
                // Remove effects after animation
                setTimeout(() => {
                    button.classList.remove('copied');
                    button.innerHTML = '📋 Copy';
                    tooltip.remove();
                }, 2000);
                
            }).catch(function(err) {
                console.error('Failed to copy text: ', err);
                button.innerHTML = '❌ Error!';
                setTimeout(() => {
                    button.innerHTML = '📋 Copy';
                }, 2000);
            });
        }
    </script>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        Built with 💖 by <a href='https://github.com/KIRANAHMED'>Kiran Ahmed</a>
    </div>
    """, 
    unsafe_allow_html=True
)
    