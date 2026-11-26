# Objetivos de Nivel de Servicio (SLOs) — Acortador de URLs

## SLO 1: Disponibilidad de redirección
* **Servicio:** `redireccion-service` (endpoint público detrás de Cloud Load Balancing)
* **SLI (definición):** Proporción de peticiones HTTP válidas respondidas sin error `5xx`.
* **SLI (implementación):** `(Total_Requests - 5xx_Responses) / Total_Requests` medido en Cloud Load Balancing (`loadbalancing.googleapis.com/https/request_count` filtrando por clase de respuesta != 500). Excluye health checks y errores `4xx` del cliente.
* **Ventana:** 30 días móviles
* **Objetivo (SLO):** ≥ 99.5%
* **Presupuesto de error:** $0.5\% \times 43,200\text{ min} = 216\text{ min}$ por ventana de 30 días.
* **Alertas:** Aviso (Warning) al consumir 50% del presupuesto (108 min); Crítica (Critical) al consumir 100% (216 min).
* **Política:** Al agotarse el 100% del presupuesto, se congelan los despliegues de funciones nuevas y el equipo trabaja exclusivamente en tareas de confiabilidad (rollbacks, pruebas de carga, ajuste de HPA y alertas) hasta recuperar al menos el 25% del presupuesto (54 min). Decide el responsable del SLO.
* **Verificación externa:** Monitor sintético cada 5 min sobre `GET /health` y un enlace de prueba.
* **Responsable:** Diego Mendieta (`DiegxMG`)
* **Revisión:** Cada cierre parcial

---

## SLO 2: Latencia de redirección (p95)
* **Servicio:** `redireccion-service`
* **SLI (definición):** Proporción de redirecciones válidas (`301`/`302`) respondidas en $\le 150\text{ ms}$ medidas en el balanceador.
* **SLI (implementación):** Percentil 95 de `loadbalancing.googleapis.com/https/total_latencies` $\le 150\text{ ms}$ en Cloud Monitoring (excluyendo `4xx` y health checks).
* **Ventana:** 30 días móviles
* **Objetivo (SLO):** ≥ 95.0% de las peticiones válidas bajo el umbral de 150 ms.
* **Presupuesto de error:** 5.0% de peticiones lentas permitidas (equivalente a $2,160\text{ min-equivalentes}$ en 30 días).
* **Alertas:** Aviso al consumir 50% del presupuesto de error de latencia; Crítica al 100%.
* **Política:** Misma política de congelamiento de despliegues que el SLO 1; se prioriza optimización de caché en memoria y réplicas de Pods.
* **Verificación externa:** Pruebas de carga periódicas y sondeo sintético.
* **Responsable:** Diego Mendieta (`DiegxMG`)
* **Revisión:** Cada cierre parcial

---

## SLO 3: Frescura de métricas de clics (De dominio)
* **Servicio:** `analitica-service` (pipeline `Pub/Sub` → `Analítica` → `Firestore`)
* **SLI (definición):** Proporción de eventos de clic publicados en Pub/Sub que se procesan y quedan visibles en el panel web en $\le 2\text{ s}$.
* **SLI (implementación):** Métrica `pubsub.googleapis.com/subscription/oldest_unacked_message_age` $\le 2\text{ s}$ en Cloud Monitoring dividida entre el total de mensajes publicados.
* **Ventana:** 30 días móviles
* **Objetivo (SLO):** ≥ 99.0%
* **Presupuesto de error:** $1.0\% \times 43,200\text{ min} = 432\text{ min-equivalentes}$ por ventana de 30 días.
* **Alertas:** Aviso al consumir 50% (216 min-eq); Crítica al 100% (432 min-eq).
* **Política:** Si se agota el presupuesto, se pausan cambios en el esquema de analítica y se escalan consumidores en GKE Autopilot hasta recuperar el 25% del presupuesto.
* **Responsable:** Juan Antonio Mirón
* **Revisión:** Cada cierre parcial