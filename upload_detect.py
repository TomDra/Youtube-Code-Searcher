import requests
import re, os
import tempfile
import webbrowser, time
import pytube

def get_latest_upload(channel, finished_path):
    """returns the url of the latest upload"""
    c = pytube.Channel(channel)
    newest_video = c.videos[0]
    tags = str(newest_video.streams.filter(progressive=True))
    stream = tags[1:]
    stream = stream[:-1]
    streamlist = stream.split(", ")
    for i in range(0, len(streamlist)):
        st = streamlist[i].split(" ")
        if st[3] == 'res="360p"':
            tag1 = st[1][:-1].strip('itag="')
        elif st[3] == 'res="720p"':
            tag2 = st[1][:-1].strip('itag="')
        print(st[1], st[3])
    try:
        video = newest_video.streams.get_by_itag(tag1)
    except Exception as e:
        print("Error: ", e)
        video = newest_video.streams.get_by_itag(tag2)
    if re.sub(r'[\\/*?:"<>|,£$]',"",newest_video.title)+'.mp4' in os.listdir(finished_path):
        print("File already exists")
    else:
        print(f'Downloading - {str(newest_video.title)}')
        video.download()
        print('Download complete')



def check_new_upload(channel):
    new_video_found = False
    while new_video_found != True:
        #channel = "https://www.youtube.com/channel/UCGmnsW623G1r-Chmo5RB4Yw"
        #channel = "https://www.youtube.com/c/McLaren"
        #channel = 'https://www.youtube.com/channel/UC9_p50tH3WmMslWRWKnM7dQ'
        #channel = 'https://www.youtube.com/c/FoxNews'
        html = requests.get(channel + "/videos").text

        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8") as f:
            url = 'file://' + f.name
            f.write(html)
        webbrowser.open(url)


        html = requests.get(channel + "/videos").text
        print(html)
        info = re.search('(?<={"label":").*?(?="})', html).group()
        try:
            date = re.search('\d+ \w+ ago.*seconds ', info).group()
        except AttributeError:
            date = re.search('\d+ \w+ ago.*minutes ', info).group()
        """use re to search for the url of the video
        examples are:
        "url":"/watch?v=dQw4w9WgXcQ"
        "url":"/watch?v=ijAISJD4324"
        "url":"/watch?v=sadwSAD3dt5"
        """
        url = re.search(r"(?<=\"url\":\"/watch\?v\=)(.*)(webPageType)", html).group().split('","webPageType')[0]

        #link = re.search('"url":"/watch?v=.*"', info)
        print('hi', url)



        """if date is within the last hour then new_video_found = True"""
        if date is not None:
            for i in range(0, 60):
                print(i)
                if (f"{i} minutes ago") in date or (f"1 minute ago") in date or (f"{i} seconds ago") in date or (f"1 second ago") in date:
                    new_video_found = True
                    return url
        else:
            new_video_found = False

        print(new_video_found)

        print(info)
        print(date)
        time.sleep(30)
