import subprocess
from bottle import run, post, request, response, get, route
import slack, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests, json

def create_timer_img(timestamp):
    
    image = Image.new("RGBA", (800, 600))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Roboto-Bold.ttf", 156)
    tm = time.strftime('%H:%M:%S', time.gmtime(timestamp))
    draw.text((85, 215), tm, UKG_DARK, font=font)
    
    image.save("timer.png")

dadurl = "https://icanhazdadjoke.com/slack"
@route('/<path>',method = 'POST')
def process(path):
    #print(path)
    x = requests.get(dadurl)
    jsond = x.json()
    client.chat_postMessage(channel='#testing-slack-api', text=jsond["attachments"][0]["text"])


client = slack.WebClient(token='xoxb-2055336641954-2061564253988-WcVilyyUMoDhK567aalUXACe')
#client = slack.WebClient(token='xoxp-2055336641954-2040564657943-2048421007543-a6b5ca53ebd029bd187ea755b4b5c8d0')


# ID of the channel you want to send the message to
channel_id = "C022B45ANL8"
gen_id = "C021TENLBLL"
ts = "1620835912.000300" # ts of message to edit

UKG_TEAL = (48, 206, 187)
UKG_DARK = (0, 81, 81)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def send_image(ts):
        upload_result = client.files_upload(channels="C022B45ANL8", file="timer.png")
        last_msg = client.conversations_history(channel="C022B45ANL8", limit=1)
        del_ts = last_msg["messages"][0]["ts"]
        del_ch = "C022B45ANL8"
        delete = client.chat_delete(channel=del_ch,ts=del_ts)

        pub_url = upload_result["file"]["permalink_public"]
        TFP = pub_url.split('/')[3]
        TFP_arr = TFP.split('-')
        new_url = f"https://files.slack.com/files-pri/{TFP_arr[0]}-{TFP_arr[1]}/timer.png"

        attch = [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "image_url": new_url,
                "thumb_url": new_url,
            }
        ]
        
        #client.chat_postMessage(channel='#testing-slack-api', text="<!here>", attachments = attch)
        result = client.chat_update(channel=gen_id, ts=ts, text="", attachments = attch)

def run_timer(timer_amn):
    client.chat_postMessage(channel='C021TENLBLL', text="timer start")
    last_msg = client.conversations_history(channel="C021TENLBLL", limit=1)
    ts = last_msg["messages"][0]["ts"]

    prev_time = int(time.time())
    curr_time = prev_time
    seconds_since_start = 0
    while seconds_since_start < timer_amn:

        create_timer_img(timer_amn-seconds_since_start)
        send_image(ts)
        
        while curr_time == prev_time:
            curr_time = int(time.time())
        seconds_since_start += curr_time-prev_time
        print(seconds_since_start)
        prev_time = curr_time
    create_timer_img(0)
    send_image(ts)

# <@U0216GLKBTR> my id
# <@U021TGL7FV2> bot id

run_timer(9)

run(host='localhost', port=8080, debug=True)
quit()