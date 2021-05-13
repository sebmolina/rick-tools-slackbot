import subprocess
from bottle import run, post, request, response, get, route
import slack, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests, json

def create_timer_img(timestamp):
    
    image = Image.new("RGB", (800, 600), UKG_TEAL)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Roboto-Bold.ttf", 96)
    tm = time.strftime('%H:%M:%S', time.gmtime(timestamp))
    draw.text((190, 235), tm, UKG_DARK, font=font)
    
    image.save("timer.png")

dadurl = "https://icanhazdadjoke.com/slack"
@route('/<path>',method = 'POST')
def process(path):
    #print(path)
    x = requests.get(dadurl)
    jsond = x.json()
    client.chat_postMessage(channel='#testing-slack-api', text=jsond["attachments"][0]["text"])


client = slack.WebClient(token='xoxb-2055336641954-2061564253988-Fb9vUh80YzMQeOCa5qNIBs2v')
#client = slack.WebClient(token='xoxp-2055336641954-2040564657943-2048421007543-a6b5ca53ebd029bd187ea755b4b5c8d0')


# ID of the channel you want to send the message to
channel_id = "C022B45ANL8"
ts = "1620835912.000300" # ts of message to edit

UKG_TEAL = (48, 206, 187)
UKG_DARK = (0, 81, 81)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# <@U0216GLKBTR> my id

prev_time = int(time.time())
curr_time = prev_time
for ii in range(60):

    create_timer_img(120-ii)
    #image.show()

    upload_result = client.files_upload(channels="C022B45ANL8", file="timer.png")
    #del_ts = upload_result["timestamp"]
    #del_ch = "C022B45ANL8"
    #delete = client.chat_delete(channel=del_ch,ts=del_ts)

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
    
    print(upload_result)
    #client.chat_postMessage(channel='#testing-slack-api', text="<!here>", attachments = attch)
    result = client.chat_update(channel=channel_id, ts=ts, text=str(60-ii), attachments = attch)
    
    while curr_time == prev_time:
        curr_time = int(time.time())
    prev_time = curr_time


run(host='localhost', port=8080, debug=True)
quit()