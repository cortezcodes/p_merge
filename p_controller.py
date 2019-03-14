from tkinter import Tk, filedialog, END
from p_view import PdfView
from p_model import Pdf
from PyPDF2 import PdfFileReader, PdfFileMerger
from contextlib import ExitStack
import re

class PdfController():
    #Initializes the GUI
    def __init__(self):
        self.root = Tk()
        self.view = PdfView(self.root)
        self.pdfs = []
        self.view.add_btn['command'] = self.add_file
        self.view.delete_btn['command'] = self.delete
        self.view.path_list_view.bind("<<ListboxSelect>>", self.get_info)
        self.view.merge_btn['command'] = self.merge
        self.view.up_btn['command'] = self.moveup
        self.view.down_btn['command'] = self.movedown
        
    # Starts the Gui for the entire program
    def run(self):
        self.root.title("PMerge - PDF file Merger")
        self.root.geometry('700x700')
        self.root.mainloop()

    #opens the Filename open dialog box and sets the import_view to the selected file
    #TODO: Don't forget to change the initialdir to C:/ for production
    def add_file(self):
        file_count = 1
        filepath = filedialog.askopenfilenames(title="Select PDF",
                                               initialdir="C:\\Users\\corte\\OneDrive\\Desktop\\programming\\personal_projects\\desktop\\p_merge\\test_PDFs",
                                               filetypes=[('pdf files', '.pdf')])
        for file in filepath:
            pdf_obj = Pdf()
            with open(file, 'rb') as file_binary:
                pdf = PdfFileReader(file_binary)
                pdf_obj.info = pdf.getDocumentInfo()
                pdf_obj.page_num = pdf.getNumPages()
                pdf_obj.filepath = file
            self.view.path_list_view.insert(END, file)
            #self.build_filetree(filename=pdf_obj.filepath, num_of_pages=pdf_obj.page_num)
            self.pdfs.append(pdf_obj)
            file_binary.close()

    #build the filetree of files to be manipulated
    #TODO: Add Filetree version to do manipulations like split and merge page by page
    def build_filetree(self, filename='', num_of_pages=1):
        file_count = len(self.view.filetree.get_children())
        folder = self.view.filetree.insert("", file_count,
                                           "", text=filename)
        


    #deletes the selected files in path_list_view
    #TODO Delete multiple files at once
    def delete(self):
        files = self.view.path_list_view.curselection()
        for file in files:
            filepath = self.view.path_list_view.get(file)
            pdf = self.pdfs[file] # using the indices to grab the filepath from the listbox
            self.pdfs.remove(pdf) # removing the filepath from the pdfs list
            self.view.path_list_view.delete(file) # delete filepath from listbox
        self.clear_feedback()

    # Merge Files
    #TODO
    def merge(self):
        with ExitStack() as stack:
            new_filepath = filedialog.asksaveasfilename(title="Select PDF",
                                               initialdir="C:\\Users\\corte\\OneDrive\\Desktop\\programming\\personal_projects\\desktop\\p_merge\\test_PDFs",
                                               filetypes=[('pdf files', '.pdf'),('all files', '*.*')])
            if not re.search(".pdf$",new_filepath):
                new_filepath = new_filepath + ".pdf"
        
            pdfMerger = PdfFileMerger()
            files = [stack.enter_context(open(pdf.filepath, 'rb')) for pdf in self.pdfs]
            #open a read binary of all the filepaths currently loaded into PMerger and merge them into the pdfMerger object
            for pdf in files:
                pdfMerger.append(pdf)
            
            #open the new filepath to as a write binary file and write all of the files that were previously loaded into pdfMerger
            with open(new_filepath, 'wb') as final_filepath:
                pdfMerger.write(final_filepath)
        self.clear_feedback()
        self.append_feedback("Files have been merged")
        
    #adds text to the feedback view
    def append_feedback(self, text):
        output_text = self.view.feedback_text.get() + text
        self.view.feedback_text.set(output_text)

    # Clears the Feedback view of all text
    def clear_feedback(self):
        self.view.feedback_text.set("")

    # Displays PDF obj Items in the Object list in the feedback view
    def get_info(self, event):
        for index in self.view.path_list_view.curselection():
            pdf = self.pdfs[index]
            self.clear_feedback()
            self.append_feedback(pdf.filepath)
            self.append_feedback("\nNumber of Pages: {}".format(pdf.page_num))
            self.append_feedback("\nTitle: {}".format(pdf.info.title))
            self.append_feedback("\nAuthor: {}".format(pdf.info.author))
            self.append_feedback("\nCreator: {}".format(pdf.info.creator))
            self.append_feedback("\nProducer: {}".format(pdf.info.producer))
            self.append_feedback("\nSubject: {}".format(pdf.info.subject))

    #move file one up the list on the file order
    def moveup(self):
        if  self.view.path_list_view.curselection():
            file_index = self.view.path_list_view.curselection()[0]
        else:
            self.clear_feedback()
            self.append_feedback("\nNo file has been selected")
            return
        if file_index == 0:
            self.clear_feedback()
            self.append_feedback("\nFile already at the top of the list")
        else:
            self.pdfs.insert(file_index-1, self.pdfs.pop(file_index))
            file = self.view.path_list_view.get(file_index)
            self.view.path_list_view.delete(file_index)
            self.view.path_list_view.insert(file_index-1, file)
            self.view.path_list_view.select_set(file_index-1)

    #move file one down the list on the file order
    def movedown(self):
        if self.view.path_list_view.curselection():
            file_index = self.view.path_list_view.curselection()[0]
            list_len = self.view.path_list_view.size()
        else:
            self.clear_feedback()
            self.append_feedback("\nNo file has been selected")
            return
        if file_index == list_len - 1:
            self.clear_feedback()
            self.append_feedback("\nFile already at the bottom of the merge file stack")
        else:
            self.pdfs.insert(file_index+1, self.pdfs.pop(file_index))
            file = self.view.path_list_view.get(file_index)
            self.view.path_list_view.delete(file_index)
            self.view.path_list_view.insert(file_index+1, file)
            self.view.path_list_view.select_set(file_index+1)
        

if __name__ == "__main__":
    print("Please run the p_merge.py file as the main program")