import subprocess
from bottle import run, post, request, response, get, route
import slack, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests, json
import imageio

dadurl = "https://icanhazdadjoke.com/slack"
def get_dad_joke():
    x = requests.get(dadurl)
    return x.json()["attachments"][0]["text"]

def generate_timer_gif(at, total):
    frames = min(30, total-at)
    at_pos = 0
    filenames = []
    while frames > 0:
        filenames.append(create_timer_img(total - (at+at_pos), at_pos))
        frames -= 1
        at_pos += 1
    
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
        imageio.mimsave('movie.gif', images, format='GIF', fps=1, loop=1)

def create_timer_img(timestamp, iter=0):
    image = Image.new("RGBA", (800, 600), UKG_TEAL)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Roboto-Bold.ttf", 156)
    tm = time.strftime('%H:%M:%S', time.gmtime(timestamp))
    draw.text((85, 215), tm, UKG_DARK, font=font)
    image.save(f"timer{iter}.png")
    return f"timer{iter}.png"

client = slack.WebClient(token='xoxb-2055336641954-2061564253988-9kvF5yZLdzBTGVmT9uxFTvne')
#client = slack.WebClient(token='xoxp-2055336641954-2040564657943-2048421007543-a6b5ca53ebd029bd187ea755b4b5c8d0')


# ID of the channel you want to send the message to
test_id = "C022B45ANL8"
gen_id = "C021TENLBLL"
ts = "1620835912.000300" # ts of message to edit

UKG_TEAL = (48, 206, 187)
UKG_DARK = (0, 81, 81)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def send_image(ts, filename):
        upload_result = client.files_upload(channels=test_id, file=filename)
        last_msg = client.conversations_history(channel=test_id, limit=1)
        del_ts = last_msg["messages"][0]["ts"]
        del_ch = test_id
        delete = client.chat_delete(channel=del_ch,ts=del_ts)

        pub_url = upload_result["file"]["permalink_public"]
        TFP = pub_url.split('/')[3]
        TFP_arr = TFP.split('-')
        new_url = f"https://files.slack.com/files-pri/{TFP_arr[0]}-{TFP_arr[1]}/{filename}"

        attch = [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "image_url": new_url,
                "thumb_url": new_url,
            }
        ]
        
        result = client.chat_update(channel=gen_id, ts=ts, text="", attachments = attch)

def run_timer(timer_amn):
    client.chat_postMessage(channel=gen_id, text="Starting Timer...")
    last_msg = client.conversations_history(channel=gen_id, limit=1)
    ts = last_msg["messages"][0]["ts"]

    generate_timer_gif(0, timer_amn)
    seconds_since_start = 0
    prev_time = int(time.time())
    curr_time = prev_time
    print(seconds_since_start, timer_amn)
    while seconds_since_start < timer_amn:
        #create_timer_img(timer_amn-seconds_since_start)
        send_image(ts, "movie.gif")
        generate_timer_gif(seconds_since_start+30, timer_amn)
        print(seconds_since_start - 30, timer_amn)
        time_rem = timer_amn - seconds_since_start
        time_inc = min(time_rem, 30)
        while curr_time < prev_time + time_inc:
            print(curr_time - prev_time)
            curr_time = int(time.time())
        seconds_since_start += curr_time-prev_time
        prev_time = curr_time
    create_timer_img(0)
    send_image(ts, "timer0.png")
    client.chat_postMessage(channel=gen_id, text="<!here> Time's up! " + get_dad_joke())

# <@U0216GLKBTR> my id
# <@U021TGL7FV2> bot id

@route('/<path>',method = 'POST')
def process(path):
    print(path)
    if path == "joke":
        client.chat_postMessage(channel=gen_id, text=get_dad_joke())
    if path == "timer":
        run_timer(40)
    return True

run(host='localhost', port=8080)