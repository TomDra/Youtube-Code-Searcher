import os
import re,threading
import sms_sender as sms
codes = []

def grab_text_from_image(file):
    import pytesseract as pt
    '''grab the text from the image'''
    pt.pytesseract.tesseract_cmd = r'ignore-tesseract\tesseract.exe'
    # Grab the text from the image
    text = pt.image_to_string(file)
    return text

def get_images(folder):
    '''get all the images in the folder'''
    import os
    import glob
    # Get all the images in the folder
    images = glob.glob(folder + '/*.jpg')
    return images

def handle_image(image,code_path):
    try:
        text = grab_text_from_image(image)
    except Exception:
        print('error')
        return
    """use re to search for an amazon code which looks like this:
    MG25-Z9BARE-PXBX
    79L8-B66FZJ-62BQ
    """
    code = re.search(r'[A-Z0-9]{4}-[A-Z0-9]{6}-[A-Z0-9]{4}', text)
    code1 = re.search(r'^(Claim Code: ).{16}', text)
    filename = image.split("\\")
    if code or code1:
        if code:
            code = re.sub(r'[\\/*?:"<>|,]',"",code.group(0))
        if code1:
            code = re.sub(r'[\\/*?:"<>|,]',"",code1.group().strip('Claim Code: '))
        codes.append(code)
        print(f'{image} - Found Code - {code}')
        code_file = f'{code_path}{code.replace("-", " ")} {filename[1]}'
        try:
            os.rename(image, code_file)
        except FileExistsError:
            print(f'{image} - Code already exists')
        sms.webhook_message(code_file)
    else:
        print(f'{image} - No Code Found')
        #while True:
            #try:
                # connect
        print(f'{image} - No Code Found, moving file')
        os.rename(image, f'temp/{filename[1]}')
                #break
            #except Exception:
                #pass



def main(output_path, code_path):
    global codes
    #if path not exists, create it
    if not os.path.exists(code_path):
        os.makedirs(code_path)
    #grab the finished variable from main.py to see if the program should continue

    #get all the images in the folder
    if True:
        images = get_images(output_path)
        threads = []
        count = 0
        if images != []:
            for image in images:
                count = count + 1
                #if count % 450 == 0:
                #    thread.join()
                """create a thread for each image whith the handle_image function and parse the name of the image"""

                threads.append(threading.Thread(target=handle_image, args=(image,code_path,)))
            for thread in threads:
                thread.start()
                print(f'started thread {thread}')
            for thread in threads:
                thread.join()


def code_sender(code_path):
    global codes
    """remove any duplicates from codes list"""
    non_dup_codes = list(dict.fromkeys(codes))
    print(non_dup_codes)
    print('Sending SMS of codes')
    sms.send(non_dup_codes)
