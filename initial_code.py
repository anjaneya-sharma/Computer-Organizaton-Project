import sys
from sys import stdin

opcodes={"add":"10000","sub":"10001","mov":"10010","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"110001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"111110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}

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

def main():

    global code
    
    code=[]
    
    for line in stdin :
        if line=="":
            break
        code.append(line.lower().split())
    
    global is_erroneous
    is_erroneous=check_errors(code)

    if is_erroneous:
        return

    global var_val
    var_val={}

    curr_line=0
    for line in code:

        curr_line+=1
        
        if line[0] in Reg_typ_A:
            print(func_typ_A(line))
        elif line[0] in Reg_typ_B:
            print(func_typ_B(line))
        elif line[0] in Reg_typ_C:
            print(func_typ_C(line))
        elif line[0] in Reg_typ_D:
            print(func_typ_D(line,curr_line))
        elif line[0] in Reg_typ_F:
            print(func_typ_F(line))

    return


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
        print('Error at {} : General Syntax Error'.format(current_line))
        return False
    
    if not is_valid_register(instruction[1])  or not is_valid_register(instruction[2]) or not is_valid_register(instruction[3]):
        return False

    return True

def check_typeB(instruction):

    if len(instruction)!=3:
        print('Error at {} : General Syntax Error'.format(current_line))
        return False
    
    if not is_valid_register(instruction[1]) or not is_valid_immediate(instruction[2]):
        return False

    return True

def check_typeC(instruction):
    
    if len(instruction)!=3:
        print('Error at {} : General Syntax Error'.format(current_line))
        return False

    if not is_valid_register(instruction[1])  or not is_valid_register(instruction[2]):
        return False
    
    return True


def check_typeD(instruction):

    if len(instruction)!=3:
        print('Error at {} : General Syntax Error'.format(current_line))
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
        print('Error at {} : General Syntax Error'.format(current_line))
        return False
    
    if instruction[1] not in list_of_registers[:7]:
        if instruction[1]=='flags':
            print('Error at {} : illegal use of flag registers'.format(current_line))
            return False
        if instruction[1][0]=='r':
            print('Error at {} : invalid register name'.format(current_line))
            return False
        print("Error at line {} : General Syntax Error".format(current_line))
        return False

    if instruction[2][0]=='r' and instruction[2] not in list_of_registers:
        print('Error at {} : invalid register name'.format(current_line))
        return False

    if instruction[2][0]=='r' and instruction[2] in list_of_registers:
        return True
    
    if instruction[2][0]=='$':
        try:
            temp=int(instruction[2][1:])
            if temp>=256 or temp<0:
                print('Error at line {} : illegal immediate value'.format(current_line))
                return False
        except ValueError:
            print('Error at {} : General Syntax Error'.format(current_line))
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
    list_label=[]

    global count_hlt
    count_hlt=0

    for line in code:

        current_line+=1

        if line[0]=='var':
            
            count_var+=1

            if count_var!=current_line:
                print('Error at line {} : Variable not declared at the beginning'.format(current_line))
                return True

            if len(line)!=2:
                print('Error at line {} : General Syntax Error'.format(current_line))
                return True
            
            if line[1] in list_var:
                print('Error at line {} : Variable declared before'.format(current_line))
                return True

            if line[1] not in list_var:
                if line[1] in list_label:
                    print('Error at line {} : Misuse of label as variable'.format(current_line))
                    return True
                list_var.append(line[1])
                

        elif line[0]=='mov':

            if check_mov(line)==False:
                return True
            continue

        elif line[0] in Reg_typ_A:

            if check_typeA(line)==False:
                return True

        elif line[0] in Reg_typ_B:
            
            if check_typeB(line)==False:
                if line[0]=='mov':
                    if check_typeC(line)==True:
                        continue
                return True

        elif line[0] in Reg_typ_C:

            if check_typeC(line)==False:
                return True

        elif line[0] in Reg_typ_D:

            if check_typeD(line)==False:
                return True

        elif line[0] in Reg_typ_E:
            
            if check_typeE(line)==False:
                return True

        elif line[0].find(':')!=-1:

            if line[0].find(':')!=len(line[0])-1:
                print('Error at line {} : General Syntax Error'.format(current_line))
                return True
            
            if line[0][:len(line[0])-1] in list_label:
                print('Error at line {} : General Syntax Error'.format(current_line))
                return True
            
            if line[0][:len(line[0])-1] in list_var:
                print('Error at line {} : Misuse of variable as label'.format(current_line))
                return True
            
            list_label.append(line[0][:len(line[0])-1])

            if len(line)==1:
                continue

            if line[1:][0] in Reg_typ_A:

                if check_typeA(line[1:])==False:
                    return True
            
            elif line[1:][0] in Reg_typ_B:

                if check_typeB(line[1:])==False:
                    return True
            
            elif line[1:][0] in Reg_typ_C:

                if check_typeC(line[1:])==False:
                    return True
                
            elif line[1:][0] in Reg_typ_D:

                if check_typeD(line[1:])==False:
                    return True
            
            elif line[1:][0] in Reg_typ_E:

                if check_typeE(line[1:])==False:
                    return True
            
            elif line[1:][0]=='hlt':

                if len(line[1:])==1:
                    count_hlt+=1

                    if count_hlt>1:
                        print("Error at line {} : hlt not being used as the last instruction".format(hlt_line))
                        return True

            else:
                print("Error at line {} : General Syntax Error".format(current_line))
                return False

        elif line[0]=='hlt':

            if len(line)!=1:
                print("Error at line {} : General Syntax Error".format(current_line))
                return True
            
            count_hlt+=1

            if count_hlt>1:
                print("Error at line {} : hlt not being used as the last instruction".format(hlt_line))
                return True
            
            hlt_line=current_line

        else:
            print("Error at line {} : Illegal instruction name".format(current_line))
            return False
    
    if count_hlt==0:
        print("Error at line {} : missing hlt instruction".format(current_line))
        return True
    
    return False

def func_typ_A(argument):
    if argument[0]=="add":
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        if re2+re3>65535:
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[2][1:])]=str((re3+re2)%(2**16))

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]
        
    elif argument[0]=="sub":
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        if re2+re3<0:
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[1][1:])]="0"

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]
        
    elif argument[0]=="mul":

        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        if re2*re3>65535:
            flag_setter(1,0,0,0)
        else:
            Reg_val[int(argument[1][1:])]=str((re3*re2)%(2**16))
        
        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="xor":
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        Reg_val[int(argument[1][1:])]=re2^re3
        
        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="or":
        
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        Reg_val[int(argument[1][1:])]=re2|re3

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

    elif argument[0]=="and":
        
        re2=int(Reg_val[int(argument[2][1:])])
        re3=int(Reg_val[int(argument[3][1:])])

        Reg_val[int(argument[1][1:])]=re2 & re3

        return opcodes[argument[0]]+"00"+Reg_dict[argument[1]]+Reg_dict[argument[2]]+Reg_dict[argument[3]]

def func_typ_B(argument):
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

        return opcodes[argument[0]]+Reg_dict[argument[1]]+str((bin(imm))[2:]) 
    
    
    elif argument[0]=="rs":
        r1=int(Reg_val[int(argument[1][1:])])    
        imm=int(argument[2][1:])
        Reg_val[int(argument[1][1:])]=r1>>imm

        return opcodes[argument[0]]+Reg_dict[argument[1]]+str((bin(imm))[2:])



def func_typ_C(argument):
    if argument[0]=="mov": #mov register
        re1=int(Reg_val[int(argument[1][1:])])
        Reg_val[int(argument[2][1:])]=str(re1)
        
        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]

    elif argument[0]=="div":
        
        re3=int(Reg_val[int(argument[1][1:])])
        re4=int(Reg_val[int(argument[2][1:])])
        Reg_val[0]=str(re3//re4)
        Reg_val[1]=str(re3%re4)

        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]


    elif argument[0]=="not":
        re1=int(Reg_val[int(argument[1][1:])])
        re2=~(bin(re1)[2:])
        re2=int(str(re2),2)
        Reg_val[int(argument[2][1:])]=str(re2)

        print(re2)

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

    if argument[0] =="ld":
        Reg_val[int(reg[1:])]=var_val[var]

    elif argument[0]=="st":
        var_val[var] =Reg_val[int(reg[1:])]

    return op+rval+mem

def func_typ_E(argument):
    pass

def func_typ_F(argument):
    if argument[0]=="hlt":
        return opcodes["hlt"]+"00000000000"
    
        
main()
