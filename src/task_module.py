import json
import cmd
from datetime import datetime
import os
class Task:
    counter = 1 

    def __init__(self, description: str, id=None, status='todo', createdAt=None, updatedAt=None):
        if id is None:
            self.id = Task.counter
            Task.counter += 1
        else:
            self.id = id
            # Asegurarse de que el contador sea siempre mayor que el ID más alto existente
            if id >= Task.counter:
                Task.counter = id + 1

        self.description = description
        self.status = status
        self.createdAt = createdAt or datetime.now()
        self.updatedAt = updatedAt
        
    def to_dict(self):
            return {
                "id": self.id,
                "description": self.description,
                "status": self.status,
                "createdAt": self.createdAt.isoformat(),
                "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None
            }
            
    @classmethod
    def from_dict(cls, data):
            return cls(
                description=data["description"],
                id=data["id"],
                status=data.get("status", "todo"),
                createdAt= datetime.fromisoformat(data["createdAt"]),
                updatedAt= datetime.fromisoformat(data["updatedAt"]) if data.get("updatedAt") else None

            )


    
        
    
            
    
    
    
    def __repr__(self):
        return f"Task(id={self.id!r}, description={self.description!r}, status={self.status!r}, createdAt={self.createdAt!r}, updatedAt={self.updatedAt!r})"

    def update(self, newDescription):
        tasks_data = _get_all_tasks_from_json()
        
        found = False
        for task_dict in tasks_data:
            if task_dict["id"] == self.id:
                task_dict["description"] = newDescription
                task_dict["updatedAt"] = datetime.now().isoformat()
                found = True
                break
        
        if found:
            _save_all_tasks_to_json(tasks_data)
            print(f"Tarea con ID {self.id} actualizada exitosamente.")
        else:
            print(f"Error: No se encontró la tarea con ID {self.id}.")
        
        
    def mark_done(self):
        tasks_data = _get_all_tasks_from_json()
        found = False
        for task_dict in tasks_data:
            if task_dict["id"] == self.id:
                task_dict["status"] = 'done'
                task_dict["updatedAt"] = datetime.now().isoformat()
                found = True
                break
        if found:
            _save_all_tasks_to_json(tasks_data)
            print(f"Tarea con ID {self.id} marcada como 'done'.")
        else:
            print(f"Error: No se encontró la tarea con ID {self.id}.")
            
        
        

    def mark_todo(self):
        tasks_data = _get_all_tasks_from_json()
        found = False
        for task_dict in tasks_data:
            if task_dict["id"] == self.id:
                task_dict["status"] = 'todo'
                task_dict["updatedAt"] = datetime.now().isoformat()
                found = True
                break
        if found:
            _save_all_tasks_to_json(tasks_data)
            print(f"Tarea con ID {self.id} marcada como 'todo'.")
        else:
            print(f"Error: No se encontró la tarea con ID {self.id}.")

    def mark_in_progress(self):
        tasks_data = _get_all_tasks_from_json()
        found = False
        for task_dict in tasks_data:
            if task_dict["id"] == self.id:
                task_dict["status"] = 'in progress'
                task_dict["updatedAt"] = datetime.now().isoformat()
                found = True
                break
        if found:
            _save_all_tasks_to_json(tasks_data)
            print(f"Tarea con ID {self.id} marcada como 'in progress'.")
        else:
            print(f"Error: No se encontró la tarea con ID {self.id}.")
       
 
 
 
def agregar(titulo):
    newTask = Task(titulo)
    
    tasks_data = _get_all_tasks_from_json()
    tasks_data.append(newTask.to_dict())
    _save_all_tasks_to_json(tasks_data)
    
    print(f"Tarea '{titulo}' agregada Exitosamente con ID: {newTask.id}")

