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

Reg_bin_val=["00000000","00000000","00000000","00000000","00000000","00000000","00000000","00000000"]

def flag_setter(v=0,l=0,g=0,e=0):
    Flags[0]=str(v)
    Flags[1]=str(l)
    Flags[2]=str(g)
    Flags[3]=str(e)
    #setting value of flag register
    Reg_bin_val[7]="000000000000"+Flags[0]+Flags[1]+Flags[2]+Flags[3]

def func_typ_A(argument,prog_counter):
    ir1=int(argument[7:10],2)
    ir2=int(argument[10:13],2)
    ir3=int(argument[13:16],2)

    re1=int(Reg_bin_val[ir1])
    re2=int(Reg_bin_val[ir2])
 
    op=argument[:5]

    if op=='10000':     #add
        if re1+re2>65535:
            flag_setter(1)
            Reg_bin_val[ir3]=(str(bin((re1+re2)%(2**16))[2:]))
        else:
            Reg_bin_val[ir3]=(str(bin(re1+re2))[2:])
            flag_setter()


    elif op=="10001":   #sub
        if re1 - re2 < 0:
            flag_setter(1)
            Reg_bin_val[ir3]='0'
        else:
            flag_setter()
            Reg_bin_val[ir3]=str((bin(re1-re2)[2:]))


    elif op=='10110':   #mul
        if re1*re2>65535:
            Reg_bin_val[ir3]=(str(bin((re1*re2)%(2**16))[2:]))
            flag_setter(1)
        else:
            Reg_bin_val[ir3]=(str(bin(re1*re2))[2:])


    elif op=='11010':   #xor
        for i,j in zip(re1,re2):
            if i=='1' and j=='1':
                Reg_bin_val[ir3]+='0'
            elif i=='1' and j=='0':
                Reg_bin_val[ir3]+='1'
            elif i=='0' and j=='1':
                Reg_bin_val[ir3]+='1'
            elif i=='0' and j=='0':
                Reg_bin_val[ir3]+='0'
    
    
    elif op=='11011':   #or
        for i,j in zip(re1,re2):
            if i=='1' and j=='1':
                Reg_bin_val[ir3]+='1'
            elif i=='1' and j=='0':
                Reg_bin_val[ir3]+='1'
            elif i=='0' and j=='1':
                Reg_bin_val[ir3]+='1'
            elif i=='0' and j=='0':
                Reg_bin_val[ir3]+='0'
    
    
    elif op=='11100':   #and
        for i,j in zip(re1,re2):
            if i=='1' and j=='1':
                Reg_bin_val[ir3]+='1'
            elif i=='1' and j=='0':
                Reg_bin_val[ir3]+='0'
            elif i=='0' and j=='1':
                Reg_bin_val[ir3]+='0'
            elif i=='0' and j=='0':
                Reg_bin_val[ir3]+='0'
    
    return str((prog_counter.zfill(8))+" "+Reg_bin_val[0].zfill(8)+" "+Reg_bin_val[1].zfill(8)+" "+Reg_bin_val[2].zfill(8)+" "+Reg_bin_val[3].zfill(8)+" "+Reg_bin_val[4].zfill(8)+" "+Reg_bin_val[5].zfill(8)+" "+Reg_bin_val[6].zfill(8)+" "+Reg_bin_val[7].zfill(8))

def func_type_B(argument,prog_counter):
    ir1=int(argument[5:8],2)
    # re1=int(Reg_val[ir1])
    imm=int(argument[8:16])
    immi=int(argument[8:16],2)
    flag_setter()
    op=argument[:5]

    if op=='10010':#mov imm
        Reg_bin_val[ir1]=bin(imm)[2:]

    elif op=='11000':#bitwise rs
        Reg_bin_val[ir1]=Reg_bin_val[ir1]>>immi
    elif op=='11001':#bitwise ls
        Reg_bin_val[ir1]=Reg_bin_val[ir1]<<immi
    
    return str((prog_counter.zfill(8))+" "+Reg_bin_val[0].zfill(8)+" "+Reg_bin_val[1].zfill(8)+" "+Reg_bin_val[2].zfill(8)+" "+Reg_bin_val[3].zfill(8)+" "+Reg_bin_val[4].zfill(8)+" "+Reg_bin_val[5].zfill(8)+" "+Reg_bin_val[6].zfill(8)+" "+Reg_bin_val[7].zfill(8))

