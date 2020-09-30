# Salmon-plugins-transplant

简单修改其他nonebot的插件以移植到HoshinoBot。
感谢大佬的项目支持。

## 功能说明

<details>
<summary><mark> 点击展开</mark></summary>

### 迫害龙王

一个迫害龙王插件。需要在res包的img下新建文件夹longwang，把收集到的表情包丢进去，并将第一张重命名为dragon1.jpg，第X张就是dragonX.jpg。 然后打开代码第30行，图片改为相应张数。

### 天气查询

查询城市的一周天气预报。需要安装依赖jieba

### 老婆生成器

整活插件。发送老婆帮助可以查看相关指令。

（不是很阳间的功能，默认关闭需要启用服务，使用前请三思）。

启用模块前请修改hoshino的chat.py里“老婆”的指令回复以解除冲突（当然改这玩意的__init__.py也可以）

### steam促销查询/免费游戏领取

steam或其他平台游戏促销/喜加一的查询插件。需要安装依赖nest_asyncio

### 日语词典

日语词典查询插件。需要安装依赖kth_timeoutdecorator

### 知乎日报

知乎热搜查询插件。

### 搜图

整合了 SauceNAO 和 ascii2d 的识图插件。可以自行修改超时时间、返回数量等。需要填入SauceNAO的APIkey。安装依赖kth_timeoutdecorator

</details>
<br>

## 使用

(如果需要的话)安装对应模块的依赖，将模块文件夹放进modules下，config的__bot__.py里添加模块。然后重启hoshino。

鸣谢@Angel-Hair，@farewell12345，@kkbllt
