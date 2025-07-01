TEST
# 🚀 Sistema de Gestión Ágil - Historias de Usuario y Tareas

> **Aplicación Flask moderna con IA integrada para la gestión ágil de proyectos**

Sistema completo de gestión de historias de usuario y tareas con integración de Azure OpenAI para automatización inteligente, arquitectura modular y pipeline CI/CD con Docker.

## 🏗️ Arquitectura y Tecnologías

### Backend
- **Framework**: Flask 3.1.1 con arquitectura modular
- **Base de Datos**: MySQL con SQLAlchemy ORM
- **Validación**: Pydantic para schemas y serialización
- **IA**: Azure OpenAI GPT-4 para generación automática

### Frontend
- **Templates**: Jinja2 con Bootstrap 5
- **Interfaz**: Responsive design con feedback visual
- **UX**: Spinners de carga y alertas interactivas

### DevOps
- **Contenedores**: Docker y Dockerfile optimizado
- **CI/CD**: GitHub Actions con testing y deploy automático
- **Testing**: Pytest con coverage reporting
- **Entorno**: Virtual environment con Python 3.11

## 📁 Estructura del Proyecto

```
ProyectoUNIR/
├── 📁 src/                          # Código fuente principal
│   ├── 📁 models/                   # Modelos SQLAlchemy
│   │   ├── task.py                  # Modelo Task con enums
│   │   ├── user_story.py            # Modelo UserStory
│   │   └── enums.py                 # PriorityEnum, StatusEnum
│   ├── 📁 schemas/                  # Validación Pydantic
│   │   ├── task_schema.py           # Schema para tareas
│   │   └── user_story_schema.py     # Schema para historias
│   ├── 📁 managers/                 # Lógica de negocio
│   │   ├── task_manager.py          # CRUD y operaciones Task
│   │   └── user_story_manager.py    # CRUD y operaciones UserStory
│   ├── 📁 routes/                   # Endpoints REST y vistas
│   │   ├── task_routes.py           # API y rutas IA tareas
│   │   └── user_story_routes.py     # API y rutas IA historias
│   ├── 📁 templates/                # Vistas Jinja2
│   │   ├── user-stories.html        # Interfaz historias
│   │   └── tasks.html               # Interfaz tareas
│   ├── config.py                    # Configuración aplicación
│   ├── db.py                        # Setup MySQL/SQLAlchemy
│   └── utils.py                     # Utilidades generales
├── 📁 ai/                           # Módulo de IA
│   ├── ia_client.py                 # Cliente Azure OpenAI
│   └── ia_task_manager.py           # Generación automática tareas
├── 📁 tests/                        # Suite de testing
│   └── test_user_story_routes.py    # Tests unitarios
├── 📁 .github/workflows/            # CI/CD Pipeline
│   └── ci.yml                       # GitHub Actions
├── 📁 htmlcov/                      # Reportes de cobertura
├── 📁 env/                          # Virtual environment
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias Python
├── Dockerfile                       # Imagen Docker
└── README.md                        # Documentación
```

## ⚡ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd ProyectoUNIR
```

### 2. Configurar entorno virtual
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de entorno
Crear archivo `.env` con:
```env
# Base de datos MySQL
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_HOST=tu_host
MYSQL_PORT=3306
MYSQL_DB=nombre_bd
MYSQL_SSL_CA=ruta_certificado  # Opcional para Azure

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://tu-instancia.openai.azure.com/
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_MODEL=gpt-4
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

🌐 **Aplicación disponible en**: http://localhost:5000

## 🔗 API Endpoints

### 📋 Historias de Usuario

#### REST API (JSON)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/user_stories` | Crear historia de usuario |
| `GET` | `/user_stories` | Listar todas las historias |
| `GET` | `/user_stories/{id}` | Obtener historia específica |
| `PUT` | `/user_stories/{id}` | Actualizar historia |
| `DELETE` | `/user_stories/{id}` | Eliminar historia |

#### Vistas HTML + IA
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/user-stories` | Interfaz web de gestión |
| `POST` | `/user-stories` | Generar historia desde prompt IA |
| `POST` | `/user-stories/{id}/generate-tasks` | Auto-generar tareas con IA |
| `GET` | `/user-stories/{id}/tasks` | Ver tareas de una historia |

### 📝 Tareas

#### REST API (JSON)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/tasks` | Crear tarea |
| `GET` | `/tasks` | Listar todas las tareas |
| `GET` | `/tasks/{id}` | Obtener tarea específica |
| `PUT` | `/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/tasks/{id}` | Eliminar tarea |

#### Endpoints IA para Tareas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/ai/tasks/describe` | Generar descripción automática |
| `POST` | `/ai/tasks/categorize` | Categorizar tarea automáticamente |
| `POST` | `/ai/tasks/estimate` | Estimar esfuerzo en horas |
| `POST` | `/ai/tasks/audit` | Auditoría completa de tarea |

## 💡 Ejemplos de Uso

