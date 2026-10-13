# 🧪 Load Balancing con HAProxy + Docker + React + FastAPI

Proyecto práctico de **balanceo de carga** que demuestra cómo distribuir el tráfico HTTP entre múltiples instancias de un backend usando **HAProxy** como load balancer, todo orquestado con **Docker Compose**.

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Arquitectura](#-arquitectura)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Descripción de Archivos](#-descripción-de-archivos)
- [Servicios Docker](#-servicios-docker)
- [Configuración de HAProxy](#-configuración-de-haproxy)
- [Frontend React](#-frontend-react)
- [Backend FastAPI](#-backend-fastapi)
- [Pruebas de Carga con JMeter](#-pruebas-de-carga-con-jmeter)
- [URLs de Acceso](#-urls-de-acceso)
- [Verificación del Balanceo](#-verificación-del-balanceo)

---

## 🎯 Descripción General

Este proyecto implementa una arquitectura de microservicios con balanceo de carga:

- Un **frontend** en React + Vite que muestra mensajes del backend.
- **3 instancias** de un backend en FastAPI que responden a peticiones HTTP.
- Un **load balancer** (HAProxy) que distribuye las peticiones entre los backends usando el algoritmo **round-robin**.
- Un **plan de pruebas de carga** con Apache JMeter para simular usuarios concurrentes.

El objetivo es observar cómo HAProxy distribuye el tráfico entre las diferentes instancias del backend de forma equitativa.

---

## 🏗 Arquitectura

```
                           ┌─────────────────────┐
                           │     👤 Usuario       │
                           │   (Navegador Web)    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │   HAProxy (puerto 80)│
                           │   Load Balancer      │
                           └──────────┬──────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                  │
             /api/* │          /api/* │           /api/* │      default
                    ▼                 ▼                  ▼         │
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
          │  Backend 1   │ │  Backend 2   │ │  Backend 3   │     │
          │  FastAPI     │ │  FastAPI     │ │  FastAPI     │     │
          │  :8000       │ │  :8000       │ │  :8000       │     │
          └──────────────┘ └──────────────┘ └──────────────┘     │
                                                                  ▼
                                                        ┌──────────────┐
                                                        │  Frontend    │
                                                        │  React+Vite  │
                                                        │  :3000       │
                                                        └──────────────┘
```

### Flujo de Peticiones

1. El **usuario** accede a `http://localhost` (puerto 80).
2. **HAProxy** recibe la petición y evalúa las reglas ACL:
   - Si la ruta empieza con `/api/` → la envía a uno de los 3 backends (round-robin).
   - Si la ruta es `/stats` → muestra el dashboard de estadísticas de HAProxy.
   - Cualquier otra ruta → la envía al frontend.
3. El **frontend** hace peticiones a `/api/hello` que el proxy de Vite redirige a HAProxy.
4. **HAProxy** balancea esas peticiones entre `backend1`, `backend2` y `backend3`.

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Docker** | 24+ | Contenedorización de servicios |
| **Docker Compose** | v2 | Orquestación de múltiples contenedores |
| **HAProxy** | 2.8 | Load balancer / reverse proxy |
| **Python** | 3.11 | Runtime del backend |
| **FastAPI** | latest | Framework web del backend (API REST) |
| **Uvicorn** | latest | Servidor ASGI para FastAPI |
| **Node.js** | 18 | Runtime del frontend |
| **React** | 18.2 | Biblioteca UI del frontend |
| **Vite** | 4.5 | Build tool y dev server del frontend |
| **Apache JMeter** | 5.6+ | Pruebas de carga y rendimiento |

---

## 📁 Estructura del Proyecto

```
docker-haproxy-main/
├── backend/
│   ├── Dockerfile            # Imagen Docker del backend
│   └── main.py               # API FastAPI con endpoint /api/hello
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Componente principal de React
│   │   └── main.jsx          # Punto de entrada de React
│   ├── Dockerfile            # Imagen Docker del frontend
│   ├── index.html            # HTML base de la app
│   ├── package.json          # Dependencias npm
│   └── vite.config.js        # Configuración de Vite + proxy
├── haproxy/
│   └── haproxy.cfg           # Configuración del load balancer
├── jmeter/
│   └── haproxy_load_test.jmx # Plan de pruebas de carga
├── docs/
│   └── architecture.png      # Diagrama de arquitectura
├── docker-compose.yml        # Orquestación de todos los servicios
├── INSTRUCCIONES.md          # Guía paso a paso para ejecutar el proyecto
└── README.md                 # Este archivo
```

---

## 📄 Descripción de Archivos

### `backend/Dockerfile`

Construye la imagen del backend:

- **Imagen base**: `python:3.11-slim` (imagen ligera de Python).
- **Instala**: `fastapi` y `uvicorn` con pip.
- **Copia**: `main.py` al contenedor.
- **Expone**: puerto `8000`.
- **Ejecuta**: `uvicorn main:app --host 0.0.0.0 --port 8000`.

### `backend/main.py`

API REST con FastAPI que expone un único endpoint:

- **`GET /api/hello`**: Retorna un JSON con:
  - `message`: Saludo que incluye el nombre de la instancia.
  - `instance`: Nombre de la instancia (ej: `backend1`, `backend2`, `backend3`).
  - `hostname`: Hostname del contenedor Docker.
- **CORS**: Habilitado para todas las origenes (desarrollo).

### `frontend/Dockerfile`

Construye la imagen del frontend:

- **Imagen base**: `node:18-alpine` (imagen ligera de Node.js).
- **Instala**: dependencias npm (`react`, `react-dom`, `vite`, `@vitejs/plugin-react`).
- **Copia**: todo el código fuente.
- **Expone**: puerto `3000`.
- **Ejecuta**: `npm run dev` (servidor de desarrollo de Vite).

### `frontend/src/App.jsx`

Componente React que:

- Hace un `fetch` a `/api/hello` al montarse.
- Muestra el mensaje recibido del backend.
- Tiene un diseño visual con gradiente azul y glassmorphism.

### `frontend/vite.config.js`

Configuración de Vite:

- **Plugin**: `@vitejs/plugin-react` para compilar JSX.
- **Puerto**: `3000`.
- **Host**: `true` (accesible desde fuera del contenedor).
- **Proxy**: `/api` → `http://haproxy` (redirige peticiones API al load balancer dentro de la red Docker).

### `haproxy/haproxy.cfg`

Configuración de HAProxy:

- **Frontend `http-in`**: Escucha en puerto 80, evalúa ACLs.
- **Backend `api_servers`**: Pool de 3 servidores con `balance roundrobin` y health checks.
- **Backend `front_servers`**: Servidor frontend único.
- **Backend `stats_backend`**: Dashboard de estadísticas en `/stats`.

### `docker-compose.yml`

Orquestación de 5 servicios:

- `frontend`: Build desde `./frontend`, puerto 3000.
- `backend1`, `backend2`, `backend3`: Build desde `./backend`, cada uno con variable de entorno `INSTANCE_NAME` diferente.
- `haproxy`: Imagen `haproxy:2.8`, puerto 80, monta `haproxy.cfg`.
- Todos conectados a la red `app-net` (bridge).

### `jmeter/haproxy_load_test.jmx`

Plan de pruebas de Apache JMeter:

- **20 usuarios concurrentes** con ramp-up de 10 segundos.
- **50 iteraciones** por usuario = **1000 peticiones** totales.
- **Target**: `GET http://localhost:80/api/hello`.
- **Listeners**: View Results Tree, Summary Report, Response Time Graph.

---

## 🐳 Servicios Docker

| Servicio | Imagen | Puerto Interno | Puerto Expuesto | Descripción |
|----------|--------|---------------|-----------------|-------------|
| `frontend` | Build local | 3000 | 3000 | App React + Vite |
| `backend1` | Build local | 8000 | — | Instancia 1 de FastAPI |
| `backend2` | Build local | 8000 | — | Instancia 2 de FastAPI |
| `backend3` | Build local | 8000 | — | Instancia 3 de FastAPI |
| `haproxy` | `haproxy:2.8` | 80 | 80 | Load balancer |

> **Nota**: Los backends no exponen puertos al host; solo son accesibles a través de HAProxy dentro de la red Docker `app-net`.

---

## ⚖ Configuración de HAProxy

### Algoritmo de Balanceo: Round-Robin

El algoritmo **round-robin** distribuye las peticiones de forma secuencial y equitativa entre los servidores disponibles:

```
Petición 1 → backend1
Petición 2 → backend2
Petición 3 → backend3
Petición 4 → backend1  (vuelve a empezar)
Petición 5 → backend2
...
```

### Reglas de Enrutamiento (ACL)

| Ruta | Destino | Descripción |
|------|---------|-------------|
| `/api/*` | `api_servers` (pool de 3 backends) | Peticiones a la API |
| `/stats` | `stats_backend` | Dashboard de HAProxy |
| Todo lo demás | `front_servers` (frontend) | Aplicación React |

### Health Checks

HAProxy verifica periódicamente que cada backend esté activo enviando `GET /api/hello`. Si un backend no responde, se excluye temporalmente del pool.

---

## ⚛ Frontend React

El frontend es una Single Page Application (SPA) construida con React 18 y Vite:

- Al cargar la página, hace una petición `GET /api/hello`.
- Vite actúa como proxy: redirige `/api` hacia `http://haproxy` dentro de la red Docker.
- Muestra el mensaje recibido, que incluye el nombre de la instancia backend que respondió.

---

## 🐍 Backend FastAPI

Cada instancia del backend es una API REST mínima con FastAPI:

- **Endpoint**: `GET /api/hello`
- **Respuesta de ejemplo**:

```json
{
  "message": "Hello from FastAPI! (served by backend2)",
  "instance": "backend2",
  "hostname": "a1b2c3d4e5f6"
}
```

La variable de entorno `INSTANCE_NAME` permite identificar qué contenedor procesó la petición.

---

## 📊 Pruebas de Carga con JMeter

### Configuración del Test Plan

| Parámetro | Valor |
|-----------|-------|
| Usuarios concurrentes (threads) | 20 |
| Loops por usuario | 50 |
| Total de peticiones | 1000 |
| Ramp-up (tiempo para crear todos los threads) | 10 segundos |
| Target URL | `http://localhost:80/api/hello` |
| Método HTTP | GET |

### Listeners Incluidos

1. **View Results Tree**: Muestra cada petición individual con su request/response completo. Útil para debugging.
2. **Summary Report**: Tabla resumen con métricas agregadas (avg, min, max, throughput, % error).
3. **Response Time Graph**: Gráfica visual del tiempo de respuesta a lo largo del tiempo.

### Métricas Clave a Observar

- **Throughput** (peticiones/segundo): Indica la capacidad del sistema.
- **Average Response Time**: Tiempo promedio de respuesta en milisegundos.
- **Error %**: Porcentaje de peticiones fallidas (debería ser 0%).
- **Min/Max Response Time**: Variabilidad en tiempos de respuesta.

---

## 🌐 URLs de Acceso

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación React |
| API via HAProxy | http://localhost/api/hello | Endpoint balanceado |
| HAProxy Stats | http://localhost/stats | Dashboard de monitoreo |

---

## ✅ Verificación del Balanceo

Para verificar que HAProxy distribuye el tráfico correctamente, ejecuta múltiples peticiones al endpoint de la API:

```bash
for i in {1..9}; do curl -s http://localhost/api/hello | python -m json.tool; done
```

Deberías ver las respuestas alternando entre `backend1`, `backend2` y `backend3`:

```
Petición 1: "instance": "backend1"
Petición 2: "instance": "backend2"
Petición 3: "instance": "backend3"
Petición 4: "instance": "backend1"
...
```

También puedes verificarlo visualmente en el **dashboard de HAProxy** (`http://localhost/stats`), donde verás estadísticas en tiempo real de cada backend.

---

## 👥 Autores

- Proyecto desarrollado como taller práctico de balanceo de carga con Docker.

---
