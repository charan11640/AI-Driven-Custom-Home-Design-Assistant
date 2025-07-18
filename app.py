import streamlit as st
import google.generativeai as genai
import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="Custom Home Design Assistant", page_icon="🏠", layout="wide")

# Initialize the Gemini model
def initialize_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # Using the current recommended model
    return genai.GenerativeModel('gemini-1.5-flash')

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

def fetch_design_image(style):
    # Curated Unsplash images for common styles
    style_images = {
        "Modern": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=800&q=80",
        "Rustic": "https://images.unsplash.com/photo-1460518451285-97b6aa326961?auto=format&fit=crop&w=800&q=80",
        "Traditional": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=800&q=80",
        "Minimalist": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=800&q=80",
        "Luxury": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80",
        # Add more styles as needed
    }
    # Try to match style (case-insensitive)
    for key in style_images:
        if key.lower() in style.lower():
            return style_images[key]
    # Default fallback image
    return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"

# Fetch multiple images from Unsplash API based on user input

def fetch_unsplash_images(query, num_images=3):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        st.warning("Unsplash Access Key not found. Please set the UNSPLASH_ACCESS_KEY environment variable.")
        return []
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": num_images,
        "orientation": "landscape",
        "client_id": access_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "results" in data:
            return [img["urls"]["regular"] for img in data["results"]]
        else:
            return []
    except Exception as e:
        st.warning(f"Error fetching images: {str(e)}")
        return []

def main():
    st.title("🏠 AI Home Design Assistant")
    st.markdown("Create personalized home designs instantly")

    # Scenario selection
    scenario = st.radio(
        "Choose your scenario:",
        ["Real Estate Development", "Home Renovation", "Architectural Firm"],
        horizontal=True
    )
    st.markdown("---")

    if 'model' not in st.session_state:
        st.session_state.model = initialize_model()

    with st.sidebar:
        st.header("Design Preferences")
        budget = st.selectbox("Budget", ["Economy", "Mid-range", "Luxury"])
        priority = st.radio("Focus", ["Function", "Aesthetics", "Balance"])

    # Room-by-room customization state
    room_types = ["Bedroom", "Bathroom", "Kitchen", "Living Room", "Dining Room", "Office", "Garage", "Other"]
    if 'room_details' not in st.session_state:
        st.session_state.room_details = []
    if 'remove_room_flags' not in st.session_state:
        st.session_state.remove_room_flags = []

    # Add Room button (outside the form)
    if st.button("Add Room"):
        st.session_state.room_details.append({"type": "Bedroom", "size": "", "style": "", "features": ""})
        st.session_state.remove_room_flags.append(False)

    # Input form
    with st.form("design_form"):
        col1, col2 = st.columns(2)
        with col1:
            style = st.text_input("Style (e.g., Modern, Rustic)", key="style_input")
            size = st.text_input("Size (e.g., 2000 sq ft)", key="size_input")
        with col2:
            rooms = st.text_input("Number of Rooms", key="rooms_input")
            extras = st.text_area("Special Requirements", key="extras_input")

        # Amenities for all scenarios
        st.markdown("#### Select Desired Amenities")
        amenities = st.multiselect(
            "Amenities", ["Swimming Pool", "Home Office", "Smart Home", "Garden", "Garage", "Gym", "Theater Room", "Solar Panels"]
        )

        # Room-by-room customization
        st.markdown("#### Room-by-Room Customization")
        for idx, room in enumerate(st.session_state.room_details):
            with st.expander(f"Room {idx+1}: {room['type']}"):
                room_type = st.selectbox(f"Type", room_types, index=room_types.index(room["type"]) if room["type"] in room_types else 0, key=f"room_type_{idx}")
                room_size = st.text_input("Size (e.g., 12x14 ft)", value=room["size"], key=f"room_size_{idx}")
                room_style = st.text_input("Style (e.g., Modern, Cozy)", value=room["style"], key=f"room_style_{idx}")
                room_features = st.text_area("Special Features", value=room["features"], key=f"room_features_{idx}")
                remove_flag = st.checkbox("Remove this room", key=f"remove_room_{idx}")
                # Update session state
                st.session_state.room_details[idx] = {
                    "type": room_type,
                    "size": room_size,
                    "style": room_style,
                    "features": room_features
                }
                st.session_state.remove_room_flags[idx] = remove_flag

        # Scenario-specific fields
        uploaded_plan = None
        advanced_layout = None
        if scenario == "Home Renovation":
            st.markdown("#### Upload Current Floor Plan (optional)")
            uploaded_plan = st.file_uploader("Upload Floor Plan (image or PDF)", type=["png", "jpg", "jpeg", "pdf"])
        elif scenario == "Architectural Firm":
            st.markdown("#### Advanced Layout Options")
            advanced_layout = st.text_area("Describe any advanced layout or zoning requirements")

        submitted = st.form_submit_button("Generate Design")

    # Remove rooms flagged for removal after form submit
    if submitted:
        # Remove rooms in reverse order to avoid index issues
        for idx in reversed(range(len(st.session_state.remove_room_flags))):
            if st.session_state.remove_room_flags[idx]:
                st.session_state.room_details.pop(idx)
                st.session_state.remove_room_flags.pop(idx)

    # Display results outside the form
    if submitted:
        if not all([style, size, rooms]):
            st.warning("Please complete all required fields")
        else:
            with st.spinner("Creating your design..."):
                # Build room details string
                room_details_str = "\n".join([
                    f"- {r['type']}: Size {r['size']}, Style {r['style']}, Features: {r['features']}" for r in st.session_state.room_details
                ])
                preferences = f"Budget: {budget}, Priority: {priority}"
                if extras:
                    preferences += f", Extras: {extras}"
                if amenities:
                    preferences += f", Amenities: {', '.join(amenities)}"
                if advanced_layout:
                    preferences += f", Advanced Layout: {advanced_layout}"
                if room_details_str:
                    preferences += f"\nRoom Details:\n{room_details_str}"
                design = generate_design_idea(
                    st.session_state.model,
                    style, size, rooms, preferences
                )
                # Build a search query for Unsplash
                image_query = f"{style} house {size} {rooms} rooms {extras} {', '.join(amenities) if amenities else ''} "
                if room_details_str:
                    image_query += room_details_str.replace('\n', ' ')
                image_urls = fetch_unsplash_images(image_query.strip(), num_images=3)
                if design:
                    st.success("Design Generated!")
                    st.markdown("---")
                    col_text, col_img = st.columns([2, 1])
                    with col_text:
                        st.markdown("### Your Design Plan")
                        st.markdown(design, unsafe_allow_html=True)
                        if uploaded_plan is not None:
                            st.markdown("#### Uploaded Floor Plan:")
                            if uploaded_plan.type.startswith("image"):
                                st.image(uploaded_plan, use_container_width=True)
                            elif uploaded_plan.type == "application/pdf":
                                st.info("PDF preview not supported, but file is uploaded.")
                    with col_img:
                        st.markdown("### Visual Inspiration")
                        if image_urls:
                            for img_url in image_urls:
                                st.image(img_url, use_container_width=True)
                        else:
                            st.warning("Couldn't load design images. Showing fallback.")
                            st.image(
                                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
                                use_container_width=True,
                                caption="Fallback Home Example"
                            )
                    st.markdown("---")
                    st.download_button(
                        "Save Design Plan",
                        data=design,
                        file_name=f"{style}_home_design.md",
                        mime="text/markdown",
                        key="download_button"
                    )

if __name__ == "__main__":
    main()