from llone_parser import *

'''
Grammar used for this parser:

list     : '[' elements ']'                          # list is composed of a LBRACK (some other elemets) an RBRACK
elements : element (',' element)* | element=element  # elements are one or more element separated by COMMA or an element ASSIGNEMENT sign and other element  
element  : NAME | list                               # element is a NAME or another list


Added control of the index of character parsed in the token list

'''

# Test Parsing a input List
input_list = "[a = b, c, df, Abc]"

lexer1 = ListLexer(input_list)
parser = ListParser(lexer1)

parser.list()
print("List elements:")
print(parser.getElements())


#Test printing all the Tokens from the input List
lexer2 = ListLexer(input_list)
token = lexer2.nextToken()

print("\nLexer tokens:")
while token.type != Lexer.EOF_TYPE:
    print(token)
    token = lexer2.nextToken()

print(token) #print the last EOF char


