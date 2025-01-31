from enum import Enum,auto
from dataclasses import dataclass
from os import O_NONBLOCK
from utils import Ilogger,Result

class TokenType(Enum):

    LEFT_PAREN=auto() 
    RIGHT_PAREN=auto()
    LEFT_BRACE=auto()
    RIGHT_BRACE=auto()

    COMMA=auto()
    DOT=auto()
    MINUS=auto()
    PLUS=auto()
    SEMICOLON=auto()
    SLASH=auto()
    STAR=auto()

    BANG=auto()
    BANG_EQUAL=auto()

    EQUAL=auto()
    EQUAL_EQUAL=auto()

    GREATER=auto()
    GREATER_EQUAL=auto()
    LESS=auto()
    LESS_EQUAL=auto()

    IDENTIFIER=auto()
    STRING=auto()
    NUMBER=auto()

    AND=auto()
    CLASS=auto()
    ELSE=auto()
    FALSE=auto()
    FUN=auto()
    FOR=auto()
    IF=auto()
    NIL=auto() 
    OR=auto()
    PRINT=auto()
    RETURN=auto()
    SUPER=auto()
    THIS=auto()
    TRUE=auto()
    VAR=auto()
    WHILE=auto()

    EOF=auto()
@dataclass
class Token:

    lexeme_str:str
    literal_value:object
    line_num:int
    token_type:'TokenType'

    def __init__(self,token_type,lexeme_str,literal_value,line_num):
        self.token_type=token_type
        self.lexeme_str=lexeme_str
        self.literal_value=literal_value
        self.line_num=line_num

class Tokenizer:

    def __init__(self,source_code=''):
        self.tokens=[]
        self.source_code=source_code
        self.current=self.start=0
        self.line=1
        self.Ilogger=Ilogger()
        self.keywords={}
        self.keywords["and"]=TokenType.AND
        self.keywords["class"]=TokenType.CLASS
        self.keywords["else"]=TokenType.ELSE
        self.keywords["false"]=TokenType.FALSE
        self.keywords["for"]=TokenType.FOR
        self.keywords["fun"]=TokenType.FUN
        self.keywords["if"]=TokenType.IF
        self.keywords["nil"]=TokenType.NIL
        self.keywords["or"]=TokenType.OR
        self.keywords["print"]=TokenType.PRINT
        self.keywords["return"]=TokenType.RETURN
        self.keywords["super"]=TokenType.SUPER
        self.keywords["this"]=TokenType.THIS
        self.keywords["true"]=TokenType.TRUE
        self.keywords["var"]=TokenType.VAR
        self.keywords["while"]=TokenType.WHILE

    def is_at_end(self):
        return self.current>=len(self.source_code)

    def string(self):
        while self.peek()!='"' and (not self.is_at_end()):
            if self.peek()== '\n':
                self.line+=1
            self.current+=1
        if self.is_at_end():
            return (Result.err,None)
        self.current+=1
        string_literal=self.source_code[self.start+1:self.current-1]
        return (Result.Ok,Token(TokenType.STRING,string_literal,string_literal,self.line))

    def match(self,ex_char):
        if(self.is_at_end() or self.source_code[self.current]!=ex_char):
            return False
        self.current+=1
        return True

    def number(self):
        while self.peek().isdigit():
            self.current+=1
            if self.peek()=='.' and self.peeknext().isdigit():
                self.current+=1
            while self.peek().isdigit():
                self.current+=1
        str_value=self.source_code[self.start:self.current]
        return (Result.Ok,Token(TokenType.NUMBER,str_value,str_value,self.line))

    def identifier(self):
        while self.peek().isalnum():
            self.current+=1
        text=self.source_code[self.start:self.current]
        token_type=self.keywords.get(text,None)
        if token_type:
            return (Result.Ok,Token(token_type,text,text,self.line))
        return (Result.Ok,Token(TokenType.IDENTIFIER,text,text,self.line))

    def peek(self):
        if self.is_at_end() :
            return '\0' 
        return self.source_code[self.current]

    def peeknext(self):
        if (self.current+1) >=len(self.source_code):
            return '\0'
        return self.source_code[self.current+1]

    def scan_token(self):

        if self.match('('): 
            output=(Result.Ok,Token(TokenType.LEFT_PAREN,'(',None,self.line))
        elif self.match(')'): 
            output=(Result.Ok,Token(TokenType.RIGHT_PAREN,')',None,self.line))
        elif self.match('{'): 
            output=(Result.Ok,Token(TokenType.LEFT_BRACE,'{',None,self.line))
        elif self.match('}'): 
            output=(Result.Ok,Token(TokenType.RIGHT_BRACE,'}',None,self.line))
        elif self.match(','): 
            output=(Result.Ok,Token(TokenType.COMMA,',',None,self.line))
        elif self.match('.'): 
            output=(Result.Ok,Token(TokenType.DOT,'.',None,self.line))
        elif self.match('-'): 
            output=(Result.Ok,Token(TokenType.MINUS,'-',None,self.line))
        elif self.match('+'): 
            output=(Result.Ok,Token(TokenType.PLUS,'+',None,self.line))
        elif self.match(';'): 
            output=(Result.Ok,Token(TokenType.SEMICOLON,';',None,self.line))
        elif self.match('*'): 
            output=(Result.Ok,Token(TokenType.STAR,'*',None,self.line))
        elif self.match('!'):
            if self.peek()=='=':
                output=(Result.Ok,TokenType.BANG_EQUAL);
                self.current+=1
            else:
                output=(Result.Ok,TokenType.BANG);
        elif self.match('='):
            if self.peek()=='=':
                output=(Result.Ok,Token(TokenType.EQUAL_EQUAL,'==',None,self.line))
                self.current+=1
            else:
                output=(Result.Ok,Token(TokenType.EQUAL,'=',None,self.line));
        elif self.match('<'):
            if self.peek()=='=':
                output=(Result.Ok,Token(TokenType.LESS_EQUAL,'<=',None,self.line));
                self.current+=1
            else:
                output=(Result.Ok,Token(TokenType.LESS,'<',None,self.line));
        elif self.match('>'):
            if self.peek()=='=':
                output=(Result.Ok,Token(TokenType.GREATER_EQUAL,'>=',None,self.line));
                self.current+=1
            else:
                output=(Result.Ok,Token(TokenType.GREATER,'>',None,self.line));
        elif self.match('/'):
            if self.peek()=='/':
                self.current+=1
                while(self.peek()!='\n' and not self.is_at_end()):
                    self.current+=1
                output=None
            else:
                output=(Result.Ok,Token(TokenType.SLASH,'/',None,self.line));
        elif self.match(' ') or self.match('\r') or self.match('\t'):
            output=None
        elif self.match('\n'):
            self.line+=1
            output=None
        elif self.match('"'):
            output=self.string();
        elif self.source_code[self.current].isdigit():
            output=self.number()
        elif self.source_code[self.current].isalpha():
            output=self.identifier()
        else:
            output=(Result.err,None)

        return output

    def scan_tokens(self):
        while(not self.is_at_end()):
            self.start=self.current
            token=self.scan_token()
            if token!=None:
                if token[0]==Result.err:
                    token=(Result.err,self.line,"unexpected character")
                self.tokens.append(token)
        self.tokens.append((Result.Ok,Token(TokenType.EOF,"",None,self.line)))
        return self.tokens
