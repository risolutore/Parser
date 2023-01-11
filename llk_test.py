from llk_parser import *

'''
Grammar used for this parser:

list     : '[' elements ']'                          # list is composed of a LBRACK (some other elemets) an RBRACK
elements : element (',' element)* | element=element  # elements are one or more element separated by COMMA or an element ASSIGNEMENT sign and other element  
element  : NAME '=' NAME                             # Element is a NAME assignement of a NAME
         | NAME '=' NUMBER                           # element is a NUMBER assignement to a NAME 
         | NUMBER                                    # element is a NUMBER
         | list                                      # element is a list

some xamples:
1) input_list = []
2) input_list = [a=b]
3) input_list = [a=12, b, c=1]
4) input_list = [coordx=120, coordy=10]
5) input_list = [a=1, b=3, c=ab]


Output: 
Parsing actions are translated in literal readable scripting lang
'''


input_list = "[a=5, b=12, coord]"

lexer = ListLexer(input_list)
parser = ListParser(lexer)

parser.list()


