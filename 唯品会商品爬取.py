# made by wang 
import re
import requests
import pandas as pd
import urllib.parse

#获取商品ID（PID）
def PID_api(product_name,page):
    global PID_1
    global PID_2    
    PID_1=[]
    PID_2=[]
    product_encoding_name = urllib.parse.quote_plus(product_name) 
    for i in range(page):
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Referer': 'https://category.vip.com/suggest.php?keyword={}&ff=235%7C12%7C1%7C1&page={}'.format(product_encoding_name,i+1),
            }
        params = {
            'callback':'getMerchandiseDroplets1',
            'app_name':'shop_pc',
            'app_version':'4.0',
            'warehouse':'VIP_NH',
            'fdc_area_id':'104104101',
            'client':'pc',
            'mobile_platform':'1',
            'province_id':'104104',
            'api_key':'70f71280d5d547b2a7bb370a529aeea1',
            'user_id':'',
            'mars_cid':'1613703548698_2c0d5f6421da1850d82050160fcab2a7',
            'wap_consumer':'a',
            'standby_id':'nature',
            'keyword':'{}'.format(product_name),
            'lv3CatIds':'',
            'lv2CatIds':'',
            'lv1CatIds':'',
            'brandStoreSns':'',
            'props':'',
            'priceMin':'',
            'priceMax':'',
            'vipService':'',
            'sort':'0',
            'pageOffset':'{}'.format(120*i),
            'channelId':'1',
            'gPlatform':'PC',
            'batchSize':'120',
            '_':'1613803856391',
            }   
        response = requests.get(url,headers=headers,params=params)
        PID = re.findall('"pid":"(\d+)"', response.text,re.S)
        PID_1.append(list(PID))
        PID_2.extend(list(PID))
#获取商品品牌ID（BID）
def BID_api(product_name,page):
    product_encoding_name = urllib.parse.quote_plus(product_name)
    global BID
    BID = [] 
    for PID in PID_1:    
        for i in range(3):
            if i == 0:
                PID_k = PID[0:50]
            elif i == 1:
                PID_k = PID[50:100]
            else :
                PID_k = PID[100:120]
            pro_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
                'Referer': 'https://category.vip.com/suggest.php?keyword={}&ff=235%7C12%7C1%7C1&page={}'.format(product_encoding_name,page),
                }
            params = {
                'callback':'getMerchandiseDroplets1',
                'app_name':'shop_pc',
                'app_version':'4.0',
                'warehouse':'VIP_NH',
                'fdc_area_id':'104104101',
                'client':'pc',
                'mobile_platform':'1',
                'province_id':'104104',
                'api_key':'70f71280d5d547b2a7bb370a529aeea1',
                'user_id':'',
                'mars_cid':'1613703548698_2c0d5f6421da1850d82050160fcab2a7',
                'wap_consumer':'a',
                'productIds':'{}'.format(','.join(PID_k)),
                'scene':'search',
                'standby_id':'nature',
                'extParams':'{"stdSizeVids":"","preheatTipsVer":"3","couponVer":"v2","exclusivePrice":"1","iconSpec":"2x"}',
                'context':'',
                '_':'1613746757133',
                }
            response = requests.get(pro_url,headers=headers,params=params)
            content_6 = re.findall('"brandId":"(.*?)"', response.text,re.S)
            BID.extend(list(content_6))
#获取商品价格详细信息
def prodect_detail_1(PID_BID,product_name): 
    list_all_content = []
    for i in list(PID_BID.items()):
        url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/detail/v5'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Referer': 'https://detail.vip.com/detail-{}-{}.html'.format(i[0],i[1]),
        }
        params = {
            'callback':'detailInfoCB',
            'app_name':'shop_pc',
            'app_version':'4.0',
            'warehouse':'VIP_NH',
            'fdc_area_id':'104104101',
            'client':'pc',
            'mobile_platform':'1',
            'province_id':'104104',
            'api_key':'70f71280d5d547b2a7bb370a529aeea1',
            'user_id':'',
            'mars_cid':'1613703548698_2c0d5f6421da1850d82050160fcab2a7',
            'wap_consumer':'a',
            'productId':'{}'.format(i[0]),
            'functions':'brand_store_info,newBrandLogo,hideOnlySize,extraDetailImages,sku_price,ui_settings',
            'kfVersion':'1',
            'highlightBgImgVer':'1',
            'is_get_TUV':'',
            'commitmentVer':'1',
            'mitmentVer':'2',
            'haitao_description_fields':'text',
            'supportSquare':'1',
            'longTitleVer':'2',
            'propsVer':'1',
            }
        response = requests.get(url,headers=headers,params=params)
        content_0 = re.findall('"title":"(.*?)"', response.text,re.S)
        content_1 = re.findall('"specialPrice":"(.*?)"', response.text,re.S)
        content_2 = re.findall('"vipshopPrice":"(.*?)"', response.text,re.S)
        content_3 = re.findall('"agio":"(.*?)"', response.text,re.S) 
        content_4 = re.findall('"marketPrice":"(.*?)"', response.text,re.S)
        content_5 = re.findall('"merchandiseSn":"(.*?)"', response.text,re.S)
        all_content = zip(content_0,content_1,content_2,content_3,content_4,content_5)
        for r in all_content:   
            list_all_content.append(list(r))
    df = pd.DataFrame(list_all_content,columns=['商品标题','特售售价','折后售价','折扣数','市场价','商品货号'])
    df.to_excel(excel_writer = '唯品会{}详细商品数据.xlsx'.format(product_name),encoding='utf-8-sig',index=False)
if __name__ == '__main__' :    
    product_name = input('请输入你要查询的商品名称:')
    page = int(input('请输入你要查询多少页：'))
    PID_api(product_name,page)
    BID_api(product_name,page)
    PID_BID = dict(zip(PID_2,BID))
    prodect_detail_1(PID_BID,product_name)


