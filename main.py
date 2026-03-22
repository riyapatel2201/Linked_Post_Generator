import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Informative", 
    "Inspirational", 
    "Celebratory", 
    "Promotional", 
    "Reflective", 
    "Conversational", 
    "Professional", 
    "Casual", 
    "Humorous", 
    "Friendly"
]
emoji_level_options = ["None", "Low", "Medium", "High"]
formality_options = ["Very formal", "Business casual", "Conversational", "Casual"]
writing_style_options = ["Concise", "Detailed", "Data-driven", "Story-based", "Experience-sharing"]
formatting_options = ["Bold key points", "Use bullet points", "Include quotations", "Add statistics"]
industry_focus_options = ["Technology", "Marketing", "Finance", "Healthcare", "Education", "Human Resources", 
                         "Non-profit", "Manufacturing", "Retail", "Consulting", "Legal", "Real Estate"]
target_audience_options = ["Entry-level", "Mid-career", "Executives", "Recruiters", "Job seekers", 
                          "Industry peers", "Clients", "General audience"]

def main():
    st.title("🔧 LinkedIn Content Creator Tool")
    
    fs = FewShotPosts()
    tags = fs.get_tags()
    
    st.markdown("### 🧠 Choose a topic or enter your own")
    
    tag_input_method = st.radio(
        "How would you like to select the topic?",
        options=["Choose from suggestions", "Enter custom topic"],
        horizontal=True
    )
    
    if tag_input_method == "Choose from suggestions":
        selected_tag = st.selectbox("Select a predefined topic", options=tags)
    else:
        selected_tag = st.text_input("Enter your custom topic", placeholder="e.g., AI in Education")
    
    st.markdown("### 📐 Post Configuration")
    col1, col2 = st.columns(2)
    with col1:
        selected_length = st.selectbox("Length", options=length_options)
    with col2:
        selected_language = st.selectbox("Language", options=language_options)
    
    st.markdown("### 🧩 Optional Enhancements")
    
    # Create tabs for better organization of the many options
    tabs = st.tabs(["Tone & Style", "Format & Content", "Audience & Industry", "Engagement"])
    
    # Tab 1: Tone & Style
    with tabs[0]:
        # Tone selection (choose or enter)
        tone_enabled = st.checkbox("Choose tone & intent")
        if tone_enabled:
            tone_input_method = st.radio(
                "How would you like to set the tone?",
                options=["Choose from suggestions", "Enter your own tone"],
                horizontal=True
            )
            
            if tone_input_method == "Choose from suggestions":
                tone = st.selectbox("Select tone/intent", options=tone_options)
            else:
                tone = st.text_input("Enter your custom tone", placeholder="e.g., Friendly, Motivational, Bold")
        else:
            tone = None
        
        # Formality Level
        formality_enabled = st.checkbox("Set formality level")
        if formality_enabled:
            formality = st.select_slider(
                "Formality",
                options=formality_options,
                value="Business casual"
            )
        else:
            formality = None
        
        # Writing Style
        writing_style_enabled = st.checkbox("Select writing style")
        if writing_style_enabled:
            writing_style = st.selectbox("Writing style", options=writing_style_options)
        else:
            writing_style = None
        
        # Creativity control
        creativity_enabled = st.checkbox("Control creativity level")
        if creativity_enabled:
            creativity = st.slider("Creativity (0 = focused, 1 = creative)", 0.2, 1.0, 0.7)
        else:
            creativity = None
    
    # Tab 2: Format & Content
    with tabs[1]:
        # Formatting Elements
        formatting_enabled = st.checkbox("Add formatting elements")
        if formatting_enabled:
            formatting_elements = st.multiselect(
                "Select formatting elements to include",
                options=formatting_options
            )
        else:
            formatting_elements = None
        
        # Emoji control
        emoji_enabled = st.checkbox("Add emojis to post")
        if emoji_enabled:
            emoji_level = st.select_slider(
                "Emoji level",
                options=emoji_level_options,
                value="Low",
                help="None = no emojis, Low = few emojis, Medium = moderate emojis, High = many emojis"
            )
        else:
            emoji_level = "None"
    
    # Tab 3: Audience & Industry
    with tabs[2]:
        # Industry Focus
        industry_focus_enabled = st.checkbox("Specify industry focus")
        if industry_focus_enabled:
            industry_focus = st.selectbox("Select industry", options=industry_focus_options)
        else:
            industry_focus = None
        
        # Target Audience
        target_audience_enabled = st.checkbox("Define target audience")
        if target_audience_enabled:
            target_audience = st.selectbox("Select primary audience", options=target_audience_options)
        else:
            target_audience = None
    
    # Tab 4: Engagement
    with tabs[3]:
        # Hashtag enhancements
        hashtags_enabled = st.checkbox("Add or generate hashtags")
        if hashtags_enabled:
            hashtag_mode = st.radio("How would you like to handle hashtags?", ["Add manually", "Auto-generate"])
            if hashtag_mode == "Add manually":
                custom_hashtags = st.text_input("Enter hashtags (comma or space-separated)", placeholder="#AI #Leadership")
            else:
                custom_hashtags = "AUTO"
        else:
            custom_hashtags = None
    
    # Generate button (outside tabs, always visible)
    st.markdown("### 🚀 Generate Your Post")
    if st.button("Generate LinkedIn Post"):
        if selected_tag.strip():
            post = generate_post(
                length=selected_length,
                language=selected_language,
                tag=selected_tag,
                tone=tone,
                creativity=creativity,
                hashtags=custom_hashtags,
                emoji_level=emoji_level,
                formality=formality,
                writing_style=writing_style,
                formatting_elements=formatting_elements,
                industry_focus=industry_focus,
                target_audience=target_audience
            )
            st.success("✅ Post generated successfully!")
            st.markdown("### 📝 Your LinkedIn Post")
            
            st.text_area(
                "Generated Post",
                value=post,
                height=300,
                help="Click and press Ctrl+A to select all, then Ctrl+C to copy",
                key="generated_post"
            )
        else:
            st.error("⚠️ Please provide a valid topic.")

if __name__ == "__main__":
    main()