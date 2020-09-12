# Salmon-plugins-transplant
简单修改其他nonebot的插件以移植到HoshinoBot。当然说搬运也差不多。
感谢大佬的项目支持。

使用：

文件夹丢进modules下，config的__bot__.py里添加模块。重启hoshino。

更新：

20.9.5

迫害龙王插件。res包的img下新建文件夹longwang，把收集到的表情包丢进去，并将第一张重命名为dragon1.jpg，第X张就是dragonX.jpg。 打开代码第30行，有多少张改成多少。 

20.9.7

天气查询。群聊发送指令[查天气+城市]即可。需要安装依赖thulac

20.9.9

老婆生成器（9.11已替换为船新版本），发送老婆帮助查看指令。
互动加亲密度，满亲密度可结婚；分手加渣男值。
（不是很阳间的功能，默认关闭需要启用服务，使用前请三思）。
启用模块前请修改hoshino的chat.py里“老婆”的指令回复以解除冲突（当然改这玩意的__init__.py也可以）

20.9.11

steam或其他平台游戏促销/喜加一查询。群聊发送指令[steam促销]/[喜加一]即可。需要安装依赖nest_asyncio

20.9.12

日语词典查询功能。群聊发送[日典 日语单词]查询。需要安装依赖kth_timeoutdecorator


鸣谢@Angel-Hair,@farewell12345
