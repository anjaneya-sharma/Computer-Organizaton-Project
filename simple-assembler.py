import sys
from sys import stdin

opcodes={"add":"10000","sub":"10001","mov":"10010","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"11001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}

Reg_dict={"r0":"000","r1":"001","r2":"010","r3":"011","r4":"100","r5":"101","r6":"110","flags":"111"}

Reg_typ_A=["add","sub","mul","xor","or","and"]
Reg_typ_B=["mov","rs","ls"]
Reg_typ_C=["mov","div","not","cmp"]
Reg_typ_D=["ld","st"]
Reg_typ_E=["jmp","jlt","jgt","je"]
Reg_typ_F=["hlt"]

Flags=["0","0","0","0"] #(V,L,G,E)

Reg_val=["0","0","0","0","0","0","0","0"]

def flag_setter(v=0,l=0,g=0,e=0):
    Flags[0]=str(v)
    Flags[1]=str(l)
    Flags[2]=str(g)
    Flags[3]=str(e)
    #setting value of flag register
    Reg_val[7]="000000000000"+Flags[0]+Flags[1]+Flags[2]+Flags[3]


def func_typ_A(argument):
    if argument[0]=="add":
        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])

        if re1+re2>65535:
            Reg_val[int(argument[3][1:])]=str((re1+re2)%(2**16))
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[3][1:])]=str(re1+re2)

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]
        
    elif argument[0]=="sub":
        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])

        if re1-re2<0:
            Reg_val[int(argument[3][1:])]="0"
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[3][1:])]=re1-re2
            

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]
        
    elif argument[0]=="mul":

        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])

        if re1*re2>65535:
            Reg_val[int(argument[3][1:])]=str((re1*re2)%(2**16))
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[3][1:])]=str(re1*re2)
            
        
        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="xor":
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        Reg_val[int(argument[1][1:])]=re2^re3
        
        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="or":
        
        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])

        Reg_val[int(argument[3][1:])]=re1|re2

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="and":
        
        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])

        Reg_val[int(argument[3][1:])]=re1 & re2

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

def func_typ_B(argument,current_line):
    if argument[0]=="mov":
        reg=int(argument[1][1:])
        imm=int(argument[2][1:])
        Reg_val[reg]=imm
        var=str((bin(imm))[2:]).zfill(8)
        return opcodes[argument[0]]+Reg_dict[argument[1]]+var

    
    elif argument[0]=="ls":
        r1=int(Reg_val[int(argument[1][1:])])    
        imm=int(argument[2][1:])
        Reg_val[int(argument[1][1:])]=r1<<imm

        return opcodes[argument[0]]+Reg_dict[argument[1]]+str((bin(imm))[2:].zfill(8)) 
    
    
    elif argument[0]=="rs":
        r1=int(Reg_val[int(argument[1][1:])])    
        imm=int(argument[2][1:])
        Reg_val[int(argument[1][1:])]=r1>>imm

        return opcodes[argument[0]]+Reg_dict[argument[1]]+str((bin(imm))[2:].zfill(8))



def func_typ_C(argument):
    
    if argument[0]=="mov": #mov register
        
        try:
            
            re1=int(Reg_val[int(argument[1][1:])])
            Reg_val[int(argument[2][1:])]=str(re1)
            
            return "10011"+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]
    
        except ValueError:
            re1=int(Reg_val[7])
            Reg_val[int(argument[2][1:])]=str(re1)

            return '10011'+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]
        
    elif argument[0]=="div":
        
        re3=int(Reg_val[int(argument[1][1:])])
        re4=int(Reg_val[int(argument[2][1:])])
        
        if (re4==0):
            print("Error at line {} : Division By Zero Error".format(current_line))
            return -1

        else:
            Reg_val[0]=str(re3//re4)
            Reg_val[1]=str(re3%re4)

            return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]


    elif argument[0]=="not":
        re1=int(Reg_val[int(argument[1][1:])])
        re2=str(~re1)
        
        Reg_val[int(argument[2][1:])]=re2

        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]
    
    
    elif argument[0]=="cmp":
        re1=int(Reg_val[int(argument[1][1:])])
        re2=int(Reg_val[int(argument[2][1:])])
        if re1==re2:
            Flags[3]="1"
        elif re1>re2:
            Flags[2]="1"
        elif re1<re2:
            Flags[1]="1"
        
        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]



