from pathlib import Path
from Tokenizer import Tokenizer
from utils import Ilogger, Result

class lox:

    def __init__(self):
        self.haderror=False
        self.Ilogger=Ilogger()

    def read_source_file(self,file_path):
        file = Path(file_path)

        if file.exists():
            return file.read_text()
        else:
            raise IOError(f"file {file_path} not found")

    def error(self,line_num,msg_str):
        self.haderror=True
        self.Ilogger.report(line_num,"",msg_str)

    def run(self,text_input):
        self.tokenizer=Tokenizer(text_input)
        tokens=self.tokenizer.scan_tokens()
        for token in tokens:
            if token[0]==Result.err:
                self.error(token[1],token[2])
            print(token)

    def run_prompt(self):
        while True:
            line=input(">")
            if line:
                self.run(line)
                self.haderror=False
            else:
                break

    def run_file(self,file_path):
        content=self.read_source_file(file_path)
        self.run(content)
        if self.haderror:
            exit(1)

def main():
    #lox().run_prompt()
    lox().run_file("test.lox")

if __name__=="__main__":
    main()
