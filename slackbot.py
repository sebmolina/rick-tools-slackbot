import slack, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

client = slack.WebClient(token='xoxb-2055336641954-2061564253988-d1VZMjXGyskf1SQEgfbA0nrU')
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
    
    image = Image.new("RGB", (800, 600), UKG_TEAL)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Roboto-Bold.ttf", 96)
    draw.text((190, 235),"hh:mm:ss", UKG_DARK, font=font)
    image.save("timer.png")

    #image.show()

    upload_result = client.files_upload(channels="C022B45ANL8", file="timer.png")
    del_ts = upload_result["timestamp"]
    del_ch = "C022B45ANL8"

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
