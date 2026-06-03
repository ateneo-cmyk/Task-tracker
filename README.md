# Task Tracker CLI

Una aplicación de línea de comandos (CLI) simple y eficiente para gestionar tus tareas diarias. Este proyecto permite crear, listar y actualizar tareas, manteniendo la persistencia de los datos en un archivo JSON local.

## 🚀 Características

- **Gestión de Tareas**: Añade descripciones y realiza un seguimiento de tus pendientes.
- **Persistencia de Datos**: Todas las tareas se guardan automáticamente en un archivo `task.json`.
- **Filtrado Inteligente**: Lista todas tus tareas o fíltralas por estado (`todo`, `in-progress`, `done`).
- **Interfaz Interactiva**: Utiliza el módulo `cmd` de Python para ofrecer una experiencia de terminal fluida.
- **IDs Automáticos**: Gestión automática de identificadores únicos para cada tarea.

## 🛠️ Instalación

Para instalar la herramienta de forma local y utilizarla como un comando global, sigue estos pasos:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/task-tracker.git
   cd task-tracker
   ```

2. **Instala el paquete**:
   Puedes instalarlo en modo desarrollo para que los cambios que realices se apliquen inmediatamente:
   ```bash
   pip install -e .
   ```

## 💻 Uso

Una vez instalado, puedes iniciar la aplicación simplemente escribiendo:

```bash
task-tracker
```

### Comandos Disponibles

Dentro de la interfaz interactiva `(TaskManager)`, puedes usar los siguientes comandos:

- **Añadir una tarea**: `add <descripción>`
  - Ejemplo: `add Comprar leche`
- **Listar tareas**: `list` o `list <estado>`
  - Ejemplo (todas): `list`
  - Ejemplo (filtrado): `list done` o `list in-progress`
- **Actualizar descripción**: `update <id> <nueva descripción>`
  - Ejemplo: `update 1 Comprar leche deslactosada`
- **Salir**: `exit` o `quit`

## 📁 Estructura del Proyecto

- `src/task_module.py`: Contiene la lógica principal, la clase `Task` y el loop de la CLI.
- `src/__main__.py`: Punto de entrada de la aplicación.
- `task.json`: Archivo donde se almacenan los datos (se genera automáticamente).
- `setup.py`: Configuración para la instalación del paquete de Python.

## 📝 Ejemplo de Almacenamiento (JSON)

Las tareas se guardan con el siguiente formato:
```json
{
    "id": 1,
    "description": "Finalizar proyecto CLI",
    "status": "todo",
    "createdAt": "2026-06-03T17:56:22",
    "updatedAt": null
}
```