def func_typ_D(argument,lno):
    rval=Reg_dict[argument[1]]
    memadd=str(bin(lno))
    memadd=memadd[2:]
    mem=memadd.zfill(8)
    op=opcodes[argument[0]]
    # flag_setter()
    
    reg=argument[1]
    var=argument[2]

    my_var=bin(cnt+list_var.index(var))[2:].zfill(8)

##    if argument[0] =="ld":
##        Reg_val[int(reg[1:])]=var_val[var]

##    elif argument[0]=="st":
##        var_val[var] =Reg_val[int(reg[1:])]

##    return op+rval+mem

    return op+rval+my_var


def func_typ_E(argument):

    if argument[0]=='jlt':
        return '01100'+'000'+bin(label_mem_dict[argument[1]])[2:].zfill(8)
    elif argument[0]=='jgt':
        return '01101'+'000'+bin(label_mem_dict[argument[1]])[2:].zfill(8)
    elif argument[0]=='je':
        return '01111'+'000'+bin(label_mem_dict[argument[1]])[2:].zfill(8)
    elif argument[0]=='jmp':
        return '11111'+'000'+bin(label_mem_dict[argument[1]])[2:].zfill(8)

def func_typ_F(argument):
    if argument[0]=="hlt":
        return opcodes["hlt"]+"00000000000"

def is_valid_register(register):

    list_of_registers=list(Reg_dict.keys())
    
    if register=='flags':
        print("Error at line {} : illegal use of flag registers".format(current_line))
        return False

    if register not in list_of_registers:
        if register[0]=='r':
            print("Error at line {} : invalid register name".format(current_line))
            return False
        print("Error at line {} : General Syntax Error".format(current_line))
        return False
    
    return True

def is_valid_immediate(immediate):
    
    if immediate[0]!='$':
        print("Error at line {} : invalid immediate".format(current_line))
        return False
    
    try:
        immediate=int(immediate[1:])

        if immediate>=256 or immediate<0:
            print("Error at line {} : illegal immediate value".format(current_line))
            return False

    except:
        print("Error at line {} : General Syntax Error".format(current_line))
        return False
    
    return True

def is_valid_variable(variable):

    if variable not in list_var:
        if variable in list_label:
            print('Error at line {}: Misuse of label as variable'.format(current_line))
            return False
        print('Error at line {}: Undefined variable'.format(current_line))
        return False
    
    return True


def check_typeA(instruction):

    if len(instruction)!=4:
        print('Error at line {} : General Syntax Error'.format(current_line))
        return False
    
    if not is_valid_register(instruction[1])  or not is_valid_register(instruction[2]) or not is_valid_register(instruction[3]):
        return False

    return True

def check_typeB(instruction):

    if len(instruction)!=3:
        print('Error at line {} : General Syntax Error'.format(current_line))
        return False
    
    if not is_valid_register(instruction[1]) or not is_valid_immediate(instruction[2]):
        return False

    return True

def check_typeC(instruction):
    
    if len(instruction)!=3:
        print('Error at line {} : General Syntax Error'.format(current_line))
        return False

    if not is_valid_register(instruction[1])  or not is_valid_register(instruction[2]):
        return False
    
    return True


def check_typeD(instruction):

    if len(instruction)!=3:
        print('Error at line {} : General Syntax Error'.format(current_line))
        return False

    if not is_valid_register(instruction[1]) or not is_valid_variable(instruction[2]):
        return False

    return True


def check_typeE(instruction):
    
    if len(instruction)>2:
        print("Error at line {} : General Syntax Error".format(current_line))
        return False

    if instruction[1] not in list_label:
        if instruction[1] in list_var:
            print("Error at line {} : Misuse of variable as label".format(current_line))
            return False
        print("Error at line {} : Unidentified label".format(current_line))
        return False

    return True

