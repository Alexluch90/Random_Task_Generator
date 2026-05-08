# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager
from task_model import TaskType, Difficulty
import sys

class RandomTaskGeneratorApp:
    """Главное приложение с GUI на Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Установка кодировки для консоли (только для Windows)
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        self.task_manager = TaskManager()
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения
        self.refresh_display()
    
    def setup_styles(self):
        """Настройка стилей интерфейса"""
        style = ttk.Style()
        
        # Попытка использовать доступную тему
        try:
            style.theme_use('vista')
        except:
            try:
                style.theme_use('clam')
            except:
                pass
        
        # Настройка цветов для темного фона (опционально)
        self.root.configure(bg='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', foreground='#000000', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 9, 'italic'))
    
    def create_widgets(self):
        """Создание всех виджетов"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка веса для главного фрейма
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Random Task Generator", style='Header.TLabel')
        title_label.grid(row=0, column=0, pady=10)
        
        # Информационная панель
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        total_label = ttk.Label(info_frame, text="Total Tasks: 0", style='Status.TLabel')
        total_label.grid(row=0, column=0, padx=5)
        
        # Кнопка генерации
        generate_btn = ttk.Button(main_frame, text="Generate Random Task", 
                                  command=self.generate_task, width=30)
        generate_btn.grid(row=2, column=0, pady=10)
        
        # Фрейм для добавления задачи
        self.create_add_task_frame(main_frame)
        
        # Фрейм для фильтрации
        self.create_filter_frame(main_frame)
        
        # Фрейм для отображения задач
        self.create_display_frame(main_frame)
        
        # Фрейм для истории
        self.create_history_frame(main_frame)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                               style='Status.TLabel', relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
    
    def create_add_task_frame(self, parent):
        """Фрейм для добавления новой задачи"""
        add_frame = ttk.LabelFrame(parent, text="Add Custom Task", padding="10")
        add_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        add_frame.columnconfigure(1, weight=1)
        
        # Описание
        ttk.Label(add_frame, text="Description:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.desc_entry = ttk.Entry(add_frame, width=50)
        self.desc_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Тип
        ttk.Label(add_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                  values=[t.value for t in TaskType], 
                                  width=20, state="readonly")
        type_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        type_combo.set(TaskType.WORK.value)
        
        # Сложность
        ttk.Label(add_frame, text="Difficulty:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.diff_var = tk.StringVar()
        diff_combo = ttk.Combobox(add_frame, textvariable=self.diff_var, 
                                  values=[d.value for d in Difficulty], 
                                  width=20, state="readonly")
        diff_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        diff_combo.set(Difficulty.MEDIUM.value)
        
        # Кнопка добавления
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        add_btn = ttk.Button(button_frame, text="Add Task", command=self.add_custom_task, width=15)
        add_btn.grid(row=0, column=0, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields, width=15)
        clear_btn.grid(row=0, column=1, padx=5)
    
    def create_filter_frame(self, parent):
        """Фрейм для фильтрации задач"""
        filter_frame = ttk.LabelFrame(parent, text="Filter Tasks", padding="10")
        filter_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="Task Type:").grid(row=0, column=0, padx=5)
        self.filter_type_var = tk.StringVar()
        filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                         values=["All"] + [t.value for t in TaskType], 
                                         width=15, state="readonly")
        filter_type_combo.grid(row=0, column=1, padx=5)
        filter_type_combo.set("All")
        
        # Фильтр по сложности
        ttk.Label(filter_frame, text="Difficulty:").grid(row=0, column=2, padx=5)
        self.filter_diff_var = tk.StringVar()
        filter_diff_combo = ttk.Combobox(filter_frame, textvariable=self.filter_diff_var,
                                         values=["All"] + [d.value for d in Difficulty], 
                                         width=15, state="readonly")
        filter_diff_combo.grid(row=0, column=3, padx=5)
        filter_diff_combo.set("All")
        
        # Кнопки
        button_frame = ttk.Frame(filter_frame)
        button_frame.grid(row=0, column=4, padx=10)
        
        filter_btn = ttk.Button(button_frame, text="Apply Filter", command=self.apply_filter, width=12)
        filter_btn.grid(row=0, column=0, padx=2)
        
        reset_btn = ttk.Button(button_frame, text="Reset", command=self.reset_filter, width=12)
        reset_btn.grid(row=0, column=1, padx=2)
    
    def create_display_frame(self, parent):
        """Фрейм для отображения задач"""
        display_frame = ttk.LabelFrame(parent, text="Tasks List", padding="10")
        display_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Создание Treeview для отображения задач
        columns = ('Description', 'Type', 'Difficulty', 'Created')
        self.tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=10)
        
        # Настройка заголовков
        self.tree.heading('Description', text='Description')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Difficulty', text='Difficulty')
        self.tree.heading('Created', text='Created')
        
        # Настройка ширины колонок
        self.tree.column('Description', width=400)
        self.tree.column('Type', width=100)
        self.tree.column('Difficulty', width=100)
        self.tree.column('Created', width=120)
        
        # Скроллбары
        vsb = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Размещение
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Контекстное меню для Treeview
        self.create_context_menu()
    
    def create_context_menu(self):
        """Создание контекстного меню"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy Description", command=self.copy_description)
        
        # Привязка контекстного меню
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Показ контекстного меню"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_description(self):
        """Копирование описания задачи в буфер обмена"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            if values:
                self.root.clipboard_clear()
                self.root.clipboard_append(values[0])
                self.status_var.set("Description copied to clipboard")
    
    def create_history_frame(self, parent):
        """Фрейм для отображения истории"""
        history_frame = ttk.LabelFrame(parent, text="Generation History (Last 10)", padding="10")
        history_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
        history_frame.columnconfigure(0, weight=1)
        
        # Создание списка для истории
        self.history_listbox = tk.Listbox(history_frame, height=5, bg='#ffffff', 
                                          fg='#000000', font=('Arial', 9))
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Скроллбар для истории
        history_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, 
                                       command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=history_scroll.set)
        history_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки
        button_frame = ttk.Frame(history_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear History", command=self.clear_history, width=15)
        clear_btn.grid(row=0, column=0, padx=5)
        
        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.update_history, width=15)
        refresh_btn.grid(row=0, column=1, padx=5)
    
    def generate_task(self):
        """Генерация случайной задачи"""
        try:
            task = self.task_manager.generate_random_task()
            self.refresh_display()
            self.status_var.set(f"Generated: {task.description[:50]}")
            messagebox.showinfo("Success", f"New task generated!\n\n{task}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate task: {str(e)}")
            self.status_var.set("Error generating task")
    
    def add_custom_task(self):
        """Добавление пользовательской задачи"""
        description = self.desc_entry.get().strip()
        
        # Валидация ввода
        if not description:
            messagebox.showwarning("Input Error", "Please enter a task description")
            self.status_var.set("Error: Empty description")
            return
        
        if len(description) > 200:
            messagebox.showwarning("Input Error", "Description too long (max 200 characters)")
            self.status_var.set("Error: Description too long")
            return
        
        task_type = self.type_var.get()
        difficulty = self.diff_var.get()
        
        try:
            task = self.task_manager.add_custom_task(description, task_type, difficulty)
            self.refresh_display()
            self.clear_fields()
            self.status_var.set(f"Added: {description[:50]}")
            messagebox.showinfo("Success", f"Task added successfully!\n\n{task}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error adding task")
    
    def clear_fields(self):
        """Очистка полей ввода"""
        self.desc_entry.delete(0, tk.END)
        self.type_var.set(TaskType.WORK.value)
        self.diff_var.set(Difficulty.MEDIUM.value)
        self.status_var.set("Fields cleared")
    
    def apply_filter(self):
        """Применение фильтра"""
        try:
            task_type = self.filter_type_var.get()
            difficulty = self.filter_diff_var.get()
            
            # Преобразование "All" в None
            task_type = None if task_type == "All" else task_type
            difficulty = None if difficulty == "All" else difficulty
            
            filtered_tasks = self.task_manager.filter_tasks(task_type, difficulty)
            self.update_treeview(filtered_tasks)
            
            filter_text = []
            if task_type:
                filter_text.append(f"type={task_type}")
            if difficulty:
                filter_text.append(f"difficulty={difficulty}")
            
            if filter_text:
                self.status_var.set(f"Filtered by: {', '.join(filter_text)} ({len(filtered_tasks)} tasks)")
            else:
                self.status_var.set(f"Showing all tasks ({len(filtered_tasks)} tasks)")
        except Exception as e:
            messagebox.showerror("Error", f"Filter failed: {str(e)}")
    
    def reset_filter(self):
        """Сброс фильтра"""
        self.filter_type_var.set("All")
        self.filter_diff_var.set("All")
        self.update_treeview(self.task_manager._tasks)
        self.status_var.set(f"Filter reset - showing all {len(self.task_manager._tasks)} tasks")
    
    def update_treeview(self, tasks):
        """Обновление Treeview задачами"""
        # Очистка текущих элементов
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление задач
        for task in tasks:
            created_time = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            self.tree.insert('', tk.END, values=(
                task.description,
                task.type.value,
                task.difficulty.value,
                created_time
            ))
    
    def update_history(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        history = self.task_manager.get_history(10)
        
        if not history:
            self.history_listbox.insert(tk.END, "No tasks generated yet")
        else:
            for i, task in enumerate(reversed(history), 1):
                display_text = f"{i:2}. [{task.type.value[:4]}] {task.description[:60]}"
                self.history_listbox.insert(tk.END, display_text)
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            try:
                self.task_manager.clear_history()
                self.update_history()
                self.status_var.set("History cleared")
                messagebox.showinfo("Success", "History cleared successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history: {str(e)}")
    
    def refresh_display(self):
        """Обновление всего отображения"""
        self.update_treeview(self.task_manager._tasks)
        self.update_history()
        
        # Обновление счетчика задач
        total = len(self.task_manager._tasks)
        for child in self.root.winfo_children():
            for frame in child.winfo_children():
                if isinstance(frame, ttk.Frame) and len(frame.winfo_children()) > 0:
                    for inner in frame.winfo_children():
                        if isinstance(inner, ttk.Label) and inner.cget('text').startswith('Total Tasks:'):
                            inner.configure(text=f"Total Tasks: {total}")
                            break

def main():
    """Главная функция запуска приложения"""
    try:
        root = tk.Tk()
        app = RandomTaskGeneratorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()