def _get_all_tasks_from_json():
    tasks_data = []
    if os.path.exists("task.json"):
        try:
            with open("task.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    tasks_data = data
                elif isinstance(data, dict): # Handle case where it's a single object
                    tasks_data = [data]
        except (json.JSONDecodeError, FileNotFoundError):
            tasks_data = []
    return tasks_data

def _save_all_tasks_to_json(tasks_data_list):
    with open("task.json", "w", encoding="utf-8") as f:
        json.dump(tasks_data_list, f, indent=4, default=str)
        
class TaskCli(cmd.Cmd):
    
    def __init__(self):
        super().__init__()
        print("Interactive Task manager CLI")
        self.prompt = "(TaskManager) "
        self._initialize_task_counter()

    def _initialize_task_counter(self):
        tasks_data = _get_all_tasks_from_json()
        max_id = 0
        if tasks_data:
            max_id = max(t["id"] for t in tasks_data)
        Task.counter = max_id + 1
   
    def do_add(self, arg):
        """Agrega una nueva tarea: add <descripción>"""
        if not arg.strip():
            print("Error: Debes ingresar una descripción para la tarea.")
            return
        agregar(arg.strip())

    def do_list(self, arg):
        """Lista tareas: list o list <status> (todo, in-progress, done)"""
        tasks = _get_all_tasks_from_json()
        if not tasks:
            print("No hay tareas registradas.")
            return

        status_filter = arg.strip().lower()
        # Normalizamos 'in-progress' por si el usuario lo escribe con guion
        if status_filter == "in-progress":
            status_filter = "in progress"

        if status_filter:
            filtered_tasks = [t for t in tasks if t['status'] == status_filter]
            if not filtered_tasks:
                print(f"No se encontraron tareas con el estado: {status_filter}")
                return
            tasks = filtered_tasks

        print(f"\n--- Lista de Tareas ({status_filter if status_filter else 'todas'}) ---")
        for t in tasks:
            status = t['status'].upper()
            print(f"ID: {t['id']} | [{status}] | {t['description']}")

    def do_exit(self, arg):
        """Sale de la aplicación: exit"""
        print("Saliendo del Task Manager...")
        return True
    
    def do_quit(self, arg):
        """Alias para exit: quit"""
        return self.do_exit(arg)

    def do_update(self, arg):
        parts = arg.split(maxsplit=1)
        if len(parts) < 2:
            print("Uso: update <id> <nueva_descripcion>")
            return

        try:
            task_id = int(parts[0])
            new_description = parts[1]
        except ValueError:
            print("Error: El ID de la tarea debe ser un número entero.")
            return

        tasks_data = _get_all_tasks_from_json()
        task_data_to_update = None
        for t_data in tasks_data:
            if t_data["id"] == task_id:
                task_data_to_update = t_data
                break
        
        if task_data_to_update:
            task_instance = Task.from_dict(task_data_to_update)
            task_instance.update(new_description)
        else:
            print(f"Error: No se encontró la tarea con ID {task_id}.")
   
    def do_mark_done(self, arg):
        
        try:
            task_id = int(arg.strip())
            tasks_data = _get_all_tasks_from_json()
            for t_data in tasks_data:
                if t_data["id"] == task_id:
                    task = Task.from_dict(t_data)
                    task.mark_done()
                    return
            print(f"No se encontró la tarea {task_id}")
        except ValueError:
            print("Error: Ingresa un ID numérico válido.")

    def do_mark_in_progress(self, arg):
        """Marca una tarea en progreso: mark_in_progress <id>"""
        try:
            task_id = int(arg.strip())
            tasks_data = _get_all_tasks_from_json()
            for t_data in tasks_data:
                if t_data["id"] == task_id:
                    task = Task.from_dict(t_data)
                    task.mark_in_progress()
                    return
            print(f"No se encontró la tarea {task_id}")
        except ValueError:
            print("Error: Ingresa un ID numérico válido.")

    def do_delete(self, arg):
        """Elimina una tarea: delete <id>"""
        try:
            task_id = int(arg.strip())
            tasks_data = _get_all_tasks_from_json()
            
            initial_count = len(tasks_data)
            tasks_data = [t for t in tasks_data if t["id"] != task_id]
            
            if len(tasks_data) < initial_count:
                _save_all_tasks_to_json(tasks_data)
                print(f"Tarea {task_id} eliminada correctamente.")
            else:
                print(f"No se encontró la tarea {task_id}.")
        except ValueError:
            print("Error: Ingresa un ID numérico válido.")


    
   
    
class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return obj.to_dict()
        return super().default(obj)
    
    
