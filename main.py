import os
import re
import time
import requests
import configparser
from bs4 import BeautifulSoup
from tool import set_logger


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
logger = set_logger()


class MiliuiCrawler():
    """「彩虹ui插件整合包」爬蟲"""
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def run(self, contents_url):
        start_time = time.time()

        download_urls = self.get_download_url(contents_url)
        logger.info(f'有 {len(download_urls)} 個檔案需要下載')
        for download_url in download_urls:
            logger.info(f'開始下載 {download_url[0]} 檔案...')

            is_success = self.download_file(file_name=download_url[0], predownload_url=download_url[2])
            if is_success:
                logger.info(f'下載 {download_url[0]} 檔案成功!!')
                self.update_record(file_name=download_url[0], update_date=download_url[1])
            else:
                logger.warning(f'下載 {download_url[0]} 檔案失敗!!')
            logger.info('---------------')

        logger.info(f'程式已執行完畢，耗時 {time.time()-start_time:.1f} 秒')
        logger.info('================='*2)

    def get_download_url(self, contents_url):
        """取得檔案黨名、更新日期、下載連結"""
        r = requests.get(contents_url, headers=HEADERS)
        if r.status_code != requests.codes.ok:
            logger.warning(f'網頁抓取失敗：{contents_url}')
            return False
        soup = BeautifulSoup(r.text, 'html.parser')

        files = []
        table_blocks = soup.select('#download tr')
        for table_block in table_blocks:
            if not table_block.select_one('td:nth-of-type(3) a'):
                continue

            file_block = table_block.select_one('td:nth-of-type(3) a')
            date_block = table_block.select_one('td:nth-of-type(7)')

            file_name = file_block.text.strip()
            file_upload_date = date_block.text.strip()
            file_download_url = file_block.get('href').strip()

            is_exist = False
            is_add = False
            for file_name_start in self.config['last_date']:
                # 檔名開頭是否存在
                if file_name.lower().startswith(file_name_start):
                    is_exist = True
                    # 判斷檔案是否有更新
                    if file_upload_date != self.config['last_date'][file_name_start]:
                        is_add = True
                    break

            # 如果沒下載過或有更新，就加入下載清單
            if not is_exist or is_add:
                files.append([file_name, file_upload_date, file_download_url])
        return files

    def download_file(self, file_name, predownload_url):
        """下載檔案"""
        s = requests.session()

        # 先抓取下載網址與 Token
        headers_ = HEADERS.copy()
        headers_['referer'] = predownload_url
        r = s.get(predownload_url, headers=headers_)
        if r.status_code != requests.codes.ok:
            logger.warning(f'網頁抓取失敗：{predownload_url}')
            return False
        soup = BeautifulSoup(r.text, 'html.parser')

        form_block = soup.select_one('form')
        if not (form_block and form_block.get('action')):
            logger.warning('找不到 download_url')
            return False
        download_url = form_block.get('action')

        token_block = soup.select_one('form input[name="_token"]')
        if not(token_block and token_block.get('value')):
            logger.warning('找不到 Token')
            return False
        download_token = token_block.get('value')

        # 主要下載檔案
        data = {'_token': download_token}
        r = s.post(download_url, headers=HEADERS, data=data)
        if r.status_code != requests.codes.ok:
            logger.warning(f'網頁抓取失敗：{download_url}')
            return False

        file_path = f'download/{file_name}'
        # 如有同名檔案則將舊檔案改名
        if os.path.isfile(file_path):
            file_ = os.path.splitext(file_path)
            re_file_path = f'{file_[0]}_{int(time.time())}{file_[1]}'
            os.rename(file_path, re_file_path)

        with open(file_path, 'wb') as f:
            f.write(r.content)
        return True

    def update_record(self, file_name, update_date):
        """更新檔案更新日期紀錄"""
        file_name_start = re.split('[-.]', file_name)[0]
        self.config['last_date'][file_name_start] = update_date
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    try:
        miliui_crawler = MiliuiCrawler()
        miliui_crawler.run('https://addons.miliui.com/show/1/all')
    except:
        logger.error("Catch an exception.", exc_info=True)
