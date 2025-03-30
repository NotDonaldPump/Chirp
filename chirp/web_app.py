import streamlit as st
import redis
from datetime import datetime
from redis_model import *

# Importer les fonctions Redis fournies
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
MAX_TOPS_ITEMS = 5

def main():
    st.title("🕊️ CHIRP - Compact Hub for Instant Real-time Posting")
    
    # Section principale pour afficher les données
    st.header("Live Feed")
    
    # Derniers Chirps
    st.subheader("Latest Chirps")
    chirps = get_chirps()
    if chirps:
        for chirp_content, timestamp in chirps:
            username = chirp_content.split(': ')[0]
            chirp_text = chirp_content.split(': ')[1]
            
            # Récupérer les données utilisateur
            user_data = get_user(username)
            followers = user_data.get('followers', 0)
            following = user_data.get('following', 0)
            chirps_count = user_data.get('chirps', 0)

            # Créer le tooltip HTML
            tooltip = f"""
            <div class="tooltip">
                <span style="border-bottom: 1px dotted #666; cursor: help;">{username}</span>
                <span class="tooltiptext">
                    🐦 {chirps_count} chirps<br>
                    👥 {followers} followers<br>
                    👤 {following} following
                </span>
            </div>
            """

            dt = datetime.fromtimestamp(timestamp / 1000)
            
            # Afficher avec le tooltip
            st.markdown(f"""
            <style>
                .tooltip {{
                    position: relative;
                    display: inline-block;
                }}
                .tooltip .tooltiptext {{
                    visibility: hidden;
                    width: 160px;
                    background-color: #555;
                    color: #fff;
                    text-align: center;
                    border-radius: 6px;
                    padding: 8px;
                    position: absolute;
                    z-index: 1;
                    bottom: 125%;
                    left: 50%;
                    margin-left: -80px;
                    opacity: 0;
                    transition: opacity 0.3s;
                }}
                .tooltip:hover .tooltiptext {{
                    visibility: visible;
                    opacity: 1;
                }}
            </style>{tooltip}** ({dt.strftime('%Y-%m-%d %H:%M:%S')})
            """, unsafe_allow_html=True)
            
            st.write(chirp_text)
            st.divider()
    else:
        st.write("No chirps yet. Be the first to chirp!")
    
    # Statistiques en colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Chirpers
        st.subheader("🏆 Top Chirpers")
        top_chirpers = get_top_chirpers()
        if top_chirpers:
            for i, (user, count) in enumerate(top_chirpers, 1):
                st.write(f"{i}. {user} - {count} chirps")
        else:
            st.write("No chirpers yet")
    
    with col2:
        # Most Followed
        st.subheader("🌟 Most Followed")
        most_followed = get_top_followers()
        if most_followed:
            for i, (user, count) in enumerate(most_followed, 1):
                st.write(f"{i}. {user} - {count} followers")
        else:
            st.write("No followers data yet")

if __name__ == "__main__":
    main()