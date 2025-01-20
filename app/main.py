import streamlit as st
from ..services.mock_music_service import MockMusicService
from ..services.mistral_service import MistralService
from app.config import MOOD_OPTIONS, ACTIVITY_OPTIONS, THERAPEUTIC_GOALS

class MusicTherapyApp:
    def __init__(self):
        self.music_service = MockMusicService()
        self.mistral_service = MistralService()
        
    def run(self):
        st.set_page_config(
            page_title="AI Music Therapy",
            page_icon="🎵",
            layout="wide"
        )
        
        st.title("🎵 AI-Powered Music Therapy")
        st.markdown("""
        Welcome to your personalized music therapy session. This platform uses AI 
        to create therapeutic music experiences tailored to your emotional needs.
        """)
        
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("How are you feeling?")
            mood = st.selectbox("Select your current mood:", MOOD_OPTIONS)
            activity = st.selectbox("What are you doing?", ACTIVITY_OPTIONS)
        
        with col2:
            st.subheader("Therapeutic Goals")
            goals = st.multiselect(
                "What would you like to achieve?",
                THERAPEUTIC_GOALS,
                default=["Stress Reduction"]
            )
        
        if st.button("Generate Therapeutic Playlist", type="primary"):
            with st.spinner("Creating your personalized therapeutic experience..."):
                
                songs = self.music_service.get_therapeutic_music(
                    mood=mood,
                    activity=activity,
                    goals=goals
                )
                
                if not songs:
                    st.error("Unable to generate recommendations at the moment. Please try again.")
                    return
                
            
                therapeutic_context = self.mistral_service.get_therapeutic_context(
                    mood=mood,
                    activity=activity,
                    songs=songs
                )
                
                
                st.success("Your therapeutic playlist is ready!")
                
                
                st.subheader("💭 Therapeutic Context")
                st.write(therapeutic_context)
                
                
                st.subheader("🎵 Your Playlist")
                for i, song in enumerate(songs, 1):
                    with st.expander(f"{i}. {song['title']} by {song['artist']}"):
                        st.write(f"Therapeutic Score: {song['therapeutic_score']:.2f}")
                        mindfulness_prompt = self.mistral_service.get_mindfulness_prompt(
                            song=song,
                            mood=mood
                        )
                        st.info("🧘‍♀️ Mindfulness Prompt", icon="🎵")
                        st.write(mindfulness_prompt)
                
            
                st.subheader("✨ Feedback")
                with st.form("feedback_form"):
                    rating = st.slider(
                        "How helpful was this playlist?",
                        min_value=1,
                        max_value=5,
                        value=3
                    )
                    feedback_text = st.text_area(
                        "Any additional feedback? (optional)"
                    )
                    submitted = st.form_submit_button("Submit Feedback")
                    
                    if submitted:
                        st.success("Thank you for your feedback! This helps us improve your future recommendations.")

if __name__ == "__main__":
    app = MusicTherapyApp()
    app.run()