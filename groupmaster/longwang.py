import json
import re
import random
import os
from os import path
from nonebot import MessageSegment
import random
import hoshino
from hoshino import Service, aiorequests, R, logger
from hoshino.util import FreqLimiter, DailyNumberLimiter, pic2b64

_max = 3
EXCEED_NOTICE = f'您今天已经迫害过{_max}次龙王了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)
imgbase_path = 'longwang'
if not path.exists(R.img(imgbase_path).path):
    os.makedirs(R.img(imgbase_path).path)

sv = Service('longwang')

@sv.on_command('迫害龙王')
async def longwang(session):
    global imgbase_path
    uid = session.ctx['user_id']
    if not _nlmt.check(uid):
        await session.send(EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await session.send('龙王她生气了，并堵上了你的嘴', at_sender=True)
        return
    _flmt.start_cd(uid)
    gid = session.ctx['group_id']
    dragon_king=await session.bot.get_group_honor_info(group_id=gid,type='talkative')
    if not 'current_talkative' in dragon_king:
        await session.send('本群暂时还没有龙王哦……', at_sender=True)
        return
    dragon_king=dragon_king['current_talkative']['user_id']
    dir_list = os.listdir(R.img(imgbase_path).path)
    try:
        img_path = path.join(imgbase_path, random.choice(dir_list))
    except Exception:
        hoshino.logger.error('缺少龙王图片资源或目录下文件夹过多')
        return
    count = 0
    while os.path.isdir(img_path) == True:
        img_path = path.join(imgbase_path, random.choice(dir_list))
        count += 1
        if count % 5 == 0:
            hoshino.logger.error('缺少龙王图片资源或目录下文件夹过多')
            return
    longwang_img = R.img(img_path).open()
    longwang_img_message = MessageSegment.image(pic2b64(longwang_img))
    reply=random.choice(['龙王出来挨透','龙王出来喷水'])
    _nlmt.increase(uid)
    await session.finish(f'[CQ:at,qq={dragon_king}]\n{reply}\n{longwang_img_message}')
