import random
import vk_api
from config import YOUR_ID, WIFE_ID

def send_to_you(vk, msg):
    vk.messages.send(user_id=YOUR_ID, message=msg, random_id=random.randint(1, 2**31))

def send_to_wife(vk, msg):
    vk.messages.send(user_id=WIFE_ID, message=msg, random_id=random.randint(1, 2**31))