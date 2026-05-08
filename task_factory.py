from task_model import Task, TaskType, Difficulty
import random

class TaskFactory:
    """Фабрика для создания различных типов задач"""
    
    _work_tasks = [
        "Complete project report",
        "Attend team meeting",
        "Write documentation",
        "Review pull requests",
        "Fix critical bug",
        "Plan next sprint",
        "Update dependencies",
        "Conduct code review"
    ]
    
    _sport_tasks = [
        "Run 5 kilometers",
        "Do 50 pushups",
        "Swim 20 laps",
        "Yoga session",
        "Hit the gym",
        "Play basketball",
        "Cycling for 30 minutes",
        "Stretching routine"
    ]
    
    _study_tasks = [
        "Read 20 pages of book",
        "Complete online course module",
        "Practice coding for 1 hour",
        "Learn new language vocabulary",
        "Watch educational video",
        "Solve math problems",
        "Write study notes",
        "Review previous lessons"
    ]
    
    @classmethod
    def create_work_task(cls, description=None, difficulty=None):
        """Создание рабочей задачи"""
        if description is None:
            description = random.choice(cls._work_tasks)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.WORK, difficulty)
    
    @classmethod
    def create_sport_task(cls, description=None, difficulty=None):
        """Создание спортивной задачи"""
        if description is None:
            description = random.choice(cls._sport_tasks)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.SPORT, difficulty)
    
    @classmethod
    def create_study_task(cls, description=None, difficulty=None):
        """Создание учебной задачи"""
        if description is None:
            description = random.choice(cls._study_tasks)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.STUDY, difficulty)
    
    @classmethod
    def create_random_task(cls):
        """Создание случайной задачи"""
        task_creators = [
            cls.create_work_task,
            cls.create_sport_task,
            cls.create_study_task
        ]
        creator = random.choice(task_creators)
        return creator()
    
    @classmethod
    def create_custom_task(cls, description, task_type_str, difficulty_str):
        """Создание пользовательской задачи с валидацией"""
        try:
            task_type = TaskType(task_type_str)
            difficulty = Difficulty(difficulty_str)
            return Task(description, task_type, difficulty)
        except ValueError as e:
            raise ValueError(f"Invalid task parameters: {e}")