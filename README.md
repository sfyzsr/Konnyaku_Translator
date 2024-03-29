# Konnyaku_Translator
Konnyaku_Translator：一款使用python编写基于OCR的简易翻译器  
Konnyaku 来源于哆啦A梦中常用的翻译道具翻訳コンニャク（翻译魔芋），其コンニャク（Konnyaku）是由翻訳（honyaku）谐音所创造出来的道具名称。这里因translator功能方向与翻訳コンニャク大体相同（虽然没有翻訳コンニャク那么厉害），将其借用并命名为Konnyaku_Translator（魔芋翻译器）。
## 依赖安装
pip install PyQt5  
pip install pywin32   
pip install pyautogui  
pip install paddlepaddle  
pip install "paddleocr>=2.0.6"  
pip install googletrans  
pip install re  
## 制作动机
我作为一个多年的文字冒险类游戏玩家。在玩一些冷门老作品时，苦于找不到汉化/不会解包，又日语苦手，便打算使用机翻来进行游戏。网传的一些VNR翻译使用起来较为复杂，依赖安装复杂如需安装j北京等，资源查找复杂如分享链过期，论坛搜不到，正版买不起等，于是索性自己动手写一个翻译器。  
## 一些功能性需求
操作简单，快速上手，用户友好。  
完全免费，不需要注册账号来调用什么接口。  
安装流程简洁，规范。  
不重复造轮子，站在巨人的肩膀上。  
虽然在用OCR，但尽可能地做到轻量（毕竟是个工具类插件）。
## 原理
首先使用PYQT包来制作一个背景透明的简易程序框。程序对透明的部分进行截图，并OCR识别。最后使用googletrans或是爬虫脚本进行翻译。  
### 一些QA
* 为什么要做到背景透明？  
翻译器把需要翻译的文本框在透明的部分，当鼠标点击透明的部分时，点击的是透明部分的程序而不是翻译器，这样就不会影响需要翻译的程序运行。  
* 为什么用Python？  
~~人生苦短，我用Python~~  
用Java写，工程量可能有点大。用C++或者C#来写，翻译器可能会更快占用的内存更小一些，但时间复杂度主要集中在OCR上（OCR本身就快不到哪里去），所以为什么不用写起来更简单的Python？  
站在巨人的肩膀上 ~~(别人写好的就不用再写了)~~  
Python能用的包很多，开发起来很快，专注于实现功能本身。
* 准确度不高怎么办？  
额，一个是可能你需要一些日语基础，看到机翻和听到句子就能脑补出剩下的意思，或是直接对OCR识别的准确度低的内容进行更改后再翻译。另一个是准确度低主要是ocr识别精准度低，不少AVG的文字浮于图片上，背景图片很大影响OCR判断。后期~~有时间的话~~考虑自己训练一个神经网络来OCR。
* 拖动时一卡一卡的怎么办？  
这是正常的，一种解决方案是：去掉 高级系统设置 -> 性能 -> 拖动时显示窗口内容 复选框的 √ 
* 有时候googletrans罢工怎么办？  
googletrans本身就是一个非官方的包，它有时确实不会工作（官网里提到过），所以我额外写了一些爬虫翻译脚本，直接进行更换即可。
* 更换语言，翻译方式或是自动获取时间间隔在哪换？  
额，目前GUI还没做 ~~主要是懒~~，不如直接改源码？ 
## 软件使用
这是软件初始运行后的截图。  
![avatar](https://upload.cc/i1/2021/07/06/7Sulo1.png)
### 功能说明  
拖动Drag here来拖到翻译器，程序窗口大小可正常调节。  
Minimize：最小化程序。
Close: 关闭、退出程序。  
Get: 对透明部分截图，并进行OCR识别，翻译识别内容。  
Auto get：自动对透明部分截图，OCR识别，并翻译内容。  
Stop auto：停止自动获取翻译。  
Translation：对第一个文本框中的文字进行翻译。  
Clean：清除文本框，状态栏内容，以及清除图片缓存。
### 效果展示  

翻译器对运行在WinXP虚拟机上的游戏进行翻译，如图可见，每行提取后有一个OCR准确度，保留的目的是能帮助用户快速定位OCR识别不准确的句子并加以更改，而后对ocr提取后的文字进行处理加以翻译。  
  
![avatar](https://upload.cc/i1/2021/07/06/tivSez.png) 
  
此处文字和背景色差过小，识别效果并不太好，但基本可以脑补出意思来。  
  
![avatar](https://upload.cc/i1/2021/07/06/3QMhOI.png)  
## 后续改进
* 优化UI
* 使用自己训练的OCR，或许能提高精准度？
* 添加更多的翻译爬虫以提高翻译质量。
## 后话
我编码技术可能有些许稚嫩或是笨拙，再此抛砖引玉，请大家多多包涵不吝赐教。比起Coding更重要的是玩的开心。
