# Acortador de URLs con estadísticas de uso

Proyecto de Sistemas Distribuidos (ESCOM-IPN, 7CV1). Tres microservicios en Python que se ejecutan
**en tu computadora con un solo comando** y se despliegan **sin cambiar código** en Google Cloud (GKE Autopilot).

| Microservicio | Qué hace | Tecnología |
|---|---|---|
| `services/redirect` | Resuelve el código corto y responde 302/301. Publica el clic en una cola **después** de responder. | FastAPI, PostgreSQL, Pub/Sub |
| `services/links` | API REST (CRUD) con Swagger y panel web. | FastAPI, PostgreSQL |
| `services/analytics` | Consume los clics de la cola, los guarda y calcula estadísticas. | FastAPI, Pub/Sub, Firestore |

```
Visitante ─▶ nginx / Ingress ─▶ redirect ─▶ PostgreSQL (enlaces)
                                    │
                                    └─▶ Pub/Sub ─▶ analytics ─▶ Firestore (clics)
Creador ───▶ nginx / Ingress ─▶ links (API + panel)   y   analytics (/api/stats)
```

En local, Pub/Sub y Firestore se reemplazan por **emuladores oficiales de Google**, así el código es idéntico en tu laptop y en la nube.

## 1. Qué debes instalar

| Programa | Para qué | ¿Obligatorio? |
|---|---|---|
| **Docker Desktop** (incluye Docker Compose) | Corre todo el proyecto. No necesitas instalar Python, PostgreSQL ni nada más. | Sí |
| **Git** | Clonar y subir el código a GitHub. | Sí |
| **Visual Studio Code** (extensiones *Docker* y *Python*) | Editor. | Recomendado |
| **Python 3.12** | Solo para correr las pruebas unitarias fuera de Docker. | Opcional |
| **k6** | Pruebas de carga (SLO de latencia y autoescalado). | Opcional, lo usarán después |
| Cuenta de **Google Cloud** | Despliegue. Usa **Cloud Shell** (terminal en el navegador): no instales `gcloud` ni `kubectl`. | Para desplegar |

Notas para Windows: Docker Desktop pide activar **WSL 2** durante la instalación; si no arranca, revisa que la
virtualización esté habilitada en la BIOS. Conviene tener 8 GB de RAM o más (los emuladores de Google pesan).

## 2. Arrancar el proyecto

```bash
docker compose up --build
```

La primera vez tarda varios minutos (descarga imágenes, entre ellas la de los emuladores, de más de 1 GB).
Cuando veas que `analytics` escribe "Escuchando eventos", abre:

- Panel web: http://localhost:8080/app/
- Swagger (API de enlaces): http://localhost:8080/api/docs

Para detener todo: `Ctrl+C` y luego `docker compose down` (agrega `-v` para borrar también los datos).

### Probarlo sin escribir código

1. Abre el panel, pega una URL larga y pulsa **Crear enlace**.
2. Abre el enlace corto (por ejemplo `http://localhost:8080/aB3dE9x`) en otra pestaña varias veces.
3. En el panel pulsa **Estadísticas**: los clics aparecen en unos segundos.

Con `curl` (en Windows PowerShell usa `curl.exe` o mejor el Swagger):

```bash
curl -X POST http://localhost:8080/api/links -H "Content-Type: application/json" \
     -d '{"url":"https://www.ipn.mx","alias":"ipn"}'
curl -i http://localhost:8080/ipn            # 302 hacia la URL original
curl http://localhost:8080/api/stats/ipn     # estadísticas
```

## 3. Estructura

```
acortador-urls/
├── docker-compose.yml        entorno local completo
├── nginx/nginx.conf          puerta de entrada local (equivale al Ingress)
├── db/init.sql               tabla de enlaces
├── services/
│   ├── links/                gestión de enlaces + panel web (app/static/index.html)
│   ├── redirect/             redirección
│   └── analytics/            analítica
├── k8s/                      manifiestos de Kubernetes (Deployments, HPA, Ingress, monitoreo)
├── loadtest/redirect.js      prueba de carga con k6 (umbrales = SLOs de la Fase 2)
└── docs/DESPLIEGUE_GCP.md    guía paso a paso para Google Cloud
```

Cada servicio tiene su `Dockerfile`, `requirements.txt`, carpeta `app/` y `tests/`.

## 4. Pruebas

Unitarias (no necesitan Docker ni instalar dependencias, solo Python):

```bash
cd services/links     && python -m unittest discover -s tests
cd ../redirect        && python -m unittest discover -s tests
cd ../analytics       && python -m unittest discover -s tests
```

Carga (con el proyecto levantado): `k6 run loadtest/redirect.js`.
Ejecutada en tu laptop con Docker Desktop, la latencia no representa a la nube; los SLOs se miden en GKE.

## 5. Decisiones de diseño (útiles para la exposición)

- **La redirección no espera a la analítica.** El evento se publica en Pub/Sub *después* de enviar la respuesta; si la cola falla, el visitante no lo nota.
- **Caché en memoria (30 s)** en la redirección para cumplir el SLO de 50 ms sin consultar la base en cada clic.
- **302 por defecto.** Los navegadores guardan los 301 y las visitas repetidas ya no llegan al servicio; por eso el 301 es opcional (`permanent`).
- **Privacidad:** no se guarda la IP, solo un hash corto.
- **Métricas:** cada servicio expone `/metrics` (Prometheus) con latencias y errores, base de los SLOs.

## 6. Límites conocidos (a propósito, para las fases siguientes)

- No hay autenticación: cualquiera con acceso al panel ve y borra todos los enlaces (tema de seguridad / Fase 5).
- `/metrics` es alcanzable desde Internet a través del Ingress; en el hardening se restringe.
- Las ediciones y borrados pueden tardar hasta 30 s en reflejarse en la redirección por la caché.
- Las estadísticas leen hasta 20 000 clics por enlace; para volúmenes mayores se necesitan contadores agregados (tema de **partición de datos**).
- `redirect` y `links` comparten la tabla `links` de PostgreSQL (aceptable aquí; en una versión mayor la redirección tendría su propia réplica de lectura).
- HTTP solamente: para HTTPS en Google Cloud se necesita un dominio y un certificado administrado.

## 7. Desplegar en Google Cloud

Sigue [`docs/DESPLIEGUE_GCP.md`](docs/DESPLIEGUE_GCP.md).
