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
OPTIONS = { "BROWSE_AUTHORS" : u"[A-Z] para buscar autores por orden alfabético",
   "SEARCH_KEYWORDS" : u"Cualquier cadena para búsqueda por palabras clave",
   "EXIT" : u"[0] para salir",
   "DISPLAY_MORE" : u"[P] para visualizar otra página de títulos",
   "DISPLAY_ALL" : u"[T] para visualizar todo (puede tardar según criterio)",
   "DOWNLOAD" : u"Número a la izquierda del título para descargarlo",
   "DOWNLOAD_ALL" : u"[D] para descargar todos los títulos devueltos" }
STR_QUIT = u"Hasta luego!"
MESSAGE_STR = [u"[A-Z] para buscar autores por orden alfabético", u"Cualquier cadena para búsqueda por palabras clave", 
   u"[0] para salir", u"[P] para visualizar otra página de títulos", u"[T] para visualizar todo (puede tardar según criterio)",
   u"Número a la izquierda del título para descargarlo", u"[D] para descargar todos los títulos devueltos", u"Hasta luego!", 
   u"Buscar por autor", ""]

def performRequest(url):
   result = requests.post(url)
   trimmed_result = result.content[BOM_UTF8_LEN:]
   return BeautifulSoup(trimmed_result, 'html.parser')

def searchKeyword(criteria):
   page_number = 1
   book_list = []
   paginate = True
   soup = performRequest(BASE_URL_STR + criteria + SEARCH_BUTTON_STR + "&pg=" + str(page_number))
   result_info = soup.find("p", { "class" : "resultado" })
   num_results = result_info.text.split()[4]
   print result_info.text + "\n"
   if len(result_info.text.split()) <= 8:
      return
   num_results = int(num_results)   
   while True:
      soup = performRequest(BASE_URL_STR + criteria + SEARCH_BUTTON_STR + "&pg=" + str(page_number))
      bookcase = soup.find("ul", { "id" : "cajalibros" })
      books = bookcase.findAll("li")
      for book in books:
         Book = namedtuple("Book", "title author url")
         title = book.find("span", { "class" : "titulocondicionado" })
         author = book.find("span", { "class" : "autor" })
         url = book.find("a")["href"]
         b = Book(title, author, url)
         book_list.append(b)
         print str(len(book_list)) + ") " + title.text + " [" + author.text + "]"
      if paginate:
         valid_option = False
         for m in [MESSAGE_STR[i] for i in [9, 5, 6]]: print m
         if len(book_list) < num_results:
	        for m in [MESSAGE_STR[i] for i in [3, 4]]: print m
         else:
	        break
         while not valid_option:
            user_input = raw_input("> ")
            if len(book_list) < num_results and user_input.upper() == "P":
               valid_option = True
            elif len(book_list) < num_results and user_input.upper() == "T":
               paginate = False
               valid_option = True
      if len(book_list) < num_results:
         page_number += 1
      else:
         break
#elif user_input.upper() == "D":
#elif descarga titulo concreto

def userPrompt(option_list):
   for m in [OPTIONS[key] for key in option_list]: print m
   user_input = raw_input("> ")
   user_command = "+".join(user_input.split()).decode(sys.stdin.encoding)
   if user_command == "0" and "EXIT" in option_list:
      print OPTIONS["EXIT"]
      quit()
   elif user_command.upper() in ALPHABET_LST and "BROWSE_AUTHORS" in option_list:
      print u"Búsqueda por autor"
      print
   elif user_command.strip() != "" and "SEARCH_KEYWORDS" in option_list:
      print
      searchKeyword(user_command)
   else:
      print u"Opción no válida!"
      print
      userPrompt(option_list)

while True:
   command = userPrompt(["EXIT", "BROWSE_AUTHORS", "SEARCH_KEYWORDS"])
