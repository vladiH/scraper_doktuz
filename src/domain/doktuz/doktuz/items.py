# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class DoktuzItem(scrapy.Item):
    codigo = Field()
    fecha = Field()
    empresa = Field()
    subcontrata = Field()
    proyecto = Field()
    t_exam = Field()
    paciente = Field()
    imp = Field()
