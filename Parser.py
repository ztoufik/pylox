
class Expression:

    def __init__(self):
        pass

class BinaryExpresssion(Expression):
    
    def __init__(self,left,right,operator):
        super().__init__()
        self.left=left
        self.right=right
        self.operator=operator

class UnaryExpression(Expression):
    
    def __init__(self,right,operator):
        super().__init__()
        self.right=right
        self.operator=operator

class Literal(Expression):
    
    def __init__(self,value):
        super().__init__()
        self.value=value

class Grouping(Expression):
    
    def __init__(self,expression):
        super().__init__()
        self.expression=expression
