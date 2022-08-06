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

def main():
    
    global code

    code=[]
    for line in stdin:
        if line=='':
            break
        code.append(line.rstrip())
        
    memory_dict={}    

    for i in range(256):
        try:
            memory_dict[bin(i)[2:].zfill(8)]=code[i]
        except IndexError:
            memory_dict[bin(i)[2:].zfill(8)]='0000000000000000'

    PC=0

    is_hlt=False
    
    while (not is_hlt):

        PC_in_binary=bin(PC)[2:].zfill(8)
        current_instruction=memory_dict[PC_in_binary]

        if current_instruction[:5] in ['10000','10001','10110','11010','11011','11100']:
            code_output.append(func_typ_A(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10010','11000','11001']:
            code_output.append(func_typ_B(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10011','10111','11101','11110']:
            code_output.append(func_typ_C(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['10100','10101']:
            code_output.append(func_typ_D(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['11111','01100','01101','01111']:
            code_output.append(func_typ_E(current_instruction,PC_in_binary))

        elif current_instruction[:5] in ['01010']:
            code_output.append(func_typ_F(current_instruction,PC_in_binary))
        else:
            code_output.append('error')

        PC+=1
        
        
main()
