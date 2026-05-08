from collections import deque
from task_model import Task, TaskType, Difficulty
from task_factory import TaskFactory
import json
import random

class TaskManager:
    """Менеджер для управления задачами"""
    
    DATA_FILE = "data_f.json"
    
    def __init__(self):
        self._history = deque(maxlen=100)  # Очередь истории задач
        self._tasks = []  # Список всех задач
        self.load_data()
    
    def generate_random_task(self):
        """Генерация случайной задачи"""
        task = TaskFactory.create_random_task()
        self._history.append(task)
        self._tasks.append(task)
        self.save_data()
        return task
    
    def add_custom_task(self, description, task_type, difficulty):
        """Добавление пользовательской задачи"""
        try:
            task = TaskFactory.create_custom_task(description, task_type, difficulty)
            self._tasks.append(task)
            self.save_data()
            return task
        except ValueError as e:
            raise ValueError(f"Cannot add task: {e}")
    
    def filter_tasks(self, task_type=None, difficulty=None):
        """Фильтрация задач по типу и сложности"""
        filtered = self._tasks.copy()
        
        if task_type:
            filtered = [t for t in filtered if t.type.value == task_type]
        
        if difficulty:
            filtered = [t for t in filtered if t.difficulty.value == difficulty]
        
        return filtered
    
    def get_history(self, limit=None):
        """Получение истории задач"""
        if limit:
            return list(self._history)[-limit:]
        return list(self._history)
    
    def clear_history(self):
        """Очистка истории"""
        self._history.clear()
        self.save_data()
    
    def save_data(self):
        """Сохранение данных в JSON"""
        data = {
            'history': [task.to_dict() for task in self._history],
            'tasks': [task.to_dict() for task in self._tasks]
        }
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._history = deque(
                    [Task.from_dict(task) for task in data.get('history', [])],
                    maxlen=100
                )
                self._tasks = [Task.from_dict(task) for task in data.get('tasks', [])]
        except FileNotFoundError:
            # Создаем файл с начальными данными
            self._initialize_default_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Инициализация начальными данными"""
        default_tasks = [
            TaskFactory.create_work_task(),
            TaskFactory.create_sport_task(),
            TaskFactory.create_study_task()
        ]
        self._tasks = default_tasks
        self.save_data()
