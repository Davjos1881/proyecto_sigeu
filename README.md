# Backend Proyecto Sigeu

Proyecto backend construido con **FastAPI** y **MySQL**, utilizando **SQLAlchemy** como ORM y **asyncmy** como driver de conexión asincrónica.

## Requisitos

- Python 3.11.x
- MySQL Server (local o remoto)
- Entorno virtual (`.venv`)

## Estructura del proyecto
```
backend_sigeu/
│
├── app/
│   ├── api/                  # Rutas y versiones de la API
│   ├── crud/                 # Operaciones CRUD con SQLAlchemy
│   ├── db/                   # Configuración de la base de datos
│   ├── models/               # Modelos ORM
│   ├── schemas/              # Esquemas Pydantic
│   ├── services/             # Lógica de negocio
│   └── main.py               # Punto de entrada de la app FastAPI
│
├── .env                      # Variables de entorno
├── requirements.txt          # Dependencias del proyecto
└── README.md
```

## Instalación

### 1. Crear y activar el entorno virtual

#### Windows
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

---

### 2. Instalación de Python (si no está disponible)

- **Windows**  
  Descargar el instalador desde el sitio oficial:  
  [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

- **macOS**  
  1. Verificar la versión instalada:  
     ```bash
     python3 --version
     ```
  2. Si usas **Homebrew**, listar versiones instaladas:  
     ```bash
     brew list --versions | grep python
     ```
  3. Para instalar una versión específica (ejemplo: Python 3.13):  
     ```bash
     brew install python@3.13
     ```
  4. Si no usas Homebrew, descarga el instalador oficial:  
     [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)

---

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear el archivo `.env` en la raíz del proyecto con las variables de entorno:
```bash
DATABASE_URL=mysql+asyncmy://usuario:contraseña@localhost:3306/hospital_db
DEBUG=true # para desarrollo
APP_NAME=Nombre del proyecto
APP_VERSION=Version
ALLOWED_ORIGINS=["*"]
```

### 5. Ejecutar el servidor
```bash
uvicorn app.main:app --reload
```
