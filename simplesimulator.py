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
    
    while (PC<256 and not is_hlt):

        current_instruction=bin(PC)[2:].zfill(8)

        
        
main()
