# MDPic  

## 开发环境  
+ python 3.7.3  
+ python包，详见根目录的requirement.txt文件

## 功能计划
1. 截图  
2. ~~录屏~~   
3. gif  
4. 上传github图床  
5. 管理图片  

## 功能设计
1. 截图  
截图、多张连续截图聚合成gif。截图完成后，临时存储到本地（gif保存聚合前的），载入编辑窗口，编辑完成后保存图片。  
   + *截图过程*
     软件待机界面中，有截图与gif两个按钮。  
     鼠标右键拉出截图窗口对角线。  
   + *图片编辑器*  
     和QQ基本一致  
     常规画笔：自由画笔，矩形，（椭）圆形，箭头指向，文字。  
     提供画笔调色板、笔触大小（三个程度）。  
     图片有外框，拖动外框进行裁剪。  
     完成、取消按钮。点击完成，进入保存流程。  
   + *保存形式*  
     编辑完成后，开始保存。详细见下文第`2.`项。  
   + gif的编辑器有关于帧的选项  
     比如在哪些帧编辑，保存时可以选择帧。选择形式如：`1,2,3-4`，统一英文字符。  
     截图大小每一帧都是统一的。  
   + 使用统一的编辑窗口，单张图片的编辑时，设定帧是唯一的，且不可选帧的范围。  


2. 图片管理  
同步github图床，显示图片集，可以增删查改（显示的图片即以图床的链接获取图片，本地不存图片文件）  
   + 使用sqlite作为数据库，存储图片信息，主要为外链信息。  
   + 同一github库中，可以建立多个图床，用目录区分  
   + 图片管理的用户端，用图库来归纳管理图床，一个图库可以包含多个图床。  

