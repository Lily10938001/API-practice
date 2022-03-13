# API-practice
learning how to use flask, RESTful API, Swagger document......
including : 
1. ## 將在yahoo finance api查詢到的API串接到自己的網域(127.0.0.1)
     檔案 : 串接API到自己的網域.ipynb
2. ## 串接MYSQL資料到自己的網域,並直接透過修改網域名稱對資料庫進行動作(RESTful API的特色)
     檔案 : app.py、user.py
   ### 工具一－MAMP: 
   - https://www.mamp.info/en/windows/
   - 可以快速連線到PhpMyadmin網頁(127.0.0.1:3306)
   - 按開關”Start Servers”　→　按中間”Open Webstart Page”　→　"開啟PhpMyAdmin"
   ### 工具二－POSTMAN:
   - https://www.postman.com/downloads/
   - 類似瀏覽器,貼上url就可以針對所串的資料(如:MYSQL資料庫)執行GET、POST、DELETE....等功能
3. ## 利用Flask建立一個購物車API, 須包含以下功能 :
   - PUT或是PATCH 去新增或刪減存貨, 並能及時算出購物車內的價錢
   - 需有login API, 並將除了login之外的API 加入jwt_token
   - 讓所有API(除了login需有4隻以上)撰寫在swagger文件(類似postman功能的網頁) 
   ### 檔案 : 
   - app.py --- 定義flask架構以及執行整個程式
   - item.py --- 定義執行各種method的詳細功能(對MySQL資料庫做什麼事)
   - item_swagger_model.py --- 設定在GET/POST時所需提交的parameter/form data,以及Response的訊息文字預設內容及型別
   - msng.py --- 設定在GET/POST成功或失敗時的訊息文字(Response Body)
