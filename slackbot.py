import slack, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

client = slack.WebClient(token='xoxb-2055336641954-2061564253988-m7zVWw7B75Jz2C5y7Pl75ZYA')
#client = slack.WebClient(token='xoxp-2055336641954-2040564657943-2043879805847-ba1e3b7d035267cd8f267a2b4b13c03e')

# ID of the channel you want to send the message to
channel_id = "C022B45ANL8"
ts = "1620835912.000300" # ts of message to edit

UKG_TEAL = (48, 206, 187)
UKG_DARK = (0, 81, 81)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image = Image.new("RGB", (800, 600), UKG_TEAL)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("Roboto-Bold.ttf", 96)
draw.text((200, 230),"hh:mm:ss", UKG_DARK, font=font)

#image.show()
image.save("timer.png")

upload_result = client.files_upload(file="timer.png")

# https://slack-files.com/{team_id}-{file_id}-{pub_secret}
# https://files.slack.com/files-pri/{team_id}-{file_id}/{filename}?pub_secret={pub_secret}
# https://files.slack.com/files-pri/T021M9WJVU2-F021V896DBM/timer.png

pub_url = upload_result["file"]["permalink_public"]
TFP = pub_url.split('/')[3]
TFP_arr = TFP.split('-')
new_url = f"https://files.slack.com/files-pri/{TFP[0]}-{TFP[1]}/timer.png"

#print(pub_url)
print(new_url)
attch = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "image_url": new_url,
            "thumb_url": new_url
        }
    ]
client.chat_postMessage(channel='#testing-slack-api', text="", attachments = attch)

quit()

# <@U0216GLKBTR> my id

prev_time = int(time.time())
curr_time = prev_time
for ii in range(60):
    result = client.chat_update(channel=channel_id, ts=ts, text=str(60-ii), attachments = image)
    while curr_time == prev_time:
        curr_time = int(time.time())
    prev_time = curr_time
