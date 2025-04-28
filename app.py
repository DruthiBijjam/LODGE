# import streamlit as st
# import os
# import tempfile
# import subprocess
# import time
# from pathlib import Path
# import shutil
# import glob

# st.set_page_config(
#     page_title="Long Dance Generation",
#     page_icon="💃",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: 700;
#         color: #1E88E5;
#         text-align: center;
#         margin-bottom: 1rem;
#         text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
#     }
#     .sub-header {
#         font-size: 1.5rem;
#         font-weight: 500;
#         color: #424242;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .stVideo {
#         width: 100%;
#         border-radius: 10px;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
#     .video-title {
#         font-size: 1.2rem;
#         font-weight: 500;
#         margin-top: 0.5rem;
#         text-align: center;
#     }
#     .upload-section {
#         background-color: #f8f9fa;
#         padding: 2rem;
#         border-radius: 10px;
#         margin-bottom: 2rem;
#     }
#     .success-message {
#         padding: 1rem;
#         background-color: #d4edda;
#         color: #155724;
#         border-radius: 5px;
#         margin-bottom: 1rem;
#     }
#     .processing-message {
#         padding: 1rem;
#         background-color: #cce5ff;
#         color: #004085;
#         border-radius: 5px;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header and intro
# st.markdown("<h1 class='main-header'>Long Dance Generation</h1>", unsafe_allow_html=True)
# st.markdown("<p class='sub-header'>Upload motion files and music to generate dance videos</p>", unsafe_allow_html=True)

# # Create temp directories function
# def create_temp_directories():
#     temp_input_dir = tempfile.mkdtemp()
#     temp_output_dir = tempfile.mkdtemp()
#     return temp_input_dir, temp_output_dir

# # Function to run the render.py script
# def run_render_script(motion_dir, output_dir, song_file=None, device="0"):
#     cmd = [
#         "python", 
#         "render.py", 
#         "--modir", motion_dir,
#         "--save_path", output_dir,
#         "--device", device,
#         #"--mode", "smplh",  # Using smplh mode as default
#         "--fps", "30"
#     ]
    
#     if song_file:
#         cmd.extend(["--song", song_file])
    
#     try:
#         process = subprocess.Popen(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             universal_newlines=True
#         )
        
#         # Stream the output
#         for line in process.stdout:
#             st.text(line.strip())
            
#         process.wait()
#         return process.returncode == 0
#     except Exception as e:
#         st.error(f"Error running render script: {e}")
#         return False

# # Main app code
# def main():
#     with st.sidebar:
#         st.image("https://i.imgur.com/4oDh1eH.png", width=100)  # A placeholder dance icon
#         st.header("Settings")
        
#         device = st.selectbox(
#             "GPU Device",
#             options=["0", "1", "2", "3", "cpu"],
#             index=0,
#             help="Select the GPU device to use for rendering"
#         )
        
#         st.markdown("---")
#         st.markdown("### About")
#         st.markdown("""
#         This app generates dance animations from motion files.
#         Upload .npy motion files and optionally a music file 
#         to create synchronized dance videos.
#         """)

#     # File upload section
#     st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
#     st.subheader("Step 1: Upload Files")
    
#     uploaded_motion_files = st.file_uploader(
#         "Upload Motion Files (.npy)", 
#         type=["npy"], 
#         accept_multiple_files=True
#     )
    
#     uploaded_song = st.file_uploader(
#         "Upload Music File (optional)", 
#         type=["mp3", "wav", "ogg"]
#     )
    
#     st.markdown("</div>", unsafe_allow_html=True)
    
#     # Process button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         process_button = st.button("Generate Dance Videos", type="primary", use_container_width=True)
    
#     # Session state for tracking process status
#     if 'processing_complete' not in st.session_state:
#         st.session_state.processing_complete = False
#     if 'output_videos' not in st.session_state:
#         st.session_state.output_videos = []
    
#     # Process files when button is clicked
#     if process_button and uploaded_motion_files:
#         st.session_state.processing_complete = False
#         st.session_state.output_videos = []
        
