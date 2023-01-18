from tkinter import * # used to render drop down menu to select logs


def buildExtendedRegex(data):
    return '|'.join(data)


def createCSV(path, data, dialect='excel'):
    with open(path, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(data)


def grabSelected():
    '''Returns selected logs from the Tkinter GUI dropdown (listbox).
    '''
    return [listbox.get(i) for i in listbox.curselection()]


def renderDropdown(options):
    window = Tk()
    window.geometry("750x350")
    window.title("Log File Selection")
    yscrollbar = Scrollbar(window)
    yscrollbar.pack(side=RIGHT, fill=Y)
    label = Label(window,
                  text = "Select log files to parse:",
                  font = ("Arial", 12), 
                  padx = 10, pady = 10)
    label.pack()
    listbox = Listbox(window, selectmode = "multiple", 
                   yscrollcommand = yscrollbar.set)

    # Widget expands horizontally and 
    # vertically by assigning both to
    # fill option
    listbox.pack(padx = 10, pady = 10,
              expand = YES, fill = "both")
    for i in range(len(options)):
        listbox.insert(END, _options[i])
        listbox.itemconfig(i, bg="white")

    yscrollbar.config(command=listbox.yview)
    selectButton = Button(window, text="Export log files", command=grabSelected)
    window.mainloop()
