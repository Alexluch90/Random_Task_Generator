import json
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    WORK = "Work"
    SPORT = "Sport"
    STUDY = "Study"

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Task:
    """Базовый класс задачи"""
    
    def __init__(self, description: str, task_type: TaskType, difficulty: Difficulty):
        self._description = description
        self._type = task_type
        self._difficulty = difficulty
        self._created_at = datetime.now()
    
    # Геттеры
    @property
    def description(self):
        return self._description
    
    @property
    def type(self):
        return self._type
    
    @property
    def difficulty(self):
        return self._difficulty
    
    @property
    def created_at(self):
        return self._created_at
    
    # Сеттеры с валидацией
    @description.setter
    def description(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Description must be a non-empty string")
        self._description = value
    
    @type.setter
    def type(self, value):
        if not isinstance(value, TaskType):
            raise ValueError("Invalid task type")
        self._type = value
    
    @difficulty.setter
    def difficulty(self, value):
        if not isinstance(value, Difficulty):
            raise ValueError("Invalid difficulty level")
        self._difficulty = value
    
    def to_dict(self):
        """Конвертация задачи в словарь для JSON"""
        return {
            'description': self._description,
            'type': self._type.value,
            'difficulty': self._difficulty.value,
            'created_at': self._created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создание задачи из словаря"""
        task_type = TaskType(data['type'])
        difficulty = Difficulty(data['difficulty'])
        task = cls(data['description'], task_type, difficulty)
        task._created_at = datetime.fromisoformat(data['created_at'])
        return task
    
    def __str__(self):
        return f"[{self._type.value}] {self._description} (Difficulty: {self._difficulty.value})"