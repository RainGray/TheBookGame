from pydantic import BaseModel
#from bson import ObjectId

class Todo(BaseModel):
    
    title: str
    description: str

class PageText(BaseModel):
    textID: str
    page_title: str
    illustration: str
    text: str
    replys: list[str]

class Reply(BaseModel):
    replyID: str
    text: str
    textID: str