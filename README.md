# Miliui Crawler 「彩虹ui插件整合包」爬蟲

自動下載「奇樂」網頁的「[彩虹ui插件整合包](https://addons.miliui.com/show/1/all)」(此為魔獸世界【暗影之境】專用插件)，可加入電腦排程，自動判斷是否有更新檔案上傳，如有則自動下載。

## 安裝

建議使用 [Pipenv](https://github.com/pypa/pipenv) 安裝。

```Shell
pipenv install
```

## 執行

```Shell
pipenv run python main.py
```

## 說明

下載的檔案會儲存至 [`download`](./download) 資料夾，如有同名檔案則將舊檔案改名(加上時間戳)。

會藉由判斷[網頁](https://addons.miliui.com/show/1/all#download)下方檔案表格內的"上傳時間"，與本地 [`config.ini`](config.ini) 檔案內紀錄最新檔案日期比較，如網頁上有更新的檔案或新檔案則下載

## 定時執行

如果想要自動定時檢查是否有更新檔，Windows 可以使用"工作排程器"；linux 可以使用"crontab"。
