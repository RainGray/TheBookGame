from multiprocessing.connection import wait
from pydoc import doc
from xml.dom.minidom import Document
from model import Todo, PageText, Reply
#import sys
import logging

# mongoDB driver
import motor.motor_asyncio
import pymongo
import motor


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.TheBookGame
collection_texts = database.get_collection('PageText')
collection_replys = database.get_collection('Replys')




#============================Create Database Data=================================

async def create_page_text(page_text):
    document = page_text
    result = await collection_texts.insert_one(document)
    return document

async def create_reply(reply):
    document = reply
    result = await collection_replys.insert_one(document)
    return document


#===========================Updating Database Data================================

async def update_the_current_page_record(page: PageText):
    checker = await collection_texts.find_one({"textID": 'current_page'})
    if checker:
        logging.info(f'Checker {checker} was created')
    else:
        logging.error("Error while creating ckecker!")
        try:
            blank = await create_page_text({"textID": 'current_page'})
        except:
            logging.error('Error while creating blank page instead of ckecker')
        else:
            logging.info(f"Blank page was created: {blank}")
    
    await collection_texts.replace_one({"textID": 'current_page'}, {
        "textID": page.textID,
        "page_title": page.page_title,
        "illustration": page.illustration,
        "text": page.text,
        "replys": page.replys
    })
    document = await fetch_the_text('current_page')
    logging.info(f'So eventually we get the: {document}')
    return document


#============================Page Text functions==================================

async def fetch_the_text(textID):
    document = await collection_texts.find_one({"textID": textID})
    return document






#============================Replys functions=====================================

async def fetch_reply_by_replyid(replyID):
    document = await collection_replys.find_one({"replyID": replyID})
    return document 




async def fetch_multiple_replys_by_id_list(idList: list):
    logging.info("We are at the database function fetch_multiple_replys_by_id_list")   
    logging.info(f'Our list is: {idList}')  
    cursor = []
    logging.info(f'Our cursor is: {cursor}')
    for replyID in idList:
         logging.info(f'Current replyID: {replyID}')
         next_reply = await collection_replys.find_one({"replyID": replyID})
         logging.info(f'We get the {next_reply} for ID {replyID}') 
         cursor.append(next_reply)

    return cursor
        


async def fetch_multiple_replys_by_id_list_alt(idList: list):
    query = {
        "replyID": {
            "$in": idList,
        }
    }
    output = []
    try:    
        #the_replies = await collection_replys.find({'replyID': 'test'})
        the_replies = collection_replys.find(query)
        for reply in await the_replies.to_list(length=100):
            #logging.info(f'Next reply: {reply}')
            output.append(reply)
    except:
        logging.error('!!!!!!!! Error while fetching multiple replys by id list')
    else:
        logging.info(f'We are retrive multiple replys by id list: {output}')
        return output








"""
async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {
        "description": desc
    }} )
    document = collection.finde_one({"titile": title})
    return document

async def remove_todo(title):
    try:
        await collection.delete_one({"title": title})
        result = True
    except:
        result = False
        raise Exception(f"Object {title} not found in database")
    return result
"""

