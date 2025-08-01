import streamlit as st

def show_simple_loading():
    """
    Alternative super simple loading screen if the main one has issues.
    """
    st.markdown("""
    <div style="
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(255,255,255,0.7); z-index: 999999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        font-family: system-ui; text-align: center; pointer-events: all;
        backdrop-filter: blur(2px);
    ">
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg);}
            100% { transform: rotate(360deg);}
        }
        .rotating {
            display: inline-block;
            animation: spin 1.2s linear infinite;
        }
        </style>
        <h1 class="rotating" style="font-size: 40px; margin-bottom: 20px;">📡</h1>
        <h2 style="color: #1f2937; margin-bottom: 20px;">Loading RepeatRadar Demo</h2>
        <p style="color: #6b7280; margin-bottom: 40px;">Preparing cohort analysis tools...</p>
        <div style="padding: 20px; background: #f8fafc; border-radius: 10px; border-left: 4px solid #3b82f6;">
            <h3 style="margin: 0 0 10px 0; color: #1f2937;">👋 Hi, I'm Kristof Menyhert</h3>
            <p style="margin: 0 0 10px 0; color: #6b7280;">Data Scientist</p>
            <p style="margin: 0 0 15px 0; color: #1f2937; font-weight: bold;">💼 Open to Work</p>
            <a href="https://www.linkedin.com/in/kristof-menyhert/" target="_blank" 
               style="color: #3b82f6; text-decoration: none; font-weight: 500;">
               Let's connect on LinkedIn →
            </a>
            <p style="margin-top: 10px; color: #3b82f6; font-size: 14px;">
                📧 menyhert.kristof@gmail.com
            </p>
        </div>
        <p style="margin-top: 30px; color: #9ca3af; font-size: 14px;">
            This may take up to 1 minute
            <span id="countdown" style="margin-left:10px; color:#3b82f6;"></span>
        </p>
        <p style="margin-top: 5px; color: #6b7280; font-size: 15px;">Please wait a bit until the data loads.</p>
        <script>
        let seconds = 60;
        function updateCountdown() {
            let m = Math.floor(seconds / 60);
            let s = seconds % 60;
            document.getElementById('countdown').textContent = `(${m}:${s.toString().padStart(2, '0')})`;
            if (seconds > 0) {
                seconds--;
                setTimeout(updateCountdown, 1000);
            }
        }
        updateCountdown();
        </script>
    </div>
    """, unsafe_allow_html=True)
