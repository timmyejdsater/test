import streamlit as st
import json
import geopandas as gpd
from io import StringIO

def main():
    st.title("GeoJSON Property Editor")
    
    # File upload
    uploaded_file = st.file_uploader("Upload GeoJSON file", type=['geojson'])
    
    if uploaded_file:
        # Read GeoJSON
        data = json.load(uploaded_file)
        
        # Display properties
        if data['features']:
            properties = data['features'][0]['properties']
            st.write("Available properties:", list(properties.keys()))
            
            # Select multiple name fields
            name_fields = st.multiselect(
                "Select fields to combine for name",
                options=list(properties.keys()),
                help="Selected fields will be combined with spaces between them"
            )
            
            # Add separator option
            separator = st.text_input("Enter separator between fields", value=" ")
            
            # Update name field in all features
            if name_fields:  # Only process if fields are selected
                for feature in data['features']:
                    # Combine selected fields with the separator
                    combined_name = separator.join(str(feature['properties'].get(field, '')) 
                                                 for field in name_fields)
                    feature['properties']['name'] = combined_name
                
                # Download button
                if st.button("Download Updated GeoJSON"):
                    json_str = json.dumps(data)
                    st.download_button(
                        label="Save GeoJSON",
                        data=json_str,
                        file_name="updated.geojson",
                        mime="application/json"
                    )

if __name__ == "__main__":
    main()