### Crear Historia de Usuario
```bash
curl -X POST http://localhost:5000/user_stories \
  -H "Content-Type: application/json" \
  -d '{
    "project": "E-commerce Platform",
    "role": "Como cliente",
    "goal": "quiero poder realizar pagos seguros",
    "reason": "para completar mis compras con confianza",
    "description": "Sistema de pagos con múltiples métodos y verificación",
    "priority": "alta",
    "story_points": 8,
    "effort_hours": 16
  }'
```

### Crear Tarea
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Integrar pasarela de pago Stripe",
    "description": "Implementar SDK de Stripe para procesamiento seguro",
    "priority": "alta",
    "effort_hours": 6,
    "status": "pendiente",
    "assigned_to": "Backend Team",
    "user_story_id": 1
  }'
```

### Generar con IA desde Prompt
```bash
# Generar historia de usuario desde descripción natural
curl -X POST http://localhost:5000/user-stories \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Necesito una funcionalidad para que los usuarios puedan resetear su contraseña por email"
  }'
```

## 🤖 Funcionalidades de IA

### Generación Automática
- **Historias de Usuario**: Desde prompts en lenguaje natural
- **Descomposición en Tareas**: Breakdown automático de historias
- **Descripciones Técnicas**: Generación de documentación detallada
- **Estimaciones de Esfuerzo**: Cálculo inteligente de horas
- **Categorización**: Clasificación automática (Backend, Frontend, Testing, etc.)

### Tipos de Respuesta IA
- **Technical** (Técnica): Respuestas precisas y estructuradas
- **Creative** (Creativa): Generación de contenido innovador
- **Analytics** (Analítica): Análisis y estimaciones de datos
- **Default** (Por defecto): Respuesta equilibrada

## 🧪 Testing y Calidad

### Ejecutar Tests
```bash
# Tests básicos
pytest tests/ --maxfail=5 --disable-warnings

# Con cobertura
pytest --cov=src tests/

# Reporte HTML de cobertura
pytest --cov=src --cov-report=html tests/
# Ver en: htmlcov/index.html
```

### Pipeline CI/CD
El proyecto incluye GitHub Actions que:
1. ✅ Ejecuta tests automáticamente
2. 📊 Genera reportes de cobertura
3. 🐳 Construye imagen Docker
4. 🚀 Publica en Docker Hub

## 🐳 Docker

### Construir imagen
```bash
docker build -t proyecto-unir-pipe .
```

### Ejecutar contenedor
```bash
docker run -d -p 5000:5000 \
  --env-file .env \
  --name proyecto-unir-container \
  proyecto-unir-pipe
```

### Docker Compose (recomendado)
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=root
      - MYSQL_PASSWORD=password
      - MYSQL_DB=taskdb
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: taskdb
    ports:
      - "3306:3306"
```

## 📊 Modelos de Datos

### UserStory
```python
{
  "id": int,
  "project": str,
  "role": str,           # "Como [rol]"
  "goal": str,           # "quiero [objetivo]"
  "reason": str,         # "para [beneficio]"
  "description": str,
  "priority": enum,      # baja, media, alta, bloqueante
  "story_points": int,
  "effort_hours": float,
  "created_at": datetime
}
```

### Task
```python
{
  "id": int,
  "title": str,
  "description": str,
  "priority": enum,      # baja, media, alta, bloqueante
  "effort_hours": float,
  "status": enum,        # pendiente, en_progreso, en_revision, completada
  "assigned_to": str,
  "user_story_id": int,  # Foreign Key opcional
  "created_at": datetime
}
```

## 🔧 Configuración Avanzada

### Parámetros de IA Personalizables
```python
# En ai/ia_client.py
ResponseType.TECHNICAL    # temperature=0.2, top_p=0.4
ResponseType.CREATIVE     # temperature=1.5, top_p=1.0
ResponseType.ANALYTICS    # temperature=0.5, top_p=0.8
```

### Base de Datos
- **Desarrollo**: SQLite local (por defecto)
- **Producción**: MySQL/Azure Database for MySQL
- **SSL**: Soporte para conexiones seguras

### Debug y Desarrollo
```python
# Activar debug mode
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Flask Debug Toolbar incluida
```

## 📈 Roadmap y Mejoras Futuras

- [ ] **Autenticación JWT** para API segura
- [ ] **WebSockets** para actualizaciones en tiempo real
- [ ] **Dashboard Analytics** con métricas de proyecto
- [ ] **Exportación** a Jira/Azure DevOps
- [ ] **API GraphQL** alternativa a REST
- [ ] **Mobile App** con React Native
- [ ] **Integración Slack/Teams** para notificaciones

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [Tu GitHub](https://github.com/tuusuario)

## 🙏 Reconocimientos

- **Azure OpenAI** por la integración de IA
- **Flask Community** por el framework robusto
- **Bootstrap** por el framework CSS
- **UNIR** por el contexto académico del proyecto

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐
