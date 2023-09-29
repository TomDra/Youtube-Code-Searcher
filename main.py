import os
import upload_detect as ud
import video_manager as vm
import text_from_image as tfi
import time, shutil, threading
global finished
finished = False

def thread_loop(output_path, code_path):
    global finished
    while not finished:
        tfi.main(output_path, code_path)
    tfi.main(output_path, code_path)
    tfi.code_sender(code_path)


def main():
    running = True
    channel = 'https://www.youtube.com/user/KSIOlajidebtHD'
    code_path = 'codes/'
    finished_path = 'finished/'
    output_path = 'temp_frames/'
    while running:
        start_time = time.time()
        shutil.rmtree(output_path) if os.path.exists(output_path) else None
        shutil.rmtree('temp/') if os.path.exists('temp/') else None
        if not os.path.exists(finished_path):
            os.makedirs(finished_path)
        ud.get_latest_upload(channel, finished_path)
        #video_id = ud.check_new_upload(channel)
        #dv.download(f"https://www.youtube.com/watch?v={video_id}")
        root_dir = os.getcwd()
        file = vm.get_mp4_files(root_dir)
        if file != []:
            file = file[0]
            print(file)
            print('Converting to frames...')
            thread = threading.Thread(target=thread_loop, args=(output_path, code_path))
            thread.start()
            global finished
            finished = vm.convert_fps(file, output_path, 1)
            finished = True
            thread.join()
            print('Extracting text...')
            os.rename(file, finished_path + file)
        else:
            print('No new video processed')
        print(time.asctime(time.localtime(time.time())),'- Time taken:', time.time() - start_time)
        time.sleep(1)
if __name__ == '__main__':
    while True:
        try:
            main()
        except IndexError as a:
            print(a)
#vm.split_video_to_frames(file, 'temp_frames/')
