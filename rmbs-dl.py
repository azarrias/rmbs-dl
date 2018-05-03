#!python2
#coding: utf-8
from bs4 import BeautifulSoup
import requests
import sys

BASE_URL_STR = u"http://www.rmbs.es/catalogo.php?criterio="
SEARCH_BUTTON_STR = u"&boton=Buscar"
ALPHABET_LST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', u'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
BOM_UTF8_LEN = 3

def searchKeyword(str):
   result = requests.post(BASE_URL_STR + str + SEARCH_BUTTON_STR)
   decoded_result = result.content[BOM_UTF8_LEN:]
   soup = BeautifulSoup(decoded_result, 'html.parser')
   result_info = soup.find("p", { "class" : "resultado" })
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
