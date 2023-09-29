import cv2, os
#from moviepy.editor import *


"""
def convert_fps(video_path, fps):
    ""
    Convert the video to the given fps
    ""
    KPS = fps  # Target Keyframes Per Second
    VIDEO_PATH = video_path  # "path/to/video/folder" # Change this
    IMAGE_PATH = "images/"  # "path/to/image/folder" # ...and this
    EXTENSION = ".png"
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    print(fps)
    # exit()
    hop = round(fps / KPS)
    curr_frame = 0
    while (True):
        ret, frame = cap.read()
        if not ret:
            break
    if curr_frame % hop == 0:
        name = IMAGE_PATH + "-" + str(curr_frame) + EXTENSION
        cv2.imwrite(name, frame)
    curr_frame += 1
    cap.release()
"""

def convert_fps(video_path,output_path , wfps):
    """
    Convert the video to the given fps
    """
    threads = []
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists('temp/'):
        os.makedirs('temp/')
    vidcap = cv2.VideoCapture(video_path)
    frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    length = frames * fps
    wanted_frames = int(length / wfps)
    gap = wanted_frames/frames
    #success, image = vidcap.read()
    #thread = threading.Thread(target=create_frames, args=(gap, vidcap, output_path))
    get_all_frames_by_ms(vidcap, output_path, 0)
    return True

    #for i in range(10):
    #    threads.append(threading.Thread(target=create_frames, args=(gap, vidcap, output_path)))
    #for thread in threads:
    #    thread.start()
    #thread.join()
    #create_frames(gap, vidcap, output_path)

def get_all_frames_by_ms(vidcap, output_path, time):
    count = 0
    while True:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, time)
        capture_success, frame = vidcap.read()
        if capture_success:
            cv2.imwrite(output_path + "/frame%d.jpg" % count, frame)
            count = count + 30
        else:
            break
        time += 1000

def create_frame(gap, vidcap, output_path):
    global count
    """create a loop that will run for the number of frames in the video and will only save the frame if the frame number is divisible by the gap"""
    success, image = vidcap.read()
    while success:
        if count % gap == 0:
            cv2.imwrite(output_path + "/frame%d.jpg" % count, image)
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite('temp/' + "/frame%d.jpg" % count, image)
        count += 1



    """
    for i in range(0, frames):
        if count % wanted_frames == 0:
            print(f'writing frame {count}')
            cv2.imwrite(output_path + "/frame%d.jpg" % count, image)
        else:
            print(f'skipping frame {count}')
        success, image = vidcap.read()
        count += 1

        cv2.imwrite(output_path+"frame%d.jpg" % count, image)  # save frame as JPEG file
        for i in range(int(gap)):
            success, image = vidcap.read()
            count += 1
            print(f'skipping {count}')
        success, image = vidcap.read()
        print(count,'Read a new frame: ', success)
        count += 1
"""
def get_mp4_files(path):
    """
    Get all mp4 files in the given path
    """
    import os
    mp4_files = []
    for file in os.listdir(path):
        if file.endswith(".mp4"):
            mp4_files.append(file)
    #for root, dirs, files in os.walk(path):
    #    for file in files:
    #        if file.endswith(".mp4"):
    #            mp4_files.append(os.path.join(root, file))
    return mp4_files

#def split_video_to_frames(video_path, frame_path):
#    """
#    Split the video into frames and save them in the given path
#    """
#    import cv2
#    import os
#    if not os.path.exists(frame_path):
#        os.makedirs(frame_path)
#    vidcap = cv2.VideoCapture(video_path)
#    success, image = vidcap.read()
#    count = 0
#    while success:
#        cv2.imwrite(frame_path + "/frame%d.jpg" % count, image)
#        success, image = vidcap.read()
#        count += 1
