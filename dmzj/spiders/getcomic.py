# -*- coding: utf-8 -*-
import scrapy
import re
from dmzj.items import comicInfoItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select



class GetcomicSpider(scrapy.Spider):
    name = 'getcomic'
    allowed_domains = ['manhua.dmzj.com','www.dmzj.com','images.dmzj.com']
    start_urls = []
    for i in range(1,2):
        url = 'https://www.dmzj.com/category/1-0-0-0-0-0-'+str(i)+'.html'
        start_urls.append(url)


    def parse(self, response):
        item = comicInfoItem()

        item['comicname'] = response.css('.comic_list_det h3 a::text').extract()
        #item['comicinfo'] = response.css('.comic_list_det p::text').extract()
        item['comic_url'] = response.css('.comic_list_det h3 a::attr(href)').extract()
        
        for i in range(0,len(item['comicname'])):
            #print(item['comicname'][i]+item['comic_url'][i])
            yield scrapy.Request(url=item['comic_url'][i],callback=self.parse_chapter,meta={'comicname':item['comicname'][i]}) 

    def parse_chapter(self,response):
        item = comicInfoItem()
        list1=[]
        list2=[]
        url1 = 'https://www.dmzj.com/view/'
        urls = response.css(' li a::attr(href)').extract()
        for url in urls:
            if url1 in url:
                list1.append(url)
        for i in list1:
            if i not in list2:
                list2.append(i)
        item['chapter_url']=list2
        print(len(item['chapter_url']))
        item['comicname'] = response.meta['comicname']
        print(item['comicname'])
        #取得章节url
        for chapter in item['chapter_url']:
            yield scrapy.Request(url=chapter,callback=self.parse_page,meta={'comicname':item['comicname']})

    def parse_page(self,response):
        #executable_path指定了chromedriver所在的路径,程序运行时就会到该路径下启动chrome浏览器
        #browser = webdriver.Chrome(executable_path = 'C:/Users/yy/AppData/Local/Google/Chrome/Application/chromedriver.exe')
        browser = webdriver.PhantomJS()
        item = comicInfoItem()
        item['chapter_name'] = response.css('.head_title h2::text').extract()[0]
        item['comicname']=response.meta['comicname']
        #item['x'] = response.css('(.comic_wraCon autoHeight)').extract()
        #item['x'] = response.xpath('//@src').extract()
        #print(response.url)
        #url = response.url+'1'
        #yield scrapy.Request()

        #selenium
        pages = []
        text = []
        browser.get(response.url)
        #print(browser.page_source)
        for e in browser.find_elements_by_css_selector('#page_select>option'):
            value_url = e.get_attribute('value')
            value_text = e.get_attribute('text')
            item['image_urls'] = [value_url]
            item['image_name'] = value_text
            pages.append(value_url)
            text.append(value_text)
            yield item
            #print(value)
        #print('111111111111111111111111111111111111111111111111111111111111111\n')
        #print(pages)
        #print(text)
        #item['image_urls'] = pages
        #item['image_name'] = text
        browser.close()
        #lis = browser.find_element(By.ID,"select")
        #print(lis)
        
        
        #yield item
