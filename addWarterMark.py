# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 上午11:31
# @Author  : qq1060460048
# @File    : addWatermark.py

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#解决文件太大的问题
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import sys,os
import re

class aa(object):
    def __init__(self):
        pass

    #@params1 要处理的所有图片所在的绝对位置
    #@param2 水印图片所在的绝对位置
    def addWater(self,images,watermark):
        for root,dirs,files in images:
            for name in files:
                #判断文件大小
                file_size=os.path.getsize(os.path.join(root,name))
                if file_size == 0:#如果文件大小为0 跳出进入下次循环
                    continue
                pattern=re.compile("\.[jpg|png|gif|bmp|jpeg]&.?")
                #第三种情况文件的扩展名为空
                (filepath,tempfilename)=os.path.split(os.path.join(root,name))
                (shotname,extension)=os.path.splitext(tempfilename)
                #这里这么处理不严谨 因为如果是目录结构 目录结构根本就解析不出来扩展名，所以所有的都被忽略了
                #界定到只对文件名处理
                if re.search(pattern,name) is None:#如果出现xx.jpg&aa=xx&bb=xxx这种形式，不处理，跳出进入下次循环
                    continue
                #不是目录 但是扩展名又是空 这种文件也不合规 不处理
                elif extension is not None and len(extension)>4:#对上一种情况进一步兼容 虽然有后缀 长度不为0 但是正则没匹配到 就用后缀长度再判断
                    continue
                if name.find('.jpg') != -1 or name.find('.png') != -1 or name.find('.gif') != -1 or name.find('.jpeg') != -1:
                    imageFile = Image.open(os.path.join(root,name))
                    wm_x, wm_y = watermark.size[0], watermark.size[1]
                    #把水印加到图片中间
                    x = (imageFile.size[0] - wm_x) / 2
                    y = (imageFile.size[1] - wm_y) / 2
                    flag=None
                    #如果图片高度大于2000px
                    if y > 2000:
                        flag=True
                    position = (int(x), int(y))
                    layer=Image.new('RGBA',imageFile.size,(0,0,0,0))
                    # layer.paste(watermark,(imageFile.size[0]-600,imageFile.size[1]-400))
                    if flag:
                        #循环加水印
                        #即每隔2000px的高度加一次水印 对应上面2000判断处
                        for i in range(1,int(imageFile.size[1]/2000)):
                            position=(int(x),2000*i)
                            layer.paste(watermark,position)
                    layer.paste(watermark,position)
                    out=Image.composite(layer,imageFile,layer)
                    #以原文件名保存
                    out.save(os.path.join(root,name))
                else:
                    continue

if __name__ == '__main__':
    inclass=aa()
    aa.addWater('','')#按上面参数声明 传入相应路径