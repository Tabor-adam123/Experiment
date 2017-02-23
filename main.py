import sqlite3 as sql
import tkinter as tk

def grid_two_labels(first, second, row, column, first_width, second_width):
    first.grid(row=row, column=column, columnspan=first_width, sticky=tk.W+tk.E)
    second.grid(row=row, column=column+first_width, columnspan=second_width, sticky=tk.W+tk.E)

def grid_all_labels(list, minrow, column, first_width, second_width):
    for i in range(len(list)//2):
        grid_two_labels(list[i*2], list[i*2+1], 2+i, column, first_width, second_width)

def execute(cur, query, *args):
    cur.execute(query, tuple(args))
    return cur

con=sql.connect(':memory:')
cur=con.cursor()

cur.execute('CREATE TABLE List (Id integer primary key autoincrement, Name, Number)')

window=tk.Tk()

add_user_name_label=tk.Label(window, text='Jméno')
add_user_number_label=tk.Label(window, text='Tel. číslo')
add_user_name_label.grid(row=0, column=0)
add_user_number_label.grid(row=0, column=2)

add_user_name_var=tk.StringVar()
add_user_number_var=tk.StringVar()

add_user_name_entry=tk.Entry(window, textvariable=add_user_name_var)
add_user_number_entry=tk.Entry(window, textvariable=add_user_number_var)
add_user_name_entry.grid(row=0, column=1)
add_user_number_entry.grid(row=0, column=3)

find_user_label=tk.Label(window, text='Jméno')
find_user_label.grid(row=1, column=0)

find_user_var=tk.StringVar()
find_user_entry=tk.Entry(window, textvariable=find_user_var)
find_user_entry.grid(row=1, column=1)

labels=[]

def edit_field(var, column, id):
    execute(cur, 'UPDATE List SET '+column+' = (?) WHERE Id = (?)', var.get(), id)

def new_table(all):
    global labels
    for label in labels:
        label.grid_forget()
    labels=[]
    for row in all:
        sv=tk.StringVar()
        sv.set(row[1])
        sv.trace('w', lambda x,y,z:edit_field(sv, 'Name', row[0]))
        labels.append(tk.Entry(window, textvariable=sv, relief=tk.SUNKEN))
        
        sv2=tk.StringVar()
        sv2.set(row[2])
        sv2.trace('w', lambda x,y,z:edit_field(sv2, 'Number', row[0]))
        labels.append(tk.Entry(window, textvariable=sv2, relief=tk.SUNKEN))
    grid_all_labels(labels, minrow=2, column=0, first_width=3, second_width=2)

def refresh():
    new_table(execute(cur, 'SELECT * FROM List ORDER BY Name').fetchall())

def add_user_command():
    if add_user_name_var.get() and add_user_number_var.get():
        execute(cur, 'INSERT INTO List (Name, Number) VALUES (?,?)', add_user_name_var.get(), add_user_number_var.get())
        add_user_name_var.set('')
        add_user_number_var.set('')
        refresh()

add_user_button=tk.Button(window, text='Přidat uživatele', command=add_user_command)
add_user_button.grid(row=0, column=4)

def find_user_command():
    if find_user_var.get():
        new_table(execute(cur, 'SELECT * FROM List WHERE Name=?', find_user_var.get()).fetchall())
        find_user_var.set('')

find_user_button=tk.Button(window, text='Vyhledat uživatele', command=find_user_command)
find_user_button.grid(row=1, column=2)

refresh_button=tk.Button(window, text='Zpět na seznam', command=refresh)
refresh_button.grid(row=1, column=3, columnspan=2, sticky=tk.W+tk.E)

window.mainloop()
