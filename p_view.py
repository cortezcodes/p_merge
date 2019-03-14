from tkinter import *
from tkinter.ttk import Treeview


class PdfView():

    def __init__(self, master):
        self.feedback_text = StringVar()
        self.feedback_text.set("Welcome to PMerge 1.0! \nCreator: Cortez McCrary \nCreated: March 1 2019.")

        #Frame to hold filetree
        self.filetree_frame = Frame(master=master)
        self.filetree_frame.pack(fill=BOTH)

        #File tree view
        #self.filetree = Treeview(master=self.filetree_frame)
        #self.filetree.heading("#0", text="File", anchor=W)
        #self.filetree.pack(side=TOP, fill=BOTH)

    
        #Frame to hold all buttons
        self.top_frame = Frame(master=master, bg='dark slate gray')
        self.top_frame.pack()

        #Up, add, delete, and Merge button
        self.up_btn = Button(master=self.top_frame, text="UP", bg='green', fg='white')
        self.up_btn.pack(side=LEFT)
        self.add_btn = Button(master=self.top_frame, text="Add")
        self.add_btn.pack(side=LEFT)
        self.delete_btn = Button(master=self.top_frame, text="Delete")
        self.delete_btn.pack(side=LEFT)
        self.merge_btn = Button(master=self.top_frame, text="Merge")
        self.merge_btn.pack(side=LEFT)
        self.down_btn = Button(master=self.top_frame, text="DOWN", bg='green', fg='white')
        self.down_btn.pack(side=LEFT)

        #Frame that contains the input_list
        self.center_frame = Frame(master=master, bg='dark slate gray')
        self.center_frame.pack(fill=BOTH)
        # input_list
        self.path_list_view = Listbox(master=self.center_frame, height=20)
        self.path_list_view.pack(fill=X, expand=1)
        #commanded view
        self.feedback_text_view = Label(master=self.center_frame, anchor=NW, textvariable=self.feedback_text,
                                        bg="dark slate gray", fg="white", bd=5, justify=LEFT, padx=5, height=340,
                                        wraplength=750) #height=340,
        self.feedback_text_view.pack(fill=BOTH, expand=1)

    

if __name__ == "__main__":
    print("Please run the p_merge.py file as the main program")