import streamlit as st
import os

def get_image_size(file_path):
    """Get the size of an image in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def read_image(file_path):
    """Read an image file."""
    with open(file_path, 'rb') as f:
        return f.read()

def write_image(file_path, data):
    """Write data to an image file."""
    with open(file_path, 'wb') as f:
        f.write(data)

def simulate_compression(image_data, quality):
    """Simulate compression by truncating the data."""
    truncated_length = int(len(image_data) * (quality / 100))
    return image_data[:truncated_length]

def optimize_image(image_data, quality):
    """Optimize the image by simulating compression."""
    return simulate_compression(image_data, quality)

def main():
    # Set up page
    st.set_page_config(layout='centered')
    st.markdown("""
        <style>
        body { background-color: #f0f8ff; }
        h1, h2, h3, h4, h5, h6 { color: #4CAF50; }
        </style>
        """, unsafe_allow_html=True)

    st.title("Image Compression Tool")
    st.subheader("Effortlessly optimize your image sizes without compromising too much on quality.")
    
    st.write("---")

    # Upload Section
    st.write("### Upload your image")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        original_size = get_image_size(temp_file_path)
        st.write(f"#### Original Image Size: **{original_size:.2f} MB**")
        st.image(temp_file_path, caption="Original Image", use_column_width=True)
        st.write("---")

        if original_size > 2:
            st.warning("Image is larger than 2MB. Consider optimizing it.")
            st.write("### Select Quality Levels for Compression")

            qualities = [75, 50, 25]
            optimized_results = {}

            # Process compression for different quality levels
            for quality in qualities:
                original_data = read_image(temp_file_path)
                optimized_data = optimize_image(original_data, quality)

                optimized_results[quality] = {
                    "size": len(optimized_data) / (1024 * 1024),
                    "data": optimized_data,
                }

                st.write(f"- **{quality}% Quality**: Simulated Size: {optimized_results[quality]['size']:.2f} MB")

            # User choice of quality
            chosen_quality = st.radio("Select a quality level for download:", qualities, index=0)

            if chosen_quality:
                chosen_result = optimized_results[chosen_quality]
                st.success(f"You selected {chosen_quality}% Quality. Simulated Size: {chosen_result['size']:.2f} MB")

                # Download button for chosen quality
                st.download_button(
                    label=f"Download {chosen_quality}% Quality Image",
                    data=chosen_result['data'],
                    file_name=f"optimized_{chosen_quality}_{uploaded_file.name}",
                    mime="image/jpeg",
                )

        else:
            st.success("Image size is already under 2MB. Optimization not required.")
            st.write("Feel free to download the original image if needed.")

    else:
        st.info("Upload an image file to begin the optimization process.")

if __name__ == "__main__":
    main()
