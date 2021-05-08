import lexer2020
import sys
import re

if len(sys.argv) < 2:
    print("Please enter a file name.")
    sys.exit()
    
with open(sys.argv[1], 'r') as infile:
    #open the source file



    lines = list(line for line in (l.strip() for l in infile) if line)
    #remove empty lines

tokenss = [] 
for text in lines:
    #traverse each line independently

   
        #seperate comments from code and discard
    if '/*' in text and '*/' in text:
        s = text.find('/*')
        t = text[s+2:]
        u = t.find('*/')
        v = (s+2) + (u+2)
        str_split = text[:s] + text[v:]
        results = lexer2020.run('Testfile(1).txt', str_split)
        for result in results:
    
            tokenss.append(result)
        continue

    elif '/*' in text:
        str_split = text.split("/*", 1)[0]
        results = lexer2020.run('Testfile(1).txt', str_split)
        for result in results:
    
            tokenss.append(result)
        continue

    elif '*/' in text:
        
        str_split = text.split("*/", 1)[1]
        results = lexer2020.run('Testfile(1).txt', str_split)
        for result in results:
            
            tokenss.append(result)
        continue
 
    elif '//' in text:
    
        str_split = text.split("//", 1)[0]
        results = lexer2020.run('Testfile(1).txt', str_split)
        for result in results:
        
            tokenss.append(result)
        continue

    else:
        
        results = lexer2020.run('Testfile(1).txt', text)
        for result in results:
            
            tokenss.append(result)
infile.close()
###################################################################################################################
#Main class for parsing
MULTOP = ['*', '/']
ADDOP = ['+', '-']
RELOP = ['<=', '>=', '==', '!=', '<', '>']

fun_dec = {}
glob_var = {}
local_var = {}


class Declar:
  def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
  def __repr__(self):
        if self.value: return "{0}{1}".format(self.type, self.value)
        return '{0}'.format(self.type)
 
##########################################################################################
  @staticmethod
  def parse():
    global funT
    global iR
    if len(tokenss) == 0:
        if 'main' in fun_dec:
            print("ACCEPT")
        else:
           print( tokenss )
           sys.exit()
    elif ((tokenss[0].value == 'int' or tokenss[0].value == 'void') and tokenss[1].type == 'ID: ' and tokenss[2].value == '('):
        x = tokenss[1].value
        y = tokenss[0].value
        z = 0
        fun_dec[x] = {}
        del(tokenss[0:3])
        local_var['return'] = y
        var = Declar.params(fun_dec, x, z)
        if tokenss[0].value == '{':
            del(tokenss[0])
            Declar.cmpnd_stm()
            if tokenss[0].value == '}':
                del(tokenss[0])
                local_var.clear()
                Declar.parse()
            else:
               print( tokenss )
               sys.exit()
        else:
            print( tokenss )
            sys.exit()
    elif tokenss[0].value == 'int' and tokenss[1].type == 'ID: ':
        a = tokenss[1].value
        del(tokenss[0:2])
        Declar.var_dec(glob_var, a)
        Declar.parse()
    else:
        print( tokenss )
        sys.exit()
#####################################################################################################################
  @staticmethod
  def var_dec(new_var, a):
      if a not in new_var:
            new_var[a] = {'kind': 'int'}
            if tokenss[0].value == ';':
                del(tokenss[0])
                return
            elif (tokenss[0].value == '[' and tokenss[1].type == 'NUM: ' 
                  and tokenss[2].value == ']' and tokenss[3].value == ';'):
                    new_var[a] = {'type': 'int', 'kind': 'array', 'size': tokenss[1].value}
                    del(tokenss[0:4])
                    return
            else:
                print( tokenss )
                sys.exit()
      else:
            print( tokenss )
            sys.exit()
