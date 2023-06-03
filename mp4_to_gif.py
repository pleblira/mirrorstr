from moviepy.editor import VideoFileClip

def resize_clip(clip, percentage):
    width = int(clip.size[0] * percentage / 100)
    clip_resized = clip.resize(width=width)
    return clip_resized

def mp4_to_gif(input_file, output_file, resize_percentage, frame_rate):
    clip = VideoFileClip(input_file)
    clip_resized = resize_clip(clip, resize_percentage)
    clip_resized.write_gif(output_file, fps=frame_rate)
    clip.close()

# Example usage
# input_file = "input.mp4"
# output_file = "output.gif"
# resize_percentage = 50  # Set the desired resize percentage (e.g., 50 for 50%)
# frame_rate = 4  # Set the desired frame rate

# mp4_to_gif(input_file, output_file, resize_percentage, frame_rate)
