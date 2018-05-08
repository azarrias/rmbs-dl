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
#         print str(len(book_list)) + ") " + title.text.encode('utf-8') + " [" + author.text.encode('utf-8') + "]"
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

if sys.platform == "win32":
    import codecs
    from ctypes import WINFUNCTYPE, windll, POINTER, byref, c_int
    from ctypes.wintypes import BOOL, HANDLE, DWORD, LPWSTR, LPCWSTR, LPVOID

    original_stderr = sys.stderr

    # If any exception occurs in this code, we'll probably try to print it on stderr,
    # which makes for frustrating debugging if stderr is directed to our wrapper.
    # So be paranoid about catching errors and reporting them to original_stderr,
    # so that we can at least see them.
    def _complain(message):
        print >>original_stderr, message if isinstance(message, str) else repr(message)

    # Work around <http://bugs.python.org/issue6058>.
    codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

    # Make Unicode console output work independently of the current code page.
    # This also fixes <http://bugs.python.org/issue1602>.
    # Credit to Michael Kaplan <http://www.siao2.com/2010/04/07/9989346.aspx>
    # and TZOmegaTZIOY
    # <http://stackoverflow.com/questions/878972/windows-cmd-encoding-change-causes-python-crash/1432462#1432462>.
    try:
        # <http://msdn.microsoft.com/en-us/library/ms683231(VS.85).aspx>
        # HANDLE WINAPI GetStdHandle(DWORD nStdHandle);
        # returns INVALID_HANDLE_VALUE, NULL, or a valid handle
        #
        # <http://msdn.microsoft.com/en-us/library/aa364960(VS.85).aspx>
        # DWORD WINAPI GetFileType(DWORD hFile);
        #
        # <http://msdn.microsoft.com/en-us/library/ms683167(VS.85).aspx>
        # BOOL WINAPI GetConsoleMode(HANDLE hConsole, LPDWORD lpMode);

        GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(("GetStdHandle", windll.kernel32))
        STD_OUTPUT_HANDLE = DWORD(-11)
        STD_ERROR_HANDLE = DWORD(-12)
        GetFileType = WINFUNCTYPE(DWORD, DWORD)(("GetFileType", windll.kernel32))
        FILE_TYPE_CHAR = 0x0002
        FILE_TYPE_REMOTE = 0x8000
        GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(("GetConsoleMode", windll.kernel32))
        INVALID_HANDLE_VALUE = DWORD(-1).value

        def not_a_console(handle):
            if handle == INVALID_HANDLE_VALUE or handle is None:
                return True
            return ((GetFileType(handle) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR
                    or GetConsoleMode(handle, byref(DWORD())) == 0)

        old_stdout_fileno = None
        old_stderr_fileno = None
        if hasattr(sys.stdout, 'fileno'):
            old_stdout_fileno = sys.stdout.fileno()
        if hasattr(sys.stderr, 'fileno'):
            old_stderr_fileno = sys.stderr.fileno()

        STDOUT_FILENO = 1
        STDERR_FILENO = 2
        real_stdout = (old_stdout_fileno == STDOUT_FILENO)
        real_stderr = (old_stderr_fileno == STDERR_FILENO)

        if real_stdout:
            hStdout = GetStdHandle(STD_OUTPUT_HANDLE)
            if not_a_console(hStdout):
                real_stdout = False

        if real_stderr:
            hStderr = GetStdHandle(STD_ERROR_HANDLE)
            if not_a_console(hStderr):
                real_stderr = False

        if real_stdout or real_stderr:
            # BOOL WINAPI WriteConsoleW(HANDLE hOutput, LPWSTR lpBuffer, DWORD nChars,
            #                           LPDWORD lpCharsWritten, LPVOID lpReserved);

            WriteConsoleW = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, DWORD, POINTER(DWORD), LPVOID)(("WriteConsoleW", windll.kernel32))

            class UnicodeOutput:
                def __init__(self, hConsole, stream, fileno, name):
                    self._hConsole = hConsole
                    self._stream = stream
                    self._fileno = fileno
                    self.closed = False
                    self.softspace = False
                    self.mode = 'w'
                    self.encoding = 'utf-8'
                    self.name = name
                    self.flush()

                def isatty(self):
                    return False

                def close(self):
                    # don't really close the handle, that would only cause problems
                    self.closed = True

                def fileno(self):
                    return self._fileno

                def flush(self):
                    if self._hConsole is None:
                        try:
                            self._stream.flush()
                        except Exception as e:
                            _complain("%s.flush: %r from %r" % (self.name, e, self._stream))
                            raise

                def write(self, text):
                    try:
                        if self._hConsole is None:
                            if isinstance(text, unicode):
                                text = text.encode('utf-8')
                            self._stream.write(text)
                        else:
                            if not isinstance(text, unicode):
                                text = str(text).decode('utf-8')
                            remaining = len(text)
                            while remaining:
                                n = DWORD(0)
                                # There is a shorter-than-documented limitation on the
                                # length of the string passed to WriteConsoleW (see
                                # <http://tahoe-lafs.org/trac/tahoe-lafs/ticket/1232>.
                                retval = WriteConsoleW(self._hConsole, text, min(remaining, 10000), byref(n), None)
                                if retval == 0 or n.value == 0:
                                    raise IOError("WriteConsoleW returned %r, n.value = %r" % (retval, n.value))
                                remaining -= n.value
                                if not remaining:
                                    break
                                text = text[n.value:]
                    except Exception as e:
                        _complain("%s.write: %r" % (self.name, e))
                        raise

                def writelines(self, lines):
                    try:
                        for line in lines:
                            self.write(line)
                    except Exception as e:
                        _complain("%s.writelines: %r" % (self.name, e))
                        raise

            if real_stdout:
                sys.stdout = UnicodeOutput(hStdout, None, STDOUT_FILENO, '<Unicode console stdout>')
            else:
                sys.stdout = UnicodeOutput(None, sys.stdout, old_stdout_fileno, '<Unicode redirected stdout>')

            if real_stderr:
                sys.stderr = UnicodeOutput(hStderr, None, STDERR_FILENO, '<Unicode console stderr>')
            else:
                sys.stderr = UnicodeOutput(None, sys.stderr, old_stderr_fileno, '<Unicode redirected stderr>')
    except Exception as e:
        _complain("exception %r while fixing up sys.stdout and sys.stderr" % (e,))


    # While we're at it, let's unmangle the command-line arguments:

    # This works around <http://bugs.python.org/issue2128>.
    GetCommandLineW = WINFUNCTYPE(LPWSTR)(("GetCommandLineW", windll.kernel32))
    CommandLineToArgvW = WINFUNCTYPE(POINTER(LPWSTR), LPCWSTR, POINTER(c_int))(("CommandLineToArgvW", windll.shell32))

    argc = c_int(0)
    argv_unicode = CommandLineToArgvW(GetCommandLineW(), byref(argc))

    argv = [argv_unicode[i].encode('utf-8') for i in xrange(0, argc.value)]

    if not hasattr(sys, 'frozen'):
        # If this is an executable produced by py2exe or bbfreeze, then it will
        # have been invoked directly. Otherwise, unicode_argv[0] is the Python
        # interpreter, so skip that.
        argv = argv[1:]

        # Also skip option arguments to the Python interpreter.
        while len(argv) > 0:
            arg = argv[0]
            if not arg.startswith(u"-") or arg == u"-":
                break
            argv = argv[1:]
            if arg == u'-m':
                # sys.argv[0] should really be the absolute path of the module source,
                # but never mind
                break
            if arg == u'-c':
                argv[0] = u'-c'
                break

    # if you like:
    sys.argv = argv
	  
while True:
   command = userPrompt(["EXIT", "BROWSE_AUTHORS", "SEARCH_KEYWORDS"])
