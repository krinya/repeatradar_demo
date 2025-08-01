import streamlit as st
from datetime import datetime, timedelta
import time

@st.cache_data(ttl=86400)
def get_cache_timestamp():
    """
    Get the timestamp when data was first cached.
    This helps track when the cache was last refreshed.
    """
    return datetime.now()

@st.cache_data(ttl=86400)
def get_cache_hit_counter():
    """
    Simple counter to track cache hits.
    This increments only when cache is refreshed (every 24 hours).
    """
    return 0

def display_cache_info():
    """
    Display cache information in the sidebar including when data was cached
    and when it will expire.
    """
    try:
        cache_time = get_cache_timestamp()
        expire_time = cache_time + timedelta(hours=24)
        current_time = datetime.now()
        
        time_until_expire = expire_time - current_time
        hours_left = max(0, time_until_expire.total_seconds() / 3600)
        
        with st.sidebar:
            st.markdown("**⏰ Cache Info**")
            st.caption(f"Cached: {cache_time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.caption(f"Expires in: {hours_left:.1f} hours")
            
            if hours_left < 1:
                st.warning("⚠️ Cache expiring soon")
            elif hours_left > 23:
                st.info("🆕 Fresh cache")
            
            # Add performance tip
            st.caption("💡 Cache shared across all users for optimal performance")
            
    except Exception as e:
        st.sidebar.caption("Cache info unavailable")
