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

def func_typ_A(argument,prog_counter):
    ir1=int(argument[7:10],2)
    ir2=int(argument[10:13],2)
    ir3=int(argument[13:16],2)

    re1=int(Reg_val[ir1])
    re2=int(Reg_val[ir2])
 
    op=argument[:5]

    if op=='10000':     #add
        if re1+re2>65535:
            flag_setter(1)
            Reg_val[ir3]=str((re1+re2)%(2**16))
        else:
            flag_setter()
            Reg_val[ir3]=str(re1+re2)

    elif op=="10001":   #sub
        if re1 - re2 < 0:
            flag_setter(1)
            Reg_val[ir3]='0'
        else:
            flag_setter()
            Reg_val[ir3]=str(re1-re2)

    elif op=='10110':   #mul
        if re1*re2>65535:
            Reg_val[ir3]=str((re1*re2)%(2**16))
    elif op=='11010':   #xor
        pass
    elif op=='11011':   #or
        pass
    elif op=='11100':   #and
        pass
    
def func_type_B(argument,prog_counter):
    ir1=int(argument[5:8],2)
    # re1=int(Reg_val[ir1])
    imm=int(argument[8:16],2)

    flag_setter()
    op=argument[:5]

    if op=='10010':
        Reg_val[ir1]=imm
    elif op=='11000':
        pass
    elif op=='11001':
        pass

def func_type_C(argument ,prog_counter):
    ir1=int(argument[10:13])
    ir2=int(argument[13:16])
    op=argument[:5]

    if op=='10111': #mov reg
        if 1:#cheeeeck flags condition
            pass
        else:
            Reg_val[ir2]=Reg_val[ir1]
        flag_setter()

    elif op=='10011':
        pass
    elif op=='11101':
        pass
    elif op=='11101':#cmp
        re1=Reg_val[ir1]
        re2=Reg_val[ir2]

        if re1==re2:
            Flags[3]='1'
        elif re1>re2:
            Flags[2]='1'
        elif re1<re2:
            Flags[1]='1'
        else:
            #error to be returned-->check
            pass
    else:
        #error to be returned-->check 
        pass


def func_type_D(argument,prog_counter):
    op=argument[:5]
    re1=argument[5:8]
    mem_add=argument[8:16]

    if op=='10100':
        pass
    elif op=='10101':
        pass

    flag_setter()

def func_type_E(argument,prog_counter):
    pass

