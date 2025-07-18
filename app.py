import streamlit as st
import google.generativeai as genai
import requests
import os
import time

# Configure the page
st.set_page_config(page_title="Custom Home Design Assistant", page_icon="🏠", layout="wide")

# Initialize the Gemini model using Streamlit secrets
def initialize_model():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Failed to initialize model: {str(e)}")
        st.stop()

# Cache for designs
if 'design_cache' not in st.session_state:
    st.session_state.design_cache = {}

def get_cache_key(style, size, rooms, preferences):
    return f"{style}_{size}_{rooms}_{preferences}"

def generate_design_idea(model, style, size, rooms, preferences=""):
    cache_key = get_cache_key(style, size, rooms, preferences)
    if cache_key in st.session_state.design_cache:
        return st.session_state.design_cache[cache_key]
    
    prompt = f"""Create a detailed custom home design plan with:
    - Style: {style}
    - Size: {size}
    - Rooms: {rooms}
    - Preferences: {preferences or "None"}
    
    Include:
    1. Design concept overview
    2. Layout with room sizes
    3. Furniture recommendations
    4. Materials and finishes
    5. Style-specific tips
    
    Format in Markdown with clear headings."""
    
    try:
        response = model.generate_content(prompt)
        if response.text:
            st.session_state.design_cache[cache_key] = response.text
            return response.text
    except Exception as e:
        st.error(f"Error generating design: {str(e)}")
    
    # Fallback content
    return f"""
    ## {style} Home Design: {size}, {rooms} Bedrooms
    
    **Overview:**
    This {style.lower()} home features {rooms} rooms across {size}.
    
    **Layout:**
    - Open living area
    - {rooms} bedrooms
    - Modern amenities
    
    **Design Tips:**
    - Use natural materials
    - Large windows for light
    - Functional spaces
    
    Note: Custom design unavailable now. Try again later.
    """

def fetch_design_images(style):
    """Fetch images from Unsplash without API key"""
    try:
        # Predefined curated images for common styles
        style_images = {
            "modern": [
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
                "https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6"
            ],
            "rustic": [
                "https://images.unsplash.com/photo-1600121848594-d8644e57abab",
                "https://images.unsplash.com/photo-1600566752227-513c65e57d03",
                "https://images.unsplash.com/photo-1600607688969-a5bfcd646154"
            ],
            "traditional": [
                "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d",
                "https://images.unsplash.com/photo-1600566752355-35792bedcfea",
                "https://images.unsplash.com/photo-1600607688969-a5bfcd646154"
            ]
        }
        
        # Find closest matching style
        style_lower = style.lower()
        matched_style = next((s for s in style_images.keys() if s in style_lower), "modern")
        return style_images[matched_style]
    except Exception:
        # Fallback images
        return [
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
            "https://images.unsplash.com/photo-1600566752227-513c65e57d03"
        ]

def main():
    st.title("🏠 AI Home Design Assistant")
    st.markdown("Create personalized home designs instantly")

    # Initialize model (will show error if secrets not configured)
    if 'model' not in st.session_state:
        st.session_state.model = initialize_model()

    # Scenario selection
    scenario = st.radio(
        "Choose your scenario:",
        ["Real Estate Development", "Home Renovation", "Architectural Firm"],
        horizontal=True
    )
    st.markdown("---")

    with st.sidebar:
        st.header("Design Preferences")
        budget = st.selectbox("Budget", ["Economy", "Mid-range", "Luxury"])
        priority = st.radio("Focus", ["Function", "Aesthetics", "Balance"])

    # Input form
    with st.form("design_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            style = st.text_input("Style (e.g., Modern, Rustic)")
            size = st.text_input("Size (e.g., 2000 sq ft)")
        
        with col2:
            rooms = st.text_input("Number of Rooms")
            extras = st.text_area("Special Requirements")
        
        # Amenities selection
        amenities = st.multiselect(
            "Desired Amenities",
            ["Swimming Pool", "Home Office", "Smart Home", "Garden", "Garage", "Gym"]
        )

        submitted = st.form_submit_button("Generate Design")

    # Display results outside the form
    if submitted:
        if not all([style, size, rooms]):
            st.warning("Please complete all required fields")
        else:
            with st.spinner("Creating your design..."):
                preferences = f"Budget: {budget}, Priority: {priority}"
                if extras:
                    preferences += f", Extras: {extras}"
                if amenities:
                    preferences += f", Amenities: {', '.join(amenities)}"
                
                design = generate_design_idea(
                    st.session_state.model,
                    style, size, rooms, preferences
                )
                
                image_urls = fetch_design_images(style)
                
                if design:
                    st.success("Design Generated!")
                    st.markdown("---")
                    
                    # Display in columns
                    col_text, col_img = st.columns([2, 1])
                    
                    with col_text:
                        st.markdown("### Your Design Plan")
                        st.markdown(design, unsafe_allow_html=True)
                    
                    with col_img:
                        st.markdown("### Visual Inspiration")
                        for img_url in image_urls:
                            st.image(img_url + "?auto=format&fit=crop&w=800&q=80", 
                                   use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Download button outside form
                    st.download_button(
                        "Save Design Plan",
                        data=design,
                        file_name=f"{style}_home_design.md",
                        mime="text/markdown"
                    )

if __name__ == "__main__":
    main()
