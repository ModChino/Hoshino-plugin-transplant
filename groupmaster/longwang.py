import json
import re
import random
import os
from os import path
from nonebot import MessageSegment
import random
import hoshino
from hoshino import Service,aiorequests
from hoshino.util import FreqLimiter, DailyNumberLimiter

_max = 3
EXCEED_NOTICE = f'您今天已经迫害过{_max}次龙王了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)
res_path = path.abspath(path.join(path.expanduser(hoshino.config.RES_DIR),'longwang'))
if not path.exists(res_path):
	os.makedirs(res_path)

sv = Service('longwang')

@sv.on_command('迫害龙王')
async def longwang(session):
    global res_path
    uid = session.ctx['user_id']
    if not _nlmt.check(uid):
        await session.send(EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await session.send('龙王她生气了，并堵上了你的嘴', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    gid = session.ctx['group_id']
    dragon_king=await session.bot.get_group_honor_info(group_id=gid,type='talkative')
    dragon_king=dragon_king['current_talkative']['user_id']
    res_list = os.listdir(res_path)
    pic = random.choice(res_list)
    pic_path = path.join(res_path, pic)
    reply=random.choice(['龙王出来挨透','龙王出来喷水'])
    longwang = MessageSegment.image(f'file:///{pic_path}')
    await session.finish(f'[CQ:at,qq={dragon_king}]\n{reply}\n{longwang}')