# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,headers={'Referer':'https://manhua.dmzj.com/'},meta={'comicname':item['comicname'],'chapter_name':item['chapter_name'],'image_name':item['image_name']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        #item['image_paths'] = image_paths
        return item

    def file_path(self,request,response=None,info=None):
        #item=request.meta['item'] #通过上面的meta传递过来item
        comicname=request.meta['comicname'] 
        chapter_name=request.meta['chapter_name'] 
        image_name=request.meta['image_name']+'.jpg'
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        
        image_guid = request.url.split('/')[-1] #image_guid就是之前图片那个hash值，改成把url通过‘/’分割后的最后一部分，就是**.jpg
        filename = u'full/{0}/{1}/{2}'.format(comicname,chapter_name,image_name) 
        #return 'full/%s' %(image_guid)
        return filename