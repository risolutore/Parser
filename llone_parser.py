from abc import ABC, abstractmethod
from typing import List, Match

######################################
# CLASSE:  TOKEN                      #
######################################
class Token:
    def __init__(self, type, text, index):
        self.type = type
        self.text = text
        self.index = index

    def toString(self):
        token_name = ListLexer.tokenNames[self.type]
        return f"<'{self.text}', {token_name}, '{self.index}'>"

    def __str__(self) -> str:
        token_name = ListLexer.tokenNames[self.type]
        return f"<'{self.text}', {token_name}, '{self.index}'>"
    


######################################
# CLASS:  LEXER                      #
######################################
class Lexer(ABC):
    EOF = -1
    EOF_TYPE = 1
    carattere_corrente = 0
    carattere = ""

    def __init__(self, input) -> None:
        self.input = input
        self.carattere = input[self.carattere_corrente]
    
    def consume(self) -> None:
        self.carattere_corrente += 1
        if self.carattere_corrente >= len(self.input):
            self.carattere = self.EOF
        else:
            self.carattere = self.input[self.carattere_corrente]

    def match(self, x) -> None:
        if self.carattere == x:
            self.consume()
        else:
            raise Exception("Atteso " + str(x) + "; invece era " + str(self.carattere))

    @abstractmethod
    def nextToken(self):
        pass

    @abstractmethod
    def getTokenName(self, tokenType):
        pass



######################################
# CLASS:  LISTLEXER                  #
######################################
class ListLexer(Lexer):
    NAME = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5
    ASSIGNEMENT = 6
    tokenNames = ['n/a', '<EOF>', 'NAME', 'COMMA', 'LBRACK', 'RBRACK', 'ASSIGNEMENT']
    lettere = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, input) -> None:
        super().__init__(input)
    
    def isLETTER(self) -> bool:
        if self.carattere in self.lettere or self.carattere in self.lettere.upper():
            return True
        else:
            return False

    def getTokenName(self, tokenType):
        #return super().getTokenName(tokenType)
        return self.tokenNames[tokenType]

    def nextToken(self) -> Token:
        #return super().nextToken()
        while self.carattere != self.EOF:
            if self.carattere in [' ', '\t', '\n', '\r']:
                self.WS()
            elif self.carattere == ',':
                self.consume()
                return Token(self.COMMA, ',', self.carattere_corrente)
            elif self.carattere == '[':
                self.consume()
                return Token(self.LBRACK, '[', self.carattere_corrente)
            elif self.carattere == ']':
                self.consume()
                return Token(self.RBRACK, ']', self.carattere_corrente)
            elif self.carattere == '=':
                self.consume()
                return Token(self.ASSIGNEMENT, '=', self.carattere_corrente)
            else:
                if self.isLETTER():
                    return self.Name()
                else:
                    raise Exception("Carattere non valido " + str(self.carattere))

        return Token(self.EOF_TYPE, '<EOF>', self.carattere_corrente + 1)

    def Name(self) -> Token:
        buf = ""
        while self.isLETTER():
            buf += self.carattere
            self.consume()
        
        return Token(self.NAME, buf, self.carattere_corrente)
    
    def WS(self):
        while self.carattere in [' ', '\t', '\n', '\r']:
            self.consume()



######################################
# CLASS:  PARSER                     #
######################################
class Parser(ABC):
    def __init__(self, input) -> None:
        self.input = input
        self.lookahead = self.input.nextToken()

    def match(self, x) -> None:
        if self.lookahead.type == x:
            self.consume()
        else:
            raise Exception("Atteso " + self.input.getTokenName() + "; trovato " + str(self.lookahead))
    
    def consume(self) -> None:
        self.lookahead = self.input.nextToken()



######################################
# CLASS:  LISTPARSER                 #
######################################
class ListParser(Parser):
    elem = []

    def __init__(self, input) -> None:
        super().__init__(input)

    def list(self) -> None:
        self.match(ListLexer.LBRACK)
        self.elements()
        self.match(ListLexer.RBRACK)
    
    def elements(self) -> None:
        self.element()
        if self.lookahead.type == ListLexer.ASSIGNEMENT:
            self.match(ListLexer.ASSIGNEMENT)
            self.element()
        while self.lookahead.type == ListLexer.COMMA:
            self.match(ListLexer.COMMA)
            self.element()
            if self.lookahead.type == ListLexer.ASSIGNEMENT:
                self.match(ListLexer.ASSIGNEMENT)
                self.element()
    
    def element(self) -> None:
        if self.lookahead.type == ListLexer.NAME:
            self.elem.append(self.lookahead.text)
            self.match(ListLexer.NAME)
        elif self.lookahead.type == ListLexer.LBRACK:
            self.list()
        else:
            raise Exception("Atteso NOME o LISTA; trovato " + str(self.lookahead))

    def getElements(self):
        return self.elem
    
