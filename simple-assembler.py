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

var_val={}

def flag_setter(v=0,l=0,g=0,e=0):
    Flags[0]=str(v)
    Flags[1]=str(l)
    Flags[2]=str(g)
    Flags[3]=str(e)
    #setting value of flag register
    Reg_val[7]="000000000000"+Flags[0]+Flags[1]+Flags[2]+Flags[3]

def func_typ_C(argument):
    if argument[0]=="mov": #mov register
        re1=int(Reg_val[int(argument[1][1:])-1])
        Reg_val[int(argument[2][1:])-1]=str(re1)
        
        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]

    elif argument[0]=="div":
        
        re3=int(Reg_val[int(argument[1][1:])-1])
        re4=int(Reg_val[int(argument[2][1:])-1])
        Reg_val[0]=str(re3//re4)
        Reg_val[1]=str(re3%re4)

        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]


    elif argument[0]=="not":
        re1=int(Reg_val[int(argument[1][1:])-1])
        re2=~(re1)
        Reg_val[int(argument[2][1:])-1]=str(re2)

        return opcodes[argument[0]]+"00000"+Reg_dict[argument[1]]+Reg_dict[argument[2]]
    
    
    elif argument[0]=="cmp":
        re1=int(Reg_val[int(argument[1][1:])-1])
        re2=int(Reg_val[int(argument[2][1:])-1])
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
        Reg_val[int(reg[1:])-1]=var_val[var]

    elif argument[0]=="st":
        var_val[var] =Reg_val[int(reg[1:])-1]

    return op+rval+mem

def func_typ_E():
    pass
