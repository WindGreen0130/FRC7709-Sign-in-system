import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import time
from datetime import datetime
import gspread
import pathlib
cap = cv2.VideoCapture(0)
exe_path = pathlib.Path(__file__)
file_path = r"C:\Users\MIL\Desktop\gcsys-411617-ea253eddf949.json" 
sa =    gspread.service_account(filename=file_path) #讀取json金鑰
sh = sa.open("簽到系統賽季版本")    #開啟試算表
wks = sh.worksheet("工作表1")      #選擇工作表
k = []
code_to_name = {
"1106230007709":"溫德葛林柳如風",
    "1104150007700":"昕",
    "2102030007702":"吉吉祥",
    "1102420007702":"Train",
    "2105230007701":"塗嘉祥",
    "2101290007705":"李政叡",
    "1106690007707":"鄭余先",
    "1101980007702":"潔瓜",
    "2104610007706":"傅",
    "1103370007705":"bird",
    "1106360007709":"歐弟",
    "2101140007701":"李宜瑾",
    "2102360007700":"洪宇柏",
    "2103170007706":"莊佳恩",
    "2103660007704":"陳立勛",
    "1104080007702":"Aurora",
    "2100750007705":"吳宜臻",
    "1106760007705":"Hennes",
    "2104170007703":"陳昱豐",
    "1101790007701":"林大可",
    "2105400007708":"Hz",
    "1107930007709":"RJ",
    "1103780007702":"許均皓",
    "2102000007701":"林庭旭"
}
nametime = {
"溫德葛林柳如風":[False,False,False],
"昕":[False,False,False],
"吉吉祥":[False,False,False],
"Train":[False,False,False],
"塗嘉祥":[False,False,False],
"李政叡":[False,False,False],
"鄭余先":[False,False,False],
"潔瓜":[False,False,False],
"傅":[False,False,False],
"bird":[False,False,False],
"歐弟":[False,False,False],
"李宜瑾":[False,False,False],
"洪宇柏":[False,False,False],
"莊佳恩":[False,False,False],
"陳立勛":[False,False,False],
"Aurora":[False,False,False],
"吳宜臻":[False,False,False],
"Hennes":[False,False,False],
"陳昱豐":[False,False,False],
"林大可":[False,False,False],
"Hz":[False,False,False],
"RJ":[False,False,False],
"許均皓":[False,False,False],
"林庭旭":[False,False,False]
}


def boxSize(arr):
    global data
    box_roll = np.rollaxis(arr,1,0)
    xmax = int(np.amax(box_roll[0]))
    xmin = int(np.amin(box_roll[0]))
    ymax = int(np.amax(box_roll[1]))
    ymin = int(np.amin(box_roll[1]))
    return (xmin,ymin,xmax,ymax)

qrcode = cv2.barcode_BarcodeDetector()             # QRCode 偵測器

while True:
    
    now = datetime.now().strftime("%H")
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    img = cv2.resize(frame,(720,420))     # 縮小尺寸，加快速度
    ok, data, data_type, bbox = qrcode.detectAndDecode(img) 
    if ok:
        for i in range(len(data)):
            text = data[i]            # QRCode 內容
            box = boxSize(bbox[i])    # QRCode 座標
            cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,0,255),5)  # 繪製外框
            print(text)       # 印出 QRCode 內容            
            print(code_to_name[text])  # 印出 QRCode 內容對應的名字
            print(nametime[code_to_name[text]][0],nametime[code_to_name[text]][1],nametime[code_to_name[text]][2])  # 印出 QRCode 內容對應的名字的出席狀況
            if int(now) < 12:
                nametime[code_to_name[text]][0] = True #早上的出席調整為True
            elif int(now)>=12 and int(now)< 18:
                nametime[code_to_name[text]][1] = True #下午的出席調整為True
            else:
                nametime[code_to_name[text]][2] = True #晚上的出席調整為True
    cv2.imshow('sign in', img)
    if cv2.waitKey(1) == ord('q'):      # 按下 q 鍵退出
        break
cap.release()
cv2.destroyAllWindows()
c = int(wks.acell("A26").value) # 讀取目前的欄位數
print(c)
t = datetime.now().strftime("%m/%d")
wks.update_cell(1,c,t+'早上')   # 更新第一行的時間
wks.update_cell(1,c+1,t+'下午') # 更新第一行的時間
wks.update_cell(1,c+2,t+'晚上') # 更新第一行的時間
a = 2
for i in nametime:          # 讀取每一個人的出席狀況
    if nametime[i][0] == True:
        wks.update_cell(a,c,True)       # 更新每一個人的出席狀況
    else:
        wks.update_cell(a,c,False)
    if nametime[i][1] == True:
        wks.update_cell(a,c+1,True)
    else:
        wks.update_cell(a,c+1,False)
    if nametime[i][2] == True:
        wks.update_cell(a,c+2,True)
    else:
        wks.update_cell(a,c+2,False)
    a+=1
    time.sleep(10) #避免更新過快導致免費版的API流量不足
wks.update("A26",c+3)           # 更新下次的欄位數