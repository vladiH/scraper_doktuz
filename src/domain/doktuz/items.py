# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy.loader.processors import TakeFirst

class DoktuzItem(scrapy.Item):
    codigo = Field(output_processor=TakeFirst())
    fecha = Field(output_processor=TakeFirst())
    empresa = Field(output_processor=TakeFirst())
    subcontrata = Field(output_processor=TakeFirst())
    proyecto = Field(output_processor=TakeFirst())
    t_exam = Field(output_processor=TakeFirst())
    paciente = Field(output_processor=TakeFirst())
    imp = Field(output_processor=TakeFirst())
    cookie = Field(output_processor=TakeFirst())