#         temp_input_dir, temp_output_dir = create_temp_directories()
        
#         # Save uploaded motion files to temp directory
#         for motion_file in uploaded_motion_files:
#             file_path = os.path.join(temp_input_dir, motion_file.name)
#             with open(file_path, "wb") as f:
#                 f.write(motion_file.getbuffer())
        
#         # Save uploaded song if any
#         song_path = None
#         if uploaded_song:
#             song_path = os.path.join(temp_input_dir, uploaded_song.name)
#             with open(song_path, "wb") as f:
#                 f.write(uploaded_song.getbuffer())
        
#         # Show processing message
#         with st.status("Processing dance animations...", expanded=True) as status:
#             st.markdown("Starting render process...")
            
#             # Run the render script
#             success = run_render_script(temp_input_dir, temp_output_dir, song_path, device)
            
#             if success:
#                 st.markdown("Render process completed successfully!")
                
#                 # Get output videos
#                 output_videos = glob.glob(os.path.join(temp_output_dir, '*.mp4'))
                
#                 if output_videos:
#                     # Save paths to session state
#                     st.session_state.output_videos = output_videos
#                     st.session_state.processing_complete = True
#                     status.update(label="Processing complete!", state="complete", expanded=False)
#                 else:
#                     st.error("No output videos were generated.")
#                     status.update(label="Processing failed - no videos generated", state="error")
#             else:
#                 st.error("Error occurred during rendering.")
#                 status.update(label="Processing failed", state="error")
    
#     # Display output videos
#     if st.session_state.processing_complete and st.session_state.output_videos:
#         st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Generated Videos</h2>", unsafe_allow_html=True)
        
#         # Calculate number of columns based on number of videos
#         n_videos = len(st.session_state.output_videos)
#         cols_per_row = min(3, n_videos)  # Maximum 3 columns
        
#         # Create rows of videos
#         for i in range(0, n_videos, cols_per_row):
#             cols = st.columns(cols_per_row)
#             for j in range(cols_per_row):
#                 if i+j < n_videos:
#                     video_path = st.session_state.output_videos[i+j]
#                     video_name = os.path.basename(video_path).split('.')[0]
                    
#                     with cols[j]:
#                         st.video(video_path)
#                         st.markdown(f"<p class='video-title'>{video_name}</p>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
import os
import tempfile
import subprocess
import time
from pathlib import Path
import shutil
import glob

