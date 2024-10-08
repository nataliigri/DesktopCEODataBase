import tkinter as tk
from tkinter import messagebox, Scrollbar, Frame, Canvas, scrolledtext 
from database import Database, Field

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Система Управління Табличними Базами Даних")

        # Створення прокрутки
        self.canvas = Canvas(root)
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.db = None
        self.create_widgets()

    def create_widgets(self):
        # Введення назви бази даних
        self.db_name_label = tk.Label(self.scrollable_frame, text="Назва бази даних:")
        self.db_name_label.pack()

        self.db_name_entry = tk.Entry(self.scrollable_frame)
        self.db_name_entry.pack()

        self.create_db_button = tk.Button(self.scrollable_frame, text="Створити базу даних", command=self.create_database)
        self.create_db_button.pack()

        # Введення назви таблиці
        self.table_name_label = tk.Label(self.scrollable_frame, text="Назва таблиці:")
        self.table_name_label.pack()

        self.table_name_entry = tk.Entry(self.scrollable_frame)
        self.table_name_entry.pack()

        self.create_table_button = tk.Button(self.scrollable_frame, text="Створити таблицю", command=self.create_table)
        self.create_table_button.pack()

        # Введення полів
        self.field_name_label = tk.Label(self.scrollable_frame, text="Назва поля:")
        self.field_name_label.pack()

        self.field_name_entry = tk.Entry(self.scrollable_frame)
        self.field_name_entry.pack()

        self.field_type_label = tk.Label(self.scrollable_frame, text="Тип поля (integer, real, char, string):")
        self.field_type_label.pack()

        self.field_type_entry = tk.Entry(self.scrollable_frame)
        self.field_type_entry.pack()

        self.add_field_button = tk.Button(self.scrollable_frame, text="Додати поле", command=self.add_field)
        self.add_field_button.pack()

        self.edit_field_button = tk.Button(self.scrollable_frame, text="Редагувати поле", command=self.edit_field)
        self.edit_field_button.pack()

        self.remove_field_button = tk.Button(self.scrollable_frame, text="Видалити поле", command=self.remove_field)
        self.remove_field_button.pack()

        self.save_db_button = tk.Button(self.scrollable_frame, text="Зберегти базу даних", command=self.save_database)
        self.save_db_button.pack()

        self.view_table_button = tk.Button(self.scrollable_frame, text="Переглянути таблицю", command=self.view_table)
        self.view_table_button.pack()

        self.view_all_tables_button = tk.Button(self.scrollable_frame, text="Переглянути всі таблиці", command=self.view_all_tables)
        self.view_all_tables_button.pack()

        # Текстове поле для перегляду даних таблиць
        self.text_area = scrolledtext.ScrolledText(self.root, width=50, height=15)
        self.text_area.pack()

        # Введення назви таблиці 1
        self.table1_name_label = tk.Label(self.root, text="Назва таблиці 1:")
        self.table1_name_label.pack()
        self.table1_name_entry = tk.Entry(self.root)
        self.table1_name_entry.pack()

        # Введення назви таблиці 2
        self.table2_name_label = tk.Label(self.root, text="Назва таблиці 2:")
        self.table2_name_label.pack()
        self.table2_name_entry = tk.Entry(self.root)
        self.table2_name_entry.pack()

        # Введення спільного поля
        self.common_field_label = tk.Label(self.root, text="Назва спільного поля:")
        self.common_field_label.pack()
        self.common_field_entry = tk.Entry(self.root)
        self.common_field_entry.pack()

        # Додаємо текстову область для відображення результатів
        self.result_area = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.result_area.pack()

        self.join_tables_button = tk.Button(self.root, text="Сполучити таблиці", command=self.join_tables)
        self.join_tables_button.pack()

    def create_database(self):
        db_name = self.db_name_entry.get()
        self.db = Database(db_name)
        messagebox.showinfo("Успіх", f"База даних '{db_name}' створена!")

    def create_table(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table_name = self.table_name_entry.get()

        try:
            self.db.create_table(table_name)  # Створюємо таблицю
            messagebox.showinfo("Успіх", f"Таблиця '{table_name}' створена!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def add_field(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table_name = self.table_name_entry.get()
        field_name = self.field_name_entry.get()
        field_type = self.field_type_entry.get()

        if not field_name or not field_type:
            messagebox.showerror("Помилка", "Введіть назву та тип поля.")
            return

        try:
            field = Field(field_name, field_type)
            self.db.add_field_to_table(table_name, field)  # Додаємо поле до таблиці
            messagebox.showinfo("Успіх", f"Поле '{field_name}' додане до таблиці '{table_name}'!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def edit_field(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table_name = self.table_name_entry.get()
        old_field_name = self.field_name_entry.get()
        new_field_name = self.field_name_entry.get()
        new_field_type = self.field_type_entry.get()

        if not old_field_name or not new_field_name or not new_field_type:
            messagebox.showerror("Помилка", "Введіть стару назву поля, нову назву та тип.")
            return

        try:
            new_field = Field(new_field_name, new_field_type)
            self.db.edit_field_in_table(table_name, old_field_name, new_field)
            messagebox.showinfo("Успіх", f"Поле '{old_field_name}' змінено на '{new_field_name}' у таблиці '{table_name}'!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def remove_field(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table_name = self.table_name_entry.get()
        field_name = self.field_name_entry.get()

        if not field_name:
            messagebox.showerror("Помилка", "Введіть назву поля для видалення.")
            return

        try:
            self.db.remove_field_from_table(table_name, field_name)
            messagebox.showinfo("Успіх", f"Поле '{field_name}' видалено з таблиці '{table_name}'!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def save_database(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        try:
            self.db.save_to_disk()
            messagebox.showinfo("Успіх", f"База даних '{self.db.name}' збережена!")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def view_table(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table_name = self.table_name_entry.get()
        
        try:
            table_data = self.db.view_table(table_name)
            fields = "\n".join([f"{field[0]}: {field[1]}" for field in table_data["fields"]])
            self.text_area.delete(1.0, tk.END)  # Очищаємо текстове поле
            self.text_area.insert(tk.END, f"Таблиця '{table_name}' має поля:\n{fields}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def view_all_tables(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        all_tables = self.db.view_all_tables()
        table_info = "\n".join([f"{table_name}: {table['fields']}" for table_name, table in all_tables.items()])
        self.text_area.delete(1.0, tk.END)  # Очищаємо текстове поле
        self.text_area.insert(tk.END, f"В базі даних '{self.db.name}' є таблиці:\n{table_info}")

    def join_tables(self):
        if self.db is None:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних.")
            return

        table1_name = self.table1_name_entry.get()
        table2_name = self.table2_name_entry.get()
        common_field_name = self.common_field_entry.get()

        try:
            # Перевірка наявності таблиць
            if table1_name not in self.db.tables or table2_name not in self.db.tables:
                raise Exception("Одна з таблиць не існує.")

            # Здійснюємо сполучення
            joined_records = self.db.join_tables(table1_name, table2_name, common_field_name)
            joined_info = "\n".join([str(record) for record in joined_records])
            self.result_area.delete(1.0, tk.END)  # Очистити текстову область
            self.result_area.insert(tk.END, f"Сполучені записи:\n{joined_info}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