########################################################################################################
#Function to check params
  @staticmethod
  def params(fun_dec, x, z):
     a = tokenss[1].value
     local_var.update(glob_var)
     if tokenss[0].value == 'int' and tokenss[1].type == 'ID: ':
        z += 1
        fun_dec[x][z] = {'id': tokenss[1].value, 'kind': 'int'}
        local_var[a] = {'kind': 'int'}
        del(tokenss[0:2])
        if tokenss[0].value == '[' and tokenss[1].value == ']':
            fun_dec[x][z]['kind'] = 'array'
            local_var[a]['kind'] = 'int'
            del(tokenss[0:2])
        if tokenss[0].value == ',':
            del(tokenss[0])
            Declar.params(fun_dec, x, z)
            return
        elif tokenss[0].value == ')':
            del(tokenss[0])
            return()
        else:
            print( tokenss )
            sys.exit()
     elif tokenss[0].value == 'void' and tokenss[1].value == ')':
        
        del(tokenss[0:2])
        return
     else:
        print( tokenss )
        sys.exit()
####################################################################################################################
#Function to proccess compound statement components
  @staticmethod                  
  def cmpnd_stm():

        if tokenss[0].value == 'int' and tokenss[1].type == 'ID: ':
            a = tokenss[1].value
            del(tokenss[0:2])
            Declar.var_dec(local_var, a)
            Declar.cmpnd_stm()
        elif tokenss[0].value == '}':
            return
        else:
            Declar.statement()
            Declar.cmpnd_stm()
##########################################################################################################
#statement analyzer
  @staticmethod
  def statement():
    if tokenss[0].value == 'if':
        del(tokenss[0])
        Declar.selection_stm()
        if tokenss[0].value == 'else':
            del(tokenss[0])
            Declar.selection_else()
            return
        else:
            Declar.statement()
            return
    if tokenss[0].value == 'while':
        Declar.iter_stm()
        return
    elif tokenss[0].value == 'return':
        del(tokenss[0])
        Declar.ret_stm()
        return
    elif tokenss[0].value == '{':
        del(tokenss[0])
        Declar.cmpnd_stm()
        if tokenss[0].value == '}':
            del(tokenss[0])
            return
        else:
            print( tokenss )
            sys.exit()
    elif tokenss[0].value == '}':
        return
    else:
        Declar.expression_stm()
        return
##########################################################################################################
#expression statement
  @staticmethod
  def expression_stm():
    
    if tokenss[0].value == ';':
        del(tokenss[0])
        return
    else:
        Declar.expression()
        if tokenss[0].value == ';':
            del(tokenss[0])
            return
        else:
            print( tokenss )
            sys.exit()
##########################################################################################################
#selection statement analyzer
  @staticmethod
  def selection_stm():
    if tokenss[0].value == '(':
        del(tokenss[0])
        Declar.sim_ex()
        if tokenss[0].value == ')':
            del(tokenss[0])
            Declar.statement()
            return
        else:
            print( tokenss )
            sys.exit()
    else:
        print( tokenss )
        
        sys.exit()
############################################################################################################
#selection else
  @staticmethod
  def selection_else():

    Declar.statement()
    return
##########################################################################################################
#itteration staement analyzer
  @staticmethod
  def iter_stm():
      
    if tokenss[0].value == 'while' and tokenss[1].value == '(':
        del(tokenss[0:2])
        Declar.sim_ex()
        if tokenss[0].value == ')':
            del(tokenss[0])
            Declar.statement()
            return
        else:
            print( tokenss )
            sys.exit()
    else:
        print( tokenss )
        sys.exit()
###########################################################################################################
#return statement
  @staticmethod
  def ret_stm():
    if tokenss[0].value == ';' and local_var['return'] == 'void':
        del(tokenss[0])
        return
    else:
        if local_var['return'] == 'int':
            Declar.add_ex()
            if tokenss[0].value == ';':
                del(tokenss[0])
                return
            else:
                print( tokenss )
                sys.exit()
        else:
            print( tokenss )
            sys.exit()
