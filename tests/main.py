import tkinter as tk
from tkinter import ttk, messagebox

class AnimalShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Приют животных")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Хранилище данных: {id: {...}}
        self.animals = {}
        self.next_id = 1

        # --- Левая панель: добавление животного ---
        left_frame = tk.LabelFrame(root, text="Добавить животное", padx=10, pady=10, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(left_frame, text="Кличка:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_name = tk.Entry(left_frame, width=25)
        self.entry_name.grid(row=0, column=1, pady=3)

        tk.Label(left_frame, text="Вид:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=3)
        self.combo_species = ttk.Combobox(left_frame, values=["кошка", "собака", "другое"], state="readonly", width=22)
        self.combo_species.current(0)
        self.combo_species.grid(row=1, column=1, pady=3)

        tk.Label(left_frame, text="Возраст (лет):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=3)
        self.entry_age = tk.Entry(left_frame, width=25)
        self.entry_age.grid(row=2, column=1, pady=3)

        tk.Label(left_frame, text="Описание:", bg="#f0f0f0").grid(row=3, column=0, sticky="nw", pady=3)
        self.text_desc = tk.Text(left_frame, width=25, height=4)
        self.text_desc.grid(row=3, column=1, pady=3)

        btn_add = tk.Button(left_frame, text="➕ Добавить", command=self.add_animal, bg="#4CAF50", fg="white", width=20)
        btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Левая панель: поиск и фильтры ---
        filter_frame = tk.LabelFrame(root, text="Поиск и фильтры", padx=10, pady=10, bg="#f0f0f0")
        filter_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(filter_frame, text="Поиск по кличке:", bg="#f0f0f0").pack(anchor="w")
        self.entry_search = tk.Entry(filter_frame, width=28)
        self.entry_search.pack(pady=3)
        self.entry_search.bind("<KeyRelease>", lambda e: self.refresh_table())

        tk.Label(filter_frame, text="Показать:", bg="#f0f0f0").pack(anchor="w", pady=(10, 0))
        self.filter_var = tk.StringVar(value="все")
        for text, val in [("Все", "все"), ("Только кошки", "кошка"), ("Только собаки", "собака")]:
            tk.Radiobutton(filter_frame, text=text, variable=self.filter_var, value=val,
                           command=self.refresh_table, bg="#f0f0f0").pack(anchor="w")

        tk.Button(filter_frame, text="✅ Отметить, что нашел хозяина",
                  command=self.mark_adopted, bg="#2196F3", fg="white", wraplength=200).pack(pady=15, fill=tk.X)

        tk.Button(filter_frame, text="🔄 Сбросить фильтры", command=self.reset_filters, width=25).pack(pady=5)

        # --- Правая панель: таблица животных ---
        right_frame = tk.Frame(root, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(right_frame, text="Список животных в приюте", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")

        columns = ("id", "name", "species", "age", "description", "status")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Кличка")
        self.tree.heading("species", text="Вид")
        self.tree.heading("age", text="Возраст")
        self.tree.heading("description", text="Описание")
        self.tree.heading("status", text="Статус")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=100)
        self.tree.column("species", width=80)
        self.tree.column("age", width=60, anchor="center")
        self.tree.column("description", width=250)
        self.tree.column("status", width=150)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Цветовые теги для статуса
        self.tree.tag_configure("adopted", background="#c8e6c9")  # зеленый
        self.tree.tag_configure("available", background="#ffcdd2") # красный

        # Добавим пару примеров
        self.add_animal_data("Барсик", "кошка", 3, "Ласковый, любит спать.")
        self.add_animal_data("Шарик", "собака", 5, "Активный, нужен выгул.")

    def add_animal_data(self, name, species, age, description):
        self.animals[self.next_id] = {
            "name": name, "species": species, "age": age,
            "description": description, "has_home": False
        }
        self.next_id += 1

    def add_animal(self):
        name = self.entry_name.get().strip()
        species = self.combo_species.get()
        age_str = self.entry_age.get().strip()
        description = self.text_desc.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Ошибка", "Введите кличку животного!")
            return
        try:
            age = int(age_str)
            if age < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст должен быть целым неотрицательным числом!")
            return

        self.add_animal_data(name, species, age, description if description else "—")
        self.refresh_table()

        # Очистка полей
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.text_desc.delete("1.0", tk.END)
        messagebox.showinfo("Успех", f"Животное '{name}' добавлено!")

    def refresh_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_query = self.entry_search.get().strip().lower()
        species_filter = self.filter_var.get()

        for animal_id, data in self.animals.items():
            # Фильтр по кличке
            if search_query and search_query not in data["name"].lower():
                continue
            # Фильтр по виду
            if species_filter != "все" and data["species"] != species_filter:
                continue

            status = "✅ Нашел хозяина" if data["has_home"] else "❌ Ищет хозяина"
            tag = "adopted" if data["has_home"] else "available"

            self.tree.insert("", tk.END, values=(
                animal_id, data["name"], data["species"], data["age"],
                data["description"], status
            ), tags=(tag,))

    def mark_adopted(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите животное в таблице (кликните по строке).")
            return

        # Получаем ID животного из выделенной строки
        animal_id = int(self.tree.item(selected[0])["values"][0])

        if self.animals[animal_id]["has_home"]:
            messagebox.showinfo("Информация", "Это животное уже нашло хозяина.")
            return

        self.animals[animal_id]["has_home"] = True
        self.refresh_table()
        messagebox.showinfo("Отлично!", f"{self.animals[animal_id]['name']} теперь дома! 🏠")

    def reset_filters(self):
        self.entry_search.delete(0, tk.END)
        self.filter_var.set("все")
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalShelterApp(root)
    root.mainloop()