def check_mov(instruction):

    list_of_registers=list(Reg_dict.keys())

    if len(instruction)!=3:
        print('Error at line {} : General Syntax Error'.format(current_line))
        return False

    if instruction[1] not in list_of_registers:
        if instruction[1][0]=='r':
            print('Error at line {} : invalid register name'.format(current_line))
            return False
        else:
            print('Error at line {} : General Syntax Error'.format(current_line))
            return False

    if instruction[1] in list_of_registers:
        if instruction[2] in list_of_registers:
            if instruction[2]=='flags':
                print('Error at line {} : Illegal use of flags register'.format(current_line))
                return False
            else:
                return True
        elif instruction[2][0]!='$':
            if instruction[2][0]=='r':
                print('Error at line {} : invalid register name'.format(current_line))
                return False
            print('Error at line {} : General Syntax Error'.format(current_line))
            return False

        else:
            if instruction[1]=='flags':
                print('Error at line {} : Illegal use of flags register'.format(current_line))
                return False
            try:
                temp=int(instruction[2][1:])
                if temp>=256 or temp<0:
                    print('Error at line {} : illegal immediate value'.format(current_line))
                    return False
            except ValueError:
                print('Error at line {} : General Syntax Error'.format(current_line))
                return False
                
    return True

def check_errors(code):

    global Reg_typ_A
    global Reg_typ_B
    global Reg_typ_C
    global Reg_typ_D
    global Reg_typ_E
    
    global current_line
    current_line=0

    global list_var
    list_var=[]
    count_var=0

    global list_label
    list_label=label_mem_dict.keys()

    global count_hlt
    count_hlt=0

    for line in code:

        current_line+=1

        if line[0]=='var':
            
            count_var+=1

            if count_var!=current_line:
                print('Error at line {} : Variable not declared at the beginning'.format(current_line))
                continue

            if len(line)!=2:
                print('Error at line {} : General Syntax Error'.format(current_line))
                continue
            
            if line[1] in list_var:
                print('Error at line {} : Variable declared before'.format(current_line))
                continue

            if line[1] not in list_var:
                if line[1] in list_label:
                    print('Error at line {} : Misuse of label as variable'.format(current_line))
                    continue
                list_var.append(line[1])

        elif line[0]=='mov':

            if check_mov(line)==False:
                continue

            if line[2] in list(Reg_dict.keys()):
                print(func_typ_C(line))
            else:
                print(func_typ_B(line,current_line))

        elif line[0] in Reg_typ_A:

            if check_typeA(line)==False:
                continue
            print(func_typ_A(line))

        elif line[0] in Reg_typ_B:
            
            if check_typeB(line)==False:
                continue
            print(func_typ_B(line,current_line))

        elif line[0] in Reg_typ_C:

            if check_typeC(line)==False:
                continue
            if (func_typ_C(line))==-1:
                continue
            else:
                print(func_typ_C(line))

        elif line[0] in Reg_typ_D:

            if check_typeD(line)==False:
                continue
            print(func_typ_D(line,current_line))

        elif line[0] in Reg_typ_E:
            
            if check_typeE(line)==False:
                continue
            print(func_typ_E(line))

        elif line[0]=='hlt':

            if len(line)!=1:
                print("Error at line {} : General Syntax Error".format(current_line))
            
            count_hlt+=1

            if count_hlt>1:
                print("Error at line {} : hlt not being used as the last instruction".format(hlt_line))
            
            hlt_line=current_line

        else:
            print("Error at line {} : Illegal instruction name".format(current_line))
    
    if count_hlt==0:
        print("Error at line {} : missing hlt instruction".format(current_line))
    
    if count_hlt==1:
        print(func_typ_F(['hlt']))

def main():

    global code
    
    code=[]
    
    for line in stdin :
        if line=="":
            break
        code.append(line.lower().split())

    while [] in code:
        code.remove([])

    global var_val
    var_val={}

    global label_mem_dict
    label_mem_dict={}
    j=-1

    for i in code:
        j+=1
        if i[0].find(':')!=-1:
            label_mem_dict[i[0][:len(i[0])-1]]=j
            code[code.index(i)]=code[code.index(i)][1:]
        if i[0]=='var':
            j-=1
            
    
    code=[i for i in code if i!=[]]

    global cnt
    cnt=0
    for i in code:
        if i[0]!='var':
            cnt+=1
        
    check_errors(code)

main()
