#!python2
#coding: utf-8
from bs4 import BeautifulSoup
from collections import namedtuple
import requests
import sys

BASE_URL_STR = u"http://www.rmbs.es/catalogo.php?criterio="
SEARCH_BUTTON_STR = u"&boton=Buscar"
ALPHABET_LST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', u'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
BOM_UTF8_LEN = 3

def performRequest(url):
   result = requests.post(url)
   trimmed_result = result.content[BOM_UTF8_LEN:]
   return BeautifulSoup(trimmed_result, 'html.parser')

def searchKeyword(criteria):
   page_number = 1
   book_list = []
   while True:
      soup = performRequest(BASE_URL_STR + criteria + SEARCH_BUTTON_STR + "&pg=" + str(page_number))
      if page_number == 1:
         result_info = soup.find("p", { "class" : "resultado" })
         num_results = result_info.text.split()[4]
         num_results = int(num_results)
      bookcase = soup.find("ul", { "id" : "cajalibros" })
      books = bookcase.findAll("li")
      for book in books:
         Book = namedtuple("Book", "title author url")
         title = book.find("span", { "class" : "titulocondicionado" })
         author = book.find("span", { "class" : "autor" })
         url = book.find("a")["href"]
         b = Book(title, author, url)
         book_list.append(b)
      if len(book_list) < num_results:
         page_number += 1
      else:
	     break
   print result_info.text

def promptForInput():
   print u"Buscar título por palabra clave:"
   print u"[0] para salir"
   print u"[A-Z] para buscar autores por orden alfabético"
   user_input = raw_input("> ")
   criteria = "+".join(user_input.split()).decode(sys.stdin.encoding)
   if criteria == "0":
      print "Hasta luego!"
   elif criteria.upper() in ALPHABET_LST:
      print "Buscar por autor"
   else:
      searchKeyword(criteria)
      promptForInput()

promptForInput()
