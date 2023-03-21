# TalkToWorld
为中文地区渐冻症、失语者制作的自动发音键盘(Automatic pronunciation keyboard for people with ALS and aphasia in Chinese)
## 特点
可以在大屏幕便携设备上（例如Pad）实现病人输入的同时让系统自动进行中文发音，实现了与外界的声音交流
具体的方案，可以根据需要进行改进，例如配合具体的Pad电脑、鼠标轨迹球（病人手指可动的情况下）等外接设备，方便病人进行人机交互 

![case](https://github.com/geekgao/TalkToWorld/raw/main/CASE.png)  

或者，使用成本更高的头戴式控制方案（病人肢体无法运动的情况下），例如GlassOuse：

[![例如GlassOuse](https://glassouse.com/wp-content/uploads/2022/06/gallery-images-2-scaled.jpg)](https://glassouse.com/)  

GlassOuse是一款为残疾人设计的无线鼠标设备，其特殊的设计可以帮助身体上有一定障碍的人士更轻松地控制计算机。这款设备的外形类似于眼镜，可以佩戴在头部，并通过头部的移动来控制鼠标的移动和点击。  
GlassOuse的设计旨在为那些无法使用传统鼠标和键盘的人士提供一种可靠的、易于使用的解决方案，例如由于肢体残疾或神经系统疾病而导致的运动障碍或瘫痪。它使用蓝牙技术连接到计算机或其他设备上，并具有可替换的电池，使用寿命长。**缺点：价格高，不过还不算离谱。**  



## 原理
- 基于PyQt实现的系统界面，非常想容易可以实现跨平台移植
- 利用系统自带的TTS朗读输入文字
- 利用Google中文输入接口获取可能的输入词
## 界面截图
![screenshot](https://github.com/geekgao/TalkToWorld/raw/main/screenshot.jpg)
![screenshot](https://github.com/geekgao/TalkToWorld/raw/main/screenshot2.jpg)

## 备注
本文中提到的控制类设备均可以网络中买到，可自行搜索。
这个程序可能还有很多待完善的地方，例如：输入文字缓存、常用句收藏等功能特性