def func_type_C(argument ,prog_counter):
    ir1=int(argument[10:13],2)
    ir2=int(argument[13:16],2)

    op=argument[:5]
    if op=='10111': #mov reg
        if ir2==7:
            Reg_bin_val[ir1]=Reg_bin_val[7]
        else:
            Reg_bin_val[ir2]=Reg_bin_val[ir1]
        flag_setter()
        
    elif op=='10011':#div
        rval1=int(Reg_bin_val[ir1],2)
        rval2=int(Reg_bin_val[ir2],2)

        r0=rval1//rval2
        r1=rval1%rval2

        Reg_bin_val[0]=bin(r0)[2:]
        Reg_bin_val[1]=bin(r1)[2:]
        flag_setter()

    
    elif op=='11101':#not
        re1=(Reg_bin_val[ir1])
        for i in re1:
            if i=='1':
                Reg_bin_val[ir2]+='0'
            elif i=='0':
                Reg_bin_val[ir2]+='1'
    
    elif op=='11101':#cmp
        re1=Reg_val[ir1]
        re2=Reg_val[ir2]

        if re1==re2:
            Flags[3]='1'
        elif re1>re2:
            Flags[2]='1'
        elif re1<re2:
            Flags[1]='1'
    
    return str((prog_counter.zfill(8))+" "+Reg_bin_val[0].zfill(8)+" "+Reg_bin_val[1].zfill(8)+" "+Reg_bin_val[2].zfill(8)+" "+Reg_bin_val[3].zfill(8)+" "+Reg_bin_val[4].zfill(8)+" "+Reg_bin_val[5].zfill(8)+" "+Reg_bin_val[6].zfill(8)+" "+Reg_bin_val[7].zfill(8))

def func_type_D(argument,prog_counter):
    op=argument[:5]
    re1=int(argument[5:8],2)
    mem_add=argument[8:16]

    if op=='10100':
        Reg_bin_val[re1]=memory[mem_add]
    elif op=='10101':
        memory[mem_add]=Reg_bin_val[re1]

    flag_setter()
    return str((prog_counter.zfill(8))+" "+Reg_bin_val[0].zfill(8)+" "+Reg_bin_val[1].zfill(8)+" "+Reg_bin_val[2].zfill(8)+" "+Reg_bin_val[3].zfill(8)+" "+Reg_bin_val[4].zfill(8)+" "+Reg_bin_val[5].zfill(8)+" "+Reg_bin_val[6].zfill(8)+" "+Reg_bin_val[7].zfill(8))

def func_type_E(argument,prog_counter):
    op=argument[:5]
    add=int(argument[8:16],2)

    if op=='01100':#jlt
        if Flags[1]!='1':
            add='0'
    
    elif op=='01101':#jgt
        if Flags[2]!='1':
            add='0'

    elif op=='01111':#je
        if Flags[3]!='1':
            add='0'
    
    flag_setter()

    ret_str=str((prog_counter.zfill(8))+" "+Reg_bin_val[0].zfill(8)+" "+Reg_bin_val[1].zfill(8)+" "+Reg_bin_val[2].zfill(8)+" "+Reg_bin_val[3].zfill(8)+" "+Reg_bin_val[4].zfill(8)+" "+Reg_bin_val[5].zfill(8)+" "+Reg_bin_val[6].zfill(8)+" "+Reg_bin_val[7].zfill(8))

    ret_lst=[add,ret_str]

    return ret_lst

def main():
    
    global code

    code=[]
    for line in stdin:
        if line=='':
            break
        code.append(line.rstrip())

    global memory
    memory={}    

    for i in range(256):
        try:
            memory[bin(i)[2:].zfill(8)]=code[i]
        except IndexError:
            memory[bin(i)[2:].zfill(8)]='0000000000000000'

    PC=0

    is_hlt=False

    global code_output
    code_output=[]
    
    while (not is_hlt):

        PC_in_binary=bin(PC)[2:].zfill(8)
        current_instruction=memory[PC_in_binary]

        if current_instruction[:5] in ['10000','10001','10110','11010','11011','11100']:
            code_output.append(func_typ_A(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10010','11000','11001']:
            code_output.append(func_type_B(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10011','10111','11101','11110']:
            code_output.append(func_type_C(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10100','10101']:
            code_output.append(func_type_D(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['11111','01100','01101','01111']:
            code_output.append(func_type_E(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['01010']:
            code_output.append(func_type_F(current_instruction,PC_in_binary))
        else:
            code_output.append('error')

        PC+=1
        
        
main()