#########################################################################################################
#expression evaluator
  @staticmethod
  def expression():
    a = tokenss[0].value
    if tokenss[0].type == 'ID: ' and tokenss[1].value == '=' and a in local_var:
        local_var[a] = {'kind': 'int'}
        del(tokenss[0:2])
        Declar.expression()
        return
    elif tokenss[0].type == 'ID: ' and tokenss[1].value == '[' and tokenss[4].value == '=' and a in local_var and local_var[a]['kind'] == 'array':
        del(tokenss[0:2])
        if tokenss[0].type == 'NUM: ':
            if tokenss[0].value < local_var[a]['size']:
                del(tokenss[0])
            else:
                print( tokenss )
                sys.exit()
        else:
            Declar.factor()
        if tokenss[0].value == ']' and tokenss[1].value == '=':
            local_var[a] = {'kind': 'array'}
            del(tokenss[0:2])
            Declar.expression()
            return
    else:
        Declar.sim_ex()
        return
#######################################################################################################################
#simple expression evaluator
  @staticmethod
  def sim_ex():
        
        Declar.add_ex()
        if tokenss[0].value in RELOP:
            del(tokenss[0])
            return
        else:
            return
######################################################################################################################
#additive expression evaluator
  @staticmethod
  def add_ex():
        
        Declar.term()
        if tokenss[0].value in ADDOP: 
            del(tokenss[0])
            Declar.add_ex()
        else:
            return
#####################################################################################################################
#term evaluator
  @staticmethod
  def term():
        
        Declar.factor()
        if tokenss[0].value in MULTOP: 
            del(tokenss[0])
            Declar.term()
        else:
            return
########################################################################################################################
#factor evaluator
  @staticmethod
  def factor():
    a = tokenss[0].value
    if tokenss[0].value == '(':
        del(tokenss[0])
        Declar.add_ex()
        if tokenss[0].value == ')':
            del(tokenss[0])
            return
        else:
            print( tokenss )
            sys.exit()
    elif tokenss[0].type == 'ID: ' and tokenss[1].value == '(':
        fun_call = {}
        x = tokenss[0].value
        if x in fun_dec:
            fun_call[x] = {}
            del(tokenss[0:2])
            z = 0
            Declar.call(fun_call, x, z)
            if tokenss[0].value == ')':
                del(tokenss[0])
                return
            else:
                print( tokenss )
                sys.exit()
        else:
            print( tokenss )
            sys.exit()
    elif tokenss[0].type == 'ID: ' and tokenss[1].value == '[' and a in local_var and local_var[tokenss[0].value]['kind'] == 'array':
            a = tokenss[0].value
            del(tokenss[0:2])
            ##if tokenss[0].type == 'NUM: ' and tokenss[0].value < local_var[a]['size']:
                ##del(tokenss[0])
            ##else:
            Declar.add_ex()
            if tokenss[0].value == ']':
                del(tokenss[0])
                return
            else:
                print( tokenss )
                sys.exit()
    elif tokenss[0].type == 'ID: ' and a in local_var and local_var[tokenss[0].value]['kind'] != 'array':
        del(tokenss[0])
        return
    elif tokenss[0].type == 'NUM: ':
        del(tokenss[0])
        return
    else:
        print( tokenss )
        sys.exit()
######################################################################################################################
#Call evaluator
  @staticmethod
  def call(fun_call, x, z):
    
    if tokenss[0].value == ')':
        if len(fun_call[x]) == len(fun_dec[x]):
            return
        else:
            print("REJECT")
            sys.exit()
    else:
        z += 1
        i = tokenss[0].value
        if len(fun_call[x]) > len(fun_dec[x]):
            print( tokenss )
            sys.exit()
        if i in local_var :
            fun_call[x][z]= {'id': i}
            fun_call[x][z]['kind'] = local_var[i]['kind']
        else:
            print("REJECT ")
            sys.exit()
        if fun_call[x][z]['kind'] == fun_dec[x][z]['kind']:
            if fun_call[x][z]['kind'] == 'array':
                del(tokenss[0])
            else:
                Declar.add_ex()
        else:
            print( tokenss )
            sys.exit()
        
        if tokenss[0].value == ',':
            del(tokenss[0])
            Declar.call(fun_call, x, z)
            return
        elif tokenss[0].value == ')' and len(fun_call[x]) == len(fun_dec[x]):
            return
        else:
            print( tokenss )
            sys.exit()

Declar.parse()
