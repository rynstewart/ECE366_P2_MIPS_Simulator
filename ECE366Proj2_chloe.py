                       
#####instructions we still need######
"""
lui, ori, mfhi, mflo, slt
andi, bne
special instruction
slt - DONE
mfhi, mflo - needs mult rework
ori - DONE
bne - 
lui - 
   
"""


def saveJumpLabel(asm,labelIndex, labelName, labelAddr):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index\
            labelAddr.append(lineCount*4)
            #asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def regNameInit(regName):
    i = 0
    while i<=23:
        regName.append(str(i))
        i = i + 1
    regName.append('lo')
    regName.append('hi')
    
def rshift(val, n): 
    #x = 1
    return val>>n

    """
    if val >= 0:
        return val>>n
    else:
        #i = (format(val, '032b') + format(0x8000, '032b'))>>n
        while x <= n:
            i = (val)>>1 + 0x8000
            x+=1
        return i
    """

def main():
    
    MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25
    f = open("mc.txt","w+")
    h = open("mips1.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName, labelAddr) # Save all jump's destinations

    #import pdb; pdb.set_trace()

    #for lineCount in len(asm):
    lineCount = 0
    while(lineCount < len(asm)):

        line = asm[lineCount]
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        #line = line.replace("\t", "")

       
        
        #sep = '...'
        #rest = text.split(sep, 1)[0]
        #

        #comment_sep = '#'
        #line = line.split(comment_sep, 1)

        #useful debugging print statement
        print(line)

        print(line)
                        
        if(line[0:5] == "addiu"): # $t = $s + imm; advance_pc (4); addiu $t, $s, imm
            line = line.replace("addiu","")
            line = line.replace("\t", "")
            line = line.split(",")
            PC = PC + 4

            print(line)
            imm = str(line[2])
            #if the imm = hex...
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[2] = int(str(imm), 10)
                print(line)
                regval[int(line[0])] = regval[int(line[1])] + int(line[2])
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + str(line[2]) + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

            else:
                regval[int(line[0])] = regval[int(line[1])] + int(line[2],16)
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        if(line[0:4] == "addu"): # $t = $s + imm; advance_pc (4); addiu $t, $s, imm
            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
        
        elif(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            line = line.replace("addi","")
            line = line.split(",")
            PC = PC + 4

            imm = str(line[2])

            #if the imm = hex...
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[2] = int(str(imm), 10)
                regval[int(line[0])] = regval[int(line[1])] + int(line[2])
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + str(line[2]) + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

            #if imm = decimal
            else:
                line[2] = int(line[2], 10)
                regval[int(line[0])] = int(regval[int(line[1])]) + line[2]
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + str(line[2]) + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
            line = line.replace("xor","")
            line = line.split(",")
            PC = PC + 4
            #x = format(int(line[1]),'032b')^format(int(line[2]),'032b')
            x = format(int(line[1]),'032b')
            y = format(int(line[2]),'032b')
            z = int(x)^int(y)
            regval[int(line[0])] = z
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            
        elif(line[0:3] == "lui"): # $t = (imm << 16); advance_pc (4); lui $t, imm
            line = line.replace("lui","")
            line = line.split(",")
            PC = PC + 4

            imm = line[1]

            #if the imm = hex...
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[1] = int(str(imm), 10)
                regval[int(line[0])] = int(line[1])

                f.write('Operation: $' + line[0] + ' = ' + '(' + str(line[1]) + ' << 16); ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(line[1]) + '\n')

            else:
                regval[int(line[0])] = int(line[1],16)
                f.write('Operation: $' + line[0] + ' = ' + '(' + line[1] + ' << 16); ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + line[1] + '\n')            
                
            
        
        elif(line[0:5] == "multu"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("multu","")
            line = line.split(",")
            PC = PC + 4
            temp = regval[int(line[0])] * regval[int(line[1])]
            templo = format(temp, '064b')
            templo = temp & 0x00000000FFFFFFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + ', $HI = ' + str(regval[HI]) + '\n')
            
        #mult
        elif(line[0:4] == "mult"): # $LO = $s * $t; advance_pc (4); mult $s, $t
            line = line.replace("mult","")
            line = line.split(",")
            PC = PC + 4

            #convert the str to an int (error)
            regval[int(line[1])] = int(line[1])

            temp = regval[int(line[0])] * regval[int(line[1])]
            print(temp)
            templo = format(temp, '064b')
            templo = temp & 0x00000000FFFFFFFF
            temphi = temp >> 32
            regval[LO] = int(templo)
            regval[HI] = int(temphi)
            f.write('Operation: $LO' + ' = ' + '$' + line[0] + ' * $' + line[1] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$LO = ' + str(regval[LO]) + ', $HI = ' + str(regval[HI]) + '\n')
            
        elif(line[0:4] == "mfhi"): # Operation:$d = $HI; advance_pc (4);mfhi $d
            line = line.replace("mfhi","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[HI]
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$HI; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[HI]) + '\n')            
        
        elif(line[0:4] == "mflo"): # Operation:$d = $LO; advance_pc (4);mflo $d
            line = line.replace("mflo","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[LO]
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$LO; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[LO]) + '\n')            
        
                #srl
        elif(line[0:3] == "srl"): # $d = $t >> h; advance_pc (4); srl $d, $t, h
            line = line.replace("srl","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = rshift(-1, int(line[2]))
            #regval[int(line[0])] = rshift(regval[int(line[1])], int(line[2]))
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' >> ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')            
            
            
        elif(line[0:3] == "lbu"): # $t = MEM[$s + offset]; advance_pc (4); lb $t, offset($s)
            line = line.replace("lbu","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4

            imm = str(line[1])
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[1] = int(str(imm), 10)
                regval[int(line[0])] = format(int(MEM[regval[int(line[1])]+int(line[2])]),'08b')
                regval[int(line[0])] = abs((int(regval[int(line[0])])))
                f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + ' \n')
             
            else:
                regval[int(line[0])] = format(int(MEM[regval[int(line[1])]+int(line[2])]),'08b')
                regval[int(line[0])] = abs((int(regval[int(line[0])])))
                f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + ' \n')
             
        #sb
        elif(line[0:2] == "sb"): # MEM[$s + offset] = (0xff & $t); advance_pc (4); sb $t, offset($s)
            line = line.replace("sb","")
            line = line.replace("(",",")
            line = line.replace(")","")
            line = line.split(",")
            PC = PC + 4

            imm = str(line[1])
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[1] = int(str(imm), 10)
                MEM[ regval[int(line[2])] + int(line[1]) ] = format(int(line[0]),'08b')
                MEM[ regval[int(line[2]) + int(line[1])] ] = int(MEM[regval[int(line[2])]+int(line[1])])
                f.write('Operation: MEM[$' + line[2] + ' + ' + line[1] + '] = ' + '$' + line[0] + '; \n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str(int(line[2])+int(line[1])) + ' = ' + str(regval[int(line[0])]) + ' \n')

            else:
                MEM[ regval[int(line[2])] + int(line[1]) ] = format(int(line[0]),'08b')
                MEM[ regval[int(line[2]) + int(line[1])] ] = int(MEM[regval[int(line[2])]+int(line[1])])
                f.write('Operation: MEM[$' + line[2] + ' + ' + line[1] + '] = ' + '$' + line[0] + '; \n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str(int(line[2])+int(line[1])) + ' = ' + str(regval[int(line[0])]) + ' \n')
               
        #slt
        elif(line[0:3] == "slt"):
            line = line.replace("slt","")
            line = line.split(",")
           
            if(line[1] < line[2]):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n') 
        
        elif(line[0:4] == "andi"):
            line = line.replace("andi", "")
            line = line.split(",")
            PC = PC + 4

            imm = str(line[2])
            
            #if the imm = hex...
            if(imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[2] = int(str(imm), 10)

                print(line)
                print(regval)
                regval[int(line[1])] = int(line[2]) & regval[int(line[0])]
                temp_val = format( int(regval[int(line[1])]),'032b') 

                f.write('Operation: $' + line[1] + '= $' + line[0] + "&"  + str(line[2]))
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')
            
            #if imm != hex...
            else:
                regval[int(line[1])] = format(regval[int(line[2])] & regval[int(line[0])])
                temp_val = format( int(regval[int(line[1])]),'032b')

                f.write('Operation: $' + line[1] + '= $' + line[0] + "&"  + line[2])
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")
            PC = PC + 4

            #if imm  = hex
            imm = str(line[2])
            if( imm[0:2] == '0x'):
                imm = imm.replace('0x','')
                imm = int(imm, 16)
                line[2] = int(str(imm), 10)

                f.write('Operation: $' + line[1] + '= $' + line[0] + " | "  + str(line[2]) )
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')
            
            #if imm = decimal
            else:
                regval[int(line[1])] = format(regval[int(line[2])] | regval[int(line[0])])
                temp_val = format( int(regval[int(line[1])]),'032b')

                # __, 0, 1, 2
                #op, rs, rt, imm
                #6, 5, 5, 16
                #rt = rs | imm()
                f.write('Operation: $' + line[1] + '= $' + line[0] + "|"  + line[2])
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + str( int(line[2]) ) + '=' + str(regval[int(line[0])]) + '\n')
            
        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
        
        #hash
        elif(line[0:4]==hash):
            line = line.replace("beq","")
            line = line.split(",")
            B = 0xFA19E366#int(line[0])
            A = 0x01
            max = 0
            for A in range(0x65):
                hash(B, A, max)

        #beq
        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")
            if(regval[int(line[0])]==regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')

        #add
        elif(line[0:3] == "add"): # ADD $d = $s + $t; advance_pc (4); add $d, $s, $t
            line = line.replace("add","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')


        elif(line[0:1] == "j"): # JUMP
            #import pdb; pdb.set_trace()
            line = line.replace("j","")
            line = line.split(",")
            f.write('Operation: PC = nPC; ' + '\n')
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                 PC = line[0]
                 lineCount = line[0]
                 f.write('PC is now at ' + str(line[0]) + '\n')
            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        PC = labelAddr[i]
                        lineCount = labelIndex[i]
                        f.write('PC is now at ' + str(labelAddr[i]) + '\n')        
            f.write('No Registers have changed. \n')
            continue
        lineCount = lineCount + 1
    f.close()

if __name__ == "__main__":
    main()