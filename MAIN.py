from tkinter import *

import memories as memory
import program as assembler
import processor as cpu

def load(micro_code, main_code):
    micro, main = assembler.assembler(micro_code, main_code + strdefault)
    mem = memory.AllMemory()
    for i in micro:
        bin, address = i.split('-')
        mem.control_memory.write(int(address), '0b'+bin, 'b')
    
    for j in main:
        bin, address = j.split('-')
        mem.main_memory.write(int(address), '0b'+bin, 'b')
    
    mem.CAR.write(64, 'd')
    mem.PC.write(0, 'd')
    global computer
    computer=cpu.CPU(mem)
    clockBtn["state"]=NORMAL
    CAR_Label["text"]=computer.memory.CAR.read_binary()[2:]
    SBR_Label["text"]=computer.memory.SBR.read_binary()[2:]
    AR_Label["text"]=computer.memory.AR.read_binary()[2:]
    AC_Label["text"]=computer.memory.AC.read_binary()[2:]
    DR_Label["text"]=computer.memory.DR.read_binary()[2:]
    PC_Label["text"]=computer.memory.PC.read_binary()[2:]
    canvas = Canvas(memFrame)
    scrollbar = Scrollbar(memFrame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    content_frame = Frame(canvas)
    for i in range(2048):
        label = Label(content_frame, text="{})".format(i),width=5,highlightbackground="black", background="white",highlightthickness=2)
        label.grid(row=i, column=0)
        label2 = Label(content_frame, text=(computer.memory.main_memory.read(i,'b'))[2:]
                       ,width=20,highlightbackground="black",highlightthickness=2,justify='center')
        label2.grid(row=i, column=1)
    scrollbar.grid(row=0, column=2, sticky="ns")
    canvas.grid(row=0, column=0)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    canvas2 = Canvas(micFrame)
    scrollbar2 = Scrollbar(micFrame, orient="vertical", command=canvas2.yview)
    canvas2.configure(yscrollcommand=scrollbar2.set)
    content_frame2 = Frame(canvas2)
    for i in range(128):
        label = Label(content_frame2, text="{})".format(i),width=5,highlightbackground="black", background="white",highlightthickness=2)
        label.grid(row=i, column=0)
        label2 = Label(content_frame2, text=(computer.memory.control_memory.read(i,'b'))[2:]
                       ,width=20,highlightbackground="black",highlightthickness=2,justify='center')
        label2.grid(row=i, column=1)
    scrollbar2.grid(row=0, column=2, sticky="ns")
    canvas2.grid(row=0, column=0)
    canvas2.create_window((0, 0), window=content_frame2, anchor="nw")
    def on_canvas_configure(event):
        canvas2.configure(scrollregion=canvas2.bbox("all"))

    canvas2.bind("<Configure>", on_canvas_configure)
    return cpu.CPU(mem)

strdefault = '''
ORG 1000
    1: DEC.1
    2: DEC.2
    3: DEC.6
    4: DEC.24
    5: DEC.120
    6: DEC.720
    7: DEC.5040
    8: DEC.43200'''

micro_code = """    ORG 0
    ADD: NOP I CALL INDRCT
        READ U JMP NEXT
        ADD U JMP FETCH
    ORG 4
    BRANCH: NOP S JMP OVER
            NOP U JMP FETCH
    OVER:   NOP I CALL INDRCT
            ARTPC U JMP FETCH
    ORG 8
    STORE: NOP I CALL INDRCT
           ACTDR U JMP NEXT 
           WRITE U JMP FETCH
    ORG 12
    EXCHANGE:   NOP              I CALL INDRCT
                READ             U JMP NEXT
                ACTDR, DRTAC     U JMP NEXT
                WRITE            U JMP FETCH
    ORG 16
    HALT: HAL U JMP
    ORG 20
    FACT:   READ U JMP NEXT
            DRTAC U JMP FETCH
    ORG 64 
    FETCH: PCTAR U JMP NEXT
           READ, INCPC U JMP NEXT
           DRTAR U JMP MAP
    INDRCT: READ U JMP NEXT
            DRTAR U RET"""

def update():
    clockBtn["state"]=NORMAL
    CAR_Label["text"]=computer.memory.CAR.read_binary()[2:]
    SBR_Label["text"]=computer.memory.SBR.read_binary()[2:]
    AR_Label["text"]=computer.memory.AR.read_binary()[2:]
    AC_Label["text"]=computer.memory.AC.read_binary()[2:]
    DR_Label["text"]=computer.memory.DR.read_binary()[2:]
    PC_Label["text"]=computer.memory.PC.read_binary()[2:]

if __name__ == "__main__":
    
    

    """    ORG 0
        ADD A 
        ADD B I
        STORE DEC.100
        STORE HEX.FF
        STORE BIN.1111
        ADD C
        FACT 5
        EXCHANGE HEX.FF
        HALT DEC.0
    ORG 500
    A: DEC.50
    B: DEC.502
    C: DEC.35
    """

    root=Tk()
    global clockBtn,CAREntry
    mainCodeLabel = Label(root,text='Main Code:',font=("Arial bold",12))
    mainCodeLabel.grid(row=0,column=0,padx=30,pady=(30,0))

    mainCodeText = Text(root,width=30,height=25,border=10)
    mainCodeText.grid(row=1,column=0,padx=30,pady=(10,30))

    mainCodeLabel = Label(root,text='Mini Code:',font=("Arial bold",12))
    mainCodeLabel.grid(row=0,column=1,padx=30,pady=(30,0))

    miniCodeText = Text(root,width=50,height=25,border=10)
    miniCodeText.insert('1.0',micro_code)
    miniCodeText["state"]=DISABLED
    miniCodeText.grid(row=1,column=1,padx=30,pady=(10,30))

    submitBtn = Button(root, text="Submit",width=10,border=3,command=lambda: load(micro_code, mainCodeText.get("1.0",'end-1c')))        
    submitBtn.grid(row=2,column=0,padx=30,pady=(30,10))
    #computer.print_reg()
    clockBtn = Button(root, text="Clock",width=10,border=3,command=lambda:(computer.clock(),update()))
    clockBtn["state"]=DISABLED         
    clockBtn.grid(row=2,column=1,padx=30,pady=(30,10))

    memFrame=LabelFrame(root,width=20,height=100,border=5,text='Memory')
    memFrame.grid(row=0,column=2,rowspan=3,padx=0,pady=0)
    
    micFrame=LabelFrame(root,width=20,height=100,border=5,text='Control Memory')
    micFrame.grid(row=0,column=3,rowspan=3,padx=0,pady=0)

    regFrame=LabelFrame(root)
    regFrame.grid(row=3,column=0,columnspan=2,padx=0,pady=0)

    CARLabel = Label(regFrame,text="CAR:",font=("Arial bold",10))
    CAR_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    CARLabel.grid(row=3,column=0,padx=0,pady=0)
    CAR_Label.grid(row=4,column=0,padx=5,pady=(0,20))

    ARLabel = Label(regFrame,text="AR:",font=("Arial bold",10))
    AR_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    ARLabel.grid(row=3,column=1,padx=0,pady=0)
    AR_Label.grid(row=4,column=1,padx=5,pady=(0,20))

    DRLabel = Label(regFrame,text="DR:",font=("Arial bold",10))
    DR_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    DRLabel.grid(row=3,column=2,padx=0,pady=0)
    DR_Label.grid(row=4,column=2,padx=5,pady=(0,20))

    ACLabel = Label(regFrame,text="AC:",font=("Arial bold",10))
    AC_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    ACLabel.grid(row=3,column=3,padx=0,pady=0)
    AC_Label.grid(row=4,column=3,padx=5,pady=(0,20))

    PCLabel = Label(regFrame,text="PC:",font=("Arial bold",10))
    PC_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    PCLabel.grid(row=3,column=4,padx=0,pady=0)
    PC_Label.grid(row=4,column=4,padx=5,pady=(0,20))

    SBRLabel = Label(regFrame,text="SBR:",font=("Arial bold",10))
    SBR_Label = Label(regFrame,justify='center',text='N/A',width=18,
        highlightbackground="black", background="white",highlightthickness=2)  
    SBRLabel.grid(row=3,column=5,padx=0,pady=0)
    SBR_Label.grid(row=4,column=5,padx=5,pady=(0,20))




    root.mainloop()