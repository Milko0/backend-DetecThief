# dominio/repositorios/base_repositorio.py
from abc import ABC, abstractmethod

class BaseRepositorio(ABC):
    @abstractmethod
    def insertar(self, entidad):
        """Método abstracto para insertar entidades"""
        pass