import whisper
from tqdm import tqdm
import os

# Load the Whisper model
model = whisper.load_model("base")

# Function to transcribe a video with a progress bar and save outputs as both txt and srt
def transcribe_video(file_path, output_txt_path, output_srt_path):
    # Transcribe the video to get segments
    result = model.transcribe(file_path, verbose=True)

    # Progress bar based on the number of segments
    segments = result["segments"]
    progress_bar = tqdm(total=len(segments), desc=f"Transcribing {os.path.basename(file_path)}")

    transcription_text = ""
    srt_text = ""
    for i, segment in enumerate(segments):
        # Append each segment's text for the full transcription
        transcription_text += segment["text"]

        # Format segment to SRT format
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        srt_text += f"{i + 1}\n{start_time} --> {end_time}\n{segment['text']}\n\n"

        # Update the progress bar
        progress_bar.update(1)

    progress_bar.close()

    # Save transcription as .txt
    with open(output_txt_path, "w") as txt_file:
        txt_file.write(transcription_text)
    
    # Save transcription as .srt
    with open(output_srt_path, "w") as srt_file:
        srt_file.write(srt_text)

# Helper function to convert timestamp to SRT format (HH:MM:SS,ms)
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# Directory containing video files
resources_dir = "resources"

# Process each video file in the resources directory
for filename in os.listdir(resources_dir):
    if filename.endswith((".mp4", ".mkv", ".avi", ".mov")):  # add more video formats if needed
        video_path = os.path.join(resources_dir, filename)
        
        # Define paths for output .txt and .srt files
        base_filename = os.path.splitext(filename)[0]
        txt_output_path = os.path.join(resources_dir, f"{base_filename}.txt")
        srt_output_path = os.path.join(resources_dir, f"{base_filename}.srt")
        
        # Transcribe the video and save outputs
        print(f"Processing file: {filename}")
        transcribe_video(video_path, txt_output_path, srt_output_path)

print("All transcriptions completed.")
