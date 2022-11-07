from model import PageText, Reply
from main import (
    get_page_text,
    get_replys_for_page
)


starting_page = 'Begin01'
current_page: PageText
current_page = get_page_text(starting_page)

current_replies: list[Reply]
current_replies = get_replys_for_page(current_page.replys)




