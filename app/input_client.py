from tkinter import *

__author__ = 'brighamhausman'



class Inputclient():
    __fields = None
    __gui = None
    __gui_data = None

    #TODO: fields should be list or dict
    def __init__(self, fields=[]):
        self.__fields = fields


    @property
    def fields(self):
        return self.__fields

    # expects a flat list whose members
    # define keys for the data model
    @fields.setter
    def fields(self, field_list):
        self.__fields = field_list

    def get_terminal_input(self, src_obj=None):
        user_input = {}

        if src_obj is None:
            for field in self.__fields:
                #TODO: validate input
                user_val = input('enter {} value: '.format(field))
                user_input[field] = user_val

        else:
            for prop in src_obj:
                msg = 'update value for {}? (current value is:{})'.format(prop, src_obj[prop])
                user_val = input(msg)
                if len(user_val) > 0:
                    #TODO: validate input
                    user_input[prop] = user_val
                else:
                    user_input[prop] = src_obj[prop]

        return user_input

    # src data is a dictionary, used for the data_model
    def get_gui_input(self, src_data=None):
        self.__gui_data = None
        if src_data is None:
            src_data = {}
            #build a new data structure
            for key in self.fields:
                src_data[key] = None

        #build a window using src_data
        win = self.get_gui(src_data)
        win.mainloop()

        return self.__gui_data

    @property
    def entries(self):
        return self.__entries

    def update_entries(self):
        pass

    def send_gui_entries(self):
        # return dict based on self.fields fgor keuys
        return_data = {}
        # and self.entries for values
        for key in self.fields:
            value = self.entries[key].get()
            return_data[key] = value
        self.__gui.quit()
        self.__gui_data = return_data


    def quit_gui(self):
        self.__gui.quit()



    #returns a UI widget for fetching data from the user
    # at some point this should get upgraded to take a button config object
    def get_gui(self, data_pack=None):
        self.__gui = Tk()
        self.__gui.title('Update vales')
        form = Frame(self.__gui)
        form.pack()
        self.__entries = {}
        for (ix, label) in enumerate(('key',) + tuple(self.fields)):
            lab = Label(form, text=label)
            ent = Entry(form)
            if label in self.fields:
                # set the value of the field to a default val
                default_text = self.fields[label]
                ent.delete(0, END)
                ent.insert(0, default_text)
            lab.grid(row=ix, column=0)
            ent.grid(row=ix, column=1)
            self.__entries[lab.cget('text')] = ent


        # ok button
        Button(self.__gui, text="Ok", command=self.send_gui_entries).pack(side=LEFT)
        # cancel button
        Button(self.__gui, text="Cancel", command=self.quit_gui).pack(side=RIGHT)

        return self.__gui





if __name__ == '__main__':
    # test gui
    ic = Inputclient(['Yo', 'Lo', 'Fo', 'Co'])
    inpt = ic.get_gui_input()

    print('input from gui client:', str(inpt))