st.set_page_config(
    page_title="Long Dance Generation",
    page_icon="💃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stVideo {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .video-title {
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 0.5rem;
        text-align: center;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .processing-message {
        padding: 1rem;
        background-color: #cce5ff;
        color: #004085;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header and intro
st.markdown("<h1 class='main-header'>Long Dance Generation</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Upload motion files and music to generate dance videos</p>", unsafe_allow_html=True)

# Create temp directories function
def create_temp_directories():
    temp_input_dir = tempfile.mkdtemp()
    temp_output_dir = tempfile.mkdtemp()
    return temp_input_dir, temp_output_dir

# Function to run the render.py script
def run_render_script(motion_dir, output_dir, audio_file=None, device="0"):
    cmd = [
        "python", 
        "render.py", 
        "--modir", motion_dir,
        "--save_path", output_dir,
        "--device", device,
        "--fps", "30"
    ]
    
    # Use --audio parameter instead of --song for consistency with render.py
    if audio_file:
        cmd.extend(["--audio", audio_file])
        st.text(f"Using audio file: {audio_file}")
    
    # Show the command being executed for debugging
    st.text(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Stream the output
        for line in process.stdout:
            st.text(line.strip())
        
        # Also capture and display stderr for debugging
        stderr_output = []
        for line in process.stderr:
            stderr_output.append(line)
            st.text(f"ERROR: {line.strip()}")
        
        process.wait()
        
        if process.returncode != 0:
            st.error(f"Render process exited with error code {process.returncode}")
            st.error(f"Error output: {''.join(stderr_output)}")
            return False
        
        return True
    except Exception as e:
        st.error(f"Error running render script: {e}")
        return False

# Main app code
def main():
    with st.sidebar:
        st.image("https://i.imgur.com/4oDh1eH.png", width=100)  # A placeholder dance icon
        st.header("Settings")
        
        device = st.selectbox(
            "GPU Device",
            options=["0", "1", "2", "3", "cpu"],
            index=0,
            help="Select the GPU device to use for rendering"
        )
        
        # Add checkbox to apply audio to all videos
        apply_audio_to_all = st.checkbox(
            "Apply audio to all videos", 
            value=True,
            help="When checked, the uploaded audio will be added to all generated videos"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app generates dance animations from motion files.
        Upload .npy motion files and optionally a music file 
        to create synchronized dance videos.
        """)

    # File upload section
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.subheader("Step 1: Upload Files")
    
    uploaded_motion_files = st.file_uploader(
        "Upload Motion Files (.npy)", 
        type=["npy"], 
        accept_multiple_files=True
    )
    
    uploaded_audio = st.file_uploader(
        "Upload Audio File (optional)", 
        type=["mp3", "wav", "ogg"]
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button("Generate Dance Videos", type="primary", use_container_width=True)
    
    # Session state for tracking process status
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'output_videos' not in st.session_state:
        st.session_state.output_videos = []
    
    # Process files when button is clicked
    if process_button and uploaded_motion_files:
        st.session_state.processing_complete = False
        st.session_state.output_videos = []
        
        temp_input_dir, temp_output_dir = create_temp_directories()
        
        # Save uploaded motion files to temp directory
        for motion_file in uploaded_motion_files:
            file_path = os.path.join(temp_input_dir, motion_file.name)
            with open(file_path, "wb") as f:
                f.write(motion_file.getbuffer())
            st.text(f"Saved motion file: {file_path}")
        
        # Save uploaded audio if any
        audio_path = None
        if uploaded_audio:
            audio_path = os.path.join(temp_input_dir, uploaded_audio.name)
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())
            st.text(f"Saved audio file: {audio_path}")
        
        # Show processing message
        with st.status("Processing dance animations...", expanded=True) as status:
            st.markdown("Starting render process...")
            
            # Run the render script
            success = run_render_script(
                temp_input_dir, 
                temp_output_dir, 
                audio_path if uploaded_audio and apply_audio_to_all else None,
                device
            )
            
            if success:
                st.markdown("Render process completed successfully!")
                
                # Get output videos
                output_videos = glob.glob(os.path.join(temp_output_dir, '*.mp4'))
                
                if output_videos:
                    # Save paths to session state
                    st.session_state.output_videos = output_videos
                    st.session_state.processing_complete = True
                    status.update(label=f"Processing complete! Generated {len(output_videos)} videos.", state="complete", expanded=False)
                else:
                    st.error("No output videos were generated.")
                    status.update(label="Processing failed - no videos generated", state="error")
            else:
                st.error("Error occurred during rendering.")
                status.update(label="Processing failed", state="error")
    
    # Display output videos
    if st.session_state.processing_complete and st.session_state.output_videos:
        st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Generated Videos</h2>", unsafe_allow_html=True)
        
        # Calculate number of columns based on number of videos
        n_videos = len(st.session_state.output_videos)
        cols_per_row = min(3, n_videos)  # Maximum 3 columns
        
        # Create rows of videos
        for i in range(0, n_videos, cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i+j < n_videos:
                    video_path = st.session_state.output_videos[i+j]
                    video_name = os.path.basename(video_path).split('.')[0]
                    
                    with cols[j]:
                        # Add download button for the video
                        with open(video_path, "rb") as file:
                            st.download_button(
                                label=f"Download {video_name}",
                                data=file,
                                file_name=f"{video_name}.mp4",
                                mime="video/mp4"
                            )
                        
                        st.video(video_path)
                        st.markdown(f"<p class='video-title'>{video_name}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
