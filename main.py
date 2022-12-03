import fastapi

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import time
import pytz

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

start_time = time.time()
count = 0

    

df = pd.read_csv('databases/database.csv')


print('init values: ', start_time, count)


def setvalue(qr, confirm):
    global start_time
    global count
    global df
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    
    #print(time_string)
    
    if qr is None:
        print('QR is None')
        return None
    
    try:
        previous = df.loc[df['QR']==qr, ['Name','Confirm']].iloc[0].to_dict()

        df.loc[df['QR'] == qr, 'Confirm'] = confirm
    except:
        print('Lỗi index')
        return None
    if time.time() - start_time > 2:
        df.to_csv('databases/confirm.csv')
        df.to_csv('databases/log/log{}.csv'.format(count))
        start_time = time.time()
        count +=1
        print('Saved log', count -1,'at', time_string)
    else:
        print('No save')
    
    
    return previous

templates = Jinja2Templates(directory="templates")    

app = fastapi.FastAPI()


@app.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})

@app.get('/confirm/{values}', response_class=HTMLResponse)
async def get_from_qr(request: Request, values: str):
    
    msg ='Unvalued'
    try:
        values = values.split('&')
        qr = values[0]
        confirm = values[1]
    except:
        return 'Try not modify.'
    
    previous = setvalue(qr, confirm)
    print(previous)
    if confirm.lower() =='no':
        msg1 = 'Thật tiếc khi bạn không thể tham dự chương trình.'
        msg2 =  'Nếu vì một lý do khách quan nào, hãy liên lạc ngay với chúng mình để được trợ giúp nhé!'
        msg3 ='' 
    elif confirm.lower() =='unknown':
        msg1 = 'Cảm ơn bạn đã xác nhận'
        msg2 = 'Hy vọng có thể gặp bạn tại chương trình "'
        msg3 = "Happy Birthday To Jesus 4 - No Room"
    else:
        msg2 = 'Hẹn gặp tại chương trình "'
        msg3 = "Happy Birthday To Jesus 4 - No Room"
        if previous['Confirm'].lower() in ['no','unknown']:
            msg1 = 'Cảm ơn bạn đã đổi ý.'
            
        else:
            msg1 = 'Cảm ơn bạn đã xác nhận.'
            
    
    #print(msg)
    

    return templates.TemplateResponse("index.html", 
                                        {"request": request, 
                                        "name": previous['Name'], 
                                        "msg1": msg1, 
                                        "msg2": msg2, 
                                        "msg3": msg3})
    
    
    



    
