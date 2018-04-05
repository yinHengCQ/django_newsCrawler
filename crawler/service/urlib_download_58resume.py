#coding=utf-8
import time,re,base64,pytesseract,urllib2,logging
from lxml import etree
from fontTools.ttLib import TTFont
from PIL import ImageFont,ImageDraw,Image
from crawler.models import Resume58


pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"
__logger=logging.getLogger('django')

def download_data(url):
    __logger.info('start download 58 resume,current url is:{0}'.format(url))
    start_time=time.time()
    try:
        # url = "http://cq.58.com/searchjob/pn{0}/".format(page_index)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        request = urllib2.Request(url=url, headers=headers)
        page = urllib2.urlopen(request).read()
        if etree.HTML(page).xpath('//div[@id="infolist"]/ul[1]/li') != []:
            get_data(__trans_page(page, __get_dict(page)))
        else:
            time.sleep(3);download_data(url)
    except Exception as error:
        __logger.error('download 58 resume error:{0}'.format(error))
    finally:
        __logger.info('task 58 resume finish,times count:{0}'.format(time.time()-start_time))


def __get_dict(page):
    orgin = re.search(r';base64,(.+)\)', page).group(1)
    fontdata = base64.b64decode(orgin[:orgin.rfind(')')])
    file = open(r'C:\Users\Administrator\PycharmProjects\django_newsCrawler\crawler\service\temp.ttf', 'wb')
    file.write(fontdata)
    file.close()
    font = TTFont(r'C:\Users\Administrator\PycharmProjects\django_newsCrawler\crawler\service\temp.ttf')
    cmaps = font.getBestCmap()

    ft = ImageFont.truetype(r'C:\Users\Administrator\PycharmProjects\django_newsCrawler\crawler\service\temp.ttf', 300)
    temp_dict = {}

    for k, v in cmaps.items():
        im02 = Image.open(r"C:\Users\Administrator\PycharmProjects\django_newsCrawler\crawler\service\block.png")
        ImageDraw.Draw(im02).text((70, 0), unichr(k), font=ft, fill='black')
        temp_dict['&#x{0};'.format(v[3:].lower())] = pytesseract.image_to_string(im02, lang='chi_sim',config='--psm 8').replace('_','').replace('T','1').strip()
    return temp_dict

def __trans_page(page,temp_dict):
    for j, k in temp_dict.items():
        page = page.replace(j, k.encode('utf-8'))
    return page


def get_data(page):
    path_list = etree.HTML(page).xpath('//div[@id="infolist"]/ul[1]/li')
    for var in path_list:
        resume_id = re.search(r'&dpid=(.+)&', var.xpath('div[@class="fl"][1]/dl[1]/dt[1]/a[1]/@href')[0]).group(1)
        name = var.xpath('@username')[0].encode('utf-8')
        sex = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/div[1]/a[1]/div[1]/div[1]/em[1]/text()')[0].encode('utf-8')
        age = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/div[1]/a[1]/div[1]/div[1]/em[2]/text()')[0].encode('utf-8')
        work_age = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/div[1]/a[1]/div[1]/div[1]/em[3]/text()')[0].encode('utf-8')
        education = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/div[1]/a[1]/div[1]/div[1]/em[4]/text()')[0].encode('utf-8')
        try:hope_job = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/p[1]/span[1]/@title')[0].encode('utf-8')
        except:hope_job=''
        try:now_job = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/p[1]/em[2]/@title')[0].encode('utf-8')
        except:now_job = ''
        try:hope_work_address = var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/p[@class="placeDesire"][1]/span[1]/@title')[0].encode('utf-8')
        except:hope_work_address=''
        try:mark = ''.join(em.xpath('text()')[0] + '|' for em in var.xpath('div[@class="fl"][1]/dl[1]/dd[1]/div[@class="infocardMark clearfix"][1]/em'))[:-1].encode('utf-8')
        except:mark=''

        try:Resume58.objects.update_or_create(resume_id=resume_id,name=name,sex=sex,age=age,work_age=work_age,education=education,
                                              hope_job=hope_job,now_job=now_job,hope_work_address=hope_work_address,mark=mark)
        except Exception as e:
            __logger.error('update_or_create resume58 error:{0}'.format(e))