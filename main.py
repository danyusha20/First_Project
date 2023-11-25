# импорт библиотек
import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# создание основного класса
class Main(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.init_main()
        self.db = DB()
        self.view_records()

    # функция для инициализации главного окна
    def init_main(self):
        self.title('Список сотрудников')
        self.geometry('900x500')
        self.resizable(False, False)

        # создание toolbar и его размещение
        toolbar = tk.Frame(bg='#242424', bd=2)
        toolbar.pack(side=tk.LEFT, fill=tk.Y)

        # создание стилей для дерева
        self.style = ttk.Style()
        self.style.configure('mystyle.Treeview',
                             font=('Arial', 13, 'bold'),
                             rowheight=50)
        self.style.configure('mystyle.Treeview.Heading',
                             font=('Arial', 13, 'bold'))
        self.style.layout('mystyle.Treeview',
                          [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # создание дерева
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show='headings',
                                 style='mystyle.Treeview')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=200, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-Mail')

        # --------------создание кнопок----------------

        # кнопка для добавления
        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.btn_open_dialog = customtkinter.CTkButton(toolbar, text='',
                                                       image=self.add_img,
                                                       command=self.open_dialog,
                                                       fg_color='#4158D0',
                                                       hover_color='#A01A7D', width=5)
        self.btn_open_dialog.pack(padx=100, pady=10)

        # кнопка для внесения изменений
        self.update_img = tk.PhotoImage(file="./img/update.png")
        self.btn_edit_dialog = customtkinter.CTkButton(toolbar, text='',
                                                       image=self.update_img,
                                                       command=self.open_update_dialog,
                                                       fg_color='#4158D0',
                                                       hover_color='#A01A7D', width=5)
        self.btn_edit_dialog.pack(padx=20, pady=10)

        # кнопка для удаления
        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        self.btn_delete = customtkinter.CTkButton(toolbar, text='', image=self.delete_img,
                                                  command=self.delete_records,
                                                  fg_color='#4158D0',
                                                  hover_color='#A01A7D', width=5)
        self.btn_delete.pack(padx=0, pady=10)

        # кнопка для поиска
        self.search_img = tk.PhotoImage(file="./img/search.png")
        self.btn_search = customtkinter.CTkButton(toolbar, text='', image=self.search_img,
                                                  command=self.open_search_dialog,
                                                  fg_color='#4158D0',
                                                  hover_color='#A01A7D', width=5)
        self.btn_search.pack(padx=20, pady=10)

        # кнопка для обновления
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        self.btn_refresh = customtkinter.CTkButton(toolbar, text='',
                                                   image=self.refresh_img,
                                                   command=self.view_records,
                                                   fg_color='#4158D0',
                                                   hover_color='#A01A7D', width=5)
        self.btn_refresh.pack(padx=20, pady=10)

        # ---------------------------------------------

        # создание scrollbar
        scroll = customtkinter.CTkScrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # размещаем дерево
        self.tree.pack(side=tk.RIGHT)

    # создание функции для открытия окна добавления
    def open_dialog(self):
        Child()

    # создание функции для открытия окна редактирования
    def open_update_dialog(self):
        Update()

    # редактирование записей
    def update_records(self, name, phone, email):
        self.db.c.execute("""
        UPDATE db SET name=?, phone=?, email=? WHERE ID = ?
        """, (name, phone, email, self.tree.set(self.tree.selection()[0],
                                                "#1"),))
        self.db.conn.commit()
        self.view_records()

    # удаление записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("""
            DELETE FROM db WHERE id = ?
            """, (self.tree.set(selection_item, "#1"),))
            self.db.conn.commit()
            self.view_records()

    # открытие окна поиска
    def open_search_dialog(self):
        Search()

    # поиск записей
    def search_record(self, name):
        name = ("%" + name + "%",)
        self.db.c.execute("""
        SELECT * FROM db WHERE name LIKE ?
        """, name)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # добавление записей в базу данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # вывод записей в базу данных
    def view_records(self):
        self.db.c.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# создание класса для окна добавления записей
class Child(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # добавляем заголовки для строк ввода данных

        label_name = customtkinter.CTkLabel(self, text='ФИО')
        label_name.place(x=50, y=50)

        label_phone_number = customtkinter.CTkLabel(
            self, text='Номер телефона')
        label_phone_number.place(x=50, y=80)

        label_email = customtkinter.CTkLabel(self, text='E-Mail')
        label_email.place(x=50, y=110)

        # добавляем ввод данных

        self.entry_name = customtkinter.CTkEntry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_phone_number = customtkinter.CTkEntry(
            self)
        self.entry_phone_number.place(x=200, y=80)

        self.entry_email = customtkinter.CTkEntry(self)
        self.entry_email.place(x=200, y=110)

        # кнопка закрытия
        self.btn_cancel = customtkinter.CTkButton(self,
                                                  text='Закрыть',
                                                  command=self.destroy)
        self.btn_cancel.place(x=200, y=170)

        # кнопка подтверждения
        self.btn_ok = customtkinter.CTkButton(self,
                                              text='Добавить')
        self.btn_ok.place(x=50, y=170)

        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.records(
                             self.entry_name.get(),
                             self.entry_phone_number.get(),
                             self.entry_email.get()))

# добавляем класс для окна редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = DB()

        try:
            self.default_data()

            self.title("Редактировать позицию")

            # кнопка редактирования
            btn_edit = customtkinter.CTkButton(self, text="Редактировать")
            btn_edit.place(x=50, y=170)
            btn_edit.bind('<Button-1>', lambda event:
            self.view.update_records(self.entry_name.get(),
                                    self.entry_phone_number.get(),
                                    self.entry_email.get()
                                    ))
            btn_edit.bind("<Button-1>", lambda event:
            self.destroy(), add="+")
            self.btn_ok.destroy()

        except IndexError:
            messagebox.showerror("Ошибка!", "Пожалуйста, выберите сотрудника!")
            self.destroy()


    def default_data(self):
        self.db.c.execute("""
        SELECT * FROM db WHERE id = ?
        """, (self.view.tree.set(self.view.tree.selection()[0], "#1"),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone_number.insert(0, row[3])

# создание класса для поиска
class Search(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.grab_set()
        self.focus_set()

        self.title("Поиск")
        self.geometry("300x100")
        self.resizable(False, False)

        # добавляем заголовки для поля поиска
        label_search = customtkinter.CTkLabel(self, text="Поиск")
        label_search.place(x=50, y=20)

        # добавляем поле поиска
        self.entry_search = customtkinter.CTkEntry(self)
        self.entry_search.place(x=105, y=20)

        # добавляем кнопку закрытия
        btn_cancel = customtkinter.CTkButton(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=155, y=60)

        # добавляем кнопку поиска
        btn_search = customtkinter.CTkButton(self, text="Поиск")
        btn_search.place(x=10, y=60)
        btn_search.bind("<Button-1>",
                        lambda event: self.view.search_record(self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")

# создаем класс с базой данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''
CREATE TABLE IF NOT EXISTS db(id INTEGER primary key, name text, phone text, email text)
''')
        self.conn.commit()

    def insert_data(self, name, phone, email):
        self.c.execute('''
INSERT INTO db (name, phone, email) VALUES (?, ?, ?)
''', (name, phone, email))
        self.conn.commit()

# запуск программы
if __name__ == '__main__':
    app = Main()
    app.mainloop()