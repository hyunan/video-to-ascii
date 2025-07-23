import cv2
import numpy
from PIL import Image
import os
import time
import sys

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def resize_image(image: Image, new_width = 150):
    width, height = image.size
    aspect_ratio = height/width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height))

def get_ascii_frame(image: Image, width=120):
    resized_image = resize_image(image, new_width=width)
    gray_scale_image = resized_image.convert('L')
    ascii_string = "".join([ASCII_CHARS[pixel // 25] for pixel in gray_scale_image.getdata()])
    ascii_image = "\n".join(
        ascii_string[i:i + width] for i in range(0, len(ascii_string), width)
    )
    return ascii_image

def clear_terminal():
    # os.system("cls" if os.name == "nt" else "clear")
    print("\033[H", end="")

def play_ascii_animation(video_path, width=120):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            ascii_frame = get_ascii_frame(frame_image, width=width)
            clear_terminal()
            print(ascii_frame)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nPlayback stopped.")
    finally:
        cap.release()


if __name__ == "__main__":
    video_path = str(sys.argv[1]).strip()
    if not os.path.isfile(video_path):
        print("Error: Video not found!")
    else:
        play_ascii_animation(video_path, width=120)