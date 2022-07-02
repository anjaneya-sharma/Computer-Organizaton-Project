import sys
from sys import stdin

opcodes={"add":"10000","sub":"10001","mov":"10010","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"110001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"111110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}

Reg_dict={"r0":"000","r1":"001","r2":"010","r3":"011","r4":"100","r5":"101","r6":"110","flags":"111"}

Reg_typ_A=["add","sub","mul","xor","or","and"]
Reg_typ_B=["mov","rs","ls"]
Reg_typ_C=["mov","div","not","cmp"]
Reg_typ_D=["ld","st"]
Reg_typ_E=["jmp","jlt","jgt","je"]

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


def is_valid_register(register):

    list_of_registers=list(Reg_dict.keys())
    
    if register=='flags':
        print("Error at line {} : illegal use of flag registers".format(current_line))
        return False

    if register not in list_of_registers:
        print("Error at line {} : invalid register name".format(current_line))
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

def is_valid_memory(memory):

    if len(memory)!=8:
        print("Error at line {} : General Syntax Error".format(current_line))
        return False
    
    for i in memory:
        if i!='0' and i!='1':
            print("Error at line {} : General Syntax Error".format(current_line))
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

    if not is_valid_register(instruction[1]) or not is_valid_memory(instruction[2]):
        return False


def check_typeE(instruction):
    return 0

def check_mov(instruction):

    list_of_registers=list(Reg_dict.keys())

    if len(instruction)!=3:
        print('Error at {} : General Syntax Error'.format(current_line))
        return False
    
    if instruction[1] not in list_of_registers[:7]:
        if instruction[1]=='flags':
            print('Error at {} : illegal use of flag registers'.format(current_line))
            return False
        print('Error at {} : invalid register name'.format(current_line))
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
    
    count_var=0
    flag_reading_var=False

    global current_line
    current_line=0

    for line in code:

        current_line+=1

        if line[0]=='mov':

            if check_mov(line)==False:
                return True
            continue

        if line[0] in Reg_typ_A:

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
        
        # elif line[0]=='var':
        #     if check_var(line)
        
    return False
        


main()
    
