#from urllib import response
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import  PageText, Reply
#import uvicorn 


#=====logger libs======
import logging
#from uicheckapp.services import EchoService
from requests import Request
import random
import string
import time



from database import (

    fetch_the_text,
    #fetch_replys_for_page,
    create_page_text,
    create_reply,
    fetch_reply_by_replyid,
    fetch_multiple_replys_by_id_list,
    fetch_multiple_replys_by_id_list_alt

)



# setup loggers
#logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logging.basicConfig(filename='.\example.log', encoding='utf-8', level=logging.DEBUG)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.






#app object
app = FastAPI()



origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#=============logger======================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response





@app.get("/")
def read_root():
    logging.info('you are visiting main page')
    return {"Ping": "Pong"}
    


#============================Create Database Data=================================

@app.post("/api/add_page_text", response_model=PageText)
async def post_page_text(page_text: PageText):
    response = await create_page_text(page_text.dict())
    if response:
        return response       
    else:
        raise HTTPException(400, "Error while trying to add page text data in database")

@app.post("/api/add_reply", response_model=Reply)
async def post_reply(reply: Reply):
    response = await create_reply(reply.dict())
    if response:
        return response
    else:
        raise HTTPException(400, "Error while trying to add reply data in database")





#============================Page Text functions==================================

@app.get("/api/get_page_text/{textID}", response_model=PageText)
async def get_page_text(textID: str):
    response = await fetch_the_text(textID)
    if response:
        return response
    else:
        logger.info('404, Can not find the page text info')
        raise HTTPException(404, 'Can not find the page text info')






#============================Replys functions=====================================

@app.get("/api/get_reply_by_id/{replyID}", response_model=Reply)
async def get_reply_by_id(replyID: str):
    response = await fetch_reply_by_replyid(replyID)
    if response:
        return response
    else:
        logging.error(f'Error during the response fetch by id - searched id: {replyID}')
        raise HTTPException(404, 'Can not find reply  by its ID')


@app.get("/api/get_page_replys/{textID}", response_model=list[Reply])
async def get_replys_for_page(textID: str):
    page_text = await get_page_text(textID)
    
    #convert our PageText to dictionary
    try:
        replys_names = dict(page_text)
    except:
        logging.error(f'Error while getting replys list from {page_text}')
        
    #extract list with replys from dictionary
    try:
        replys_list = replys_names['replys']
    except:
        logging.error(f'cant extract list of replys from {replys_names}')
    
    #fetching all replies from DB according to our list
    replys_for_page = await fetch_multiple_replys_by_id_list(replys_list)
    return replys_for_page



@app.get("/api/test_fetching", response_model=list[Reply])
async def test_fetch():
    response = await fetch_multiple_replys_by_id_list_alt(['begin_reply_01', 'begin_reply_02', 'begin_reply_03'])
    return response
        







"""
@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    else:
        raise HTTPException(404, f'There is no todo with {title} title')




@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    else:
        raise HTTPException(400, "Error while trying to update data in database")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return f"The {title} todo is successfully deleted!"
    else:
        raise HTTPException(404, f"There is no todo with name {title}")
"""