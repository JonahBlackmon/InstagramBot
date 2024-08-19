from datetime import timedelta
import autosub
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt
from moviepy.config import change_settings
import uuid
from pathConfig import get_default
def autoCaption(videopath, subtitlepath):
    change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
    default_path = get_default()
    file = videopath

    def add_subtitles(video_path, srt_path, output_path):
        # Load video
        video = VideoFileClip(video_path)
        
        # Load subtitles
        subs = pysrt.open(srt_path)
        
        # Function to create subtitle clips
        def subtitle_clips(subtitles, video_clip):
            clips = []
            for sub in subtitles:
                txt_clip = TextClip(sub.text, font='KOMIKAX_', fontsize=72, color='white', stroke_width=8, stroke_color='black')
                txt_clip = txt_clip.set_position(('center', 250)).set_start(sub.start.seconds).set_duration(sub.end.seconds - sub.start.seconds)
                clips.append(txt_clip)
            return clips
        
        # Create subtitle clips
        subtitle_clips_list = subtitle_clips(subs, video)
        
        # Combine video with subtitles
        final_video = CompositeVideoClip([video] + subtitle_clips_list)
        
        # Write the result to a file
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Paths to your files
    video_path = file
    srt_path = subtitlepath
    output_path = f"{default_path}/AIChatbot/mediaOutput/captionedVideo/{uuid.uuid4()}.mp4"
    

    # Add subtitles to the video
    add_subtitles(video_path, srt_path, output_path)
