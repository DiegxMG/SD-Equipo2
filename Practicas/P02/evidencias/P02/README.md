# Práctica 2: Acuerdo de nivel de servicio (SLA) y diseño de SLOs del proyecto

* **Proyecto:** Acortador de URLs con estadísticas de uso (Equipo 2 — Grupo 7CV1)
* **Proveedor principal:** Google Cloud Platform (GCP)
* **Integrantes:**
  * Diego Mendieta González (`DiegxMG`)
  * Juan Antonio Mirón Xochipa
---

## 1. Anatomía de los SLAs reales (Tabla 1)

| Integrante | Servicio y URL (fecha) | Compromiso por configuración | Definición de inactividad | Exclusiones | Créditos | Reclamación | Min/mes permitidos |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Diego Mendieta (`DiegxMG`) | **GKE** ([cloud.google.com/kubernetes-engine/sla](https://cloud.google.com/kubernetes-engine/sla), 26/11/2026) | **Clúster Zonal (control plane):** ≥ 99.5%<br>**Clúster Regional / Autopilot (control plane):** ≥ 99.95%<br>**Autopilot Pods en múltiples zonas:** ≥ 99.9%<br>*(Querétaro `northamerica-south1` incluido en el estándar global sin penalización)* | Pérdida de conectividad del plano de control hacia todos los Pods aplicables (Autopilot) o pérdida de acceso externo/API de Kubernetes durante **≥ 5 minutos consecutivos**. | 1. Mantenimiento programado (*Scheduled Downtime*).<br>2. Fallas en instancias VM/red subyacentes (cubiertas por Compute SLA).<br>3. Falla de nodos o Pods de usuario.<br>4. Versiones fuera de canales *Stable*/*Regular*. | **Autopilot Pods / Control Plane:**<br>99.0%–<99.9% (o <99.95%): **10%**<br>95.0%–<99.0%: **25%**<br><95.0%: **50%** (tope).<br>*Con 99.0% sobre $100 USD:* **$10 USD (10%)**. | Notificar a soporte técnico en **≤ 30 días** con *server log files* (fechas y horas). Crédito a facturas futuras. **Sí es remedio único**. | **Zonal:** 216 min<br>**Regional/Autopilot CP:** 21.6 min<br>**Autopilot Pods:** 43.2 min |
| Diego Mendieta (`DiegxMG`) | **Cloud Load Balancing** ([cloud.google.com/compute/sla](https://cloud.google.com/compute/sla), 26/11/2026) | **Nivel Premium:** ≥ 99.99%<br>**Nivel Estándar:** ≥ 99.9%<br>*(Querétaro `northamerica-south1` incluido en Nivel Premium sin penalización)* | Pérdida de conectividad externa en las IPs de reenvío hacia backends saludables por falla de Google durante **≥ 1 minuto consecutivo**. | 1. Funciones en vista previa (*Preview*).<br>2. Funciones excluidas en documentación.<br>3. Fuerza mayor (fuera del control de Google).<br>4. Software/hardware del cliente o terceros, abusos o límites de cuotas. | **Nivel Premium:**<br>99.00%–<99.99%: **10%**<br>95.00%–<99.00%: **25%**<br><95.00%: **100%**.<br>*Con 99.0% sobre $100 USD:* **$10 USD (10%)**. | Notificar a soporte técnico en **≤ 60 días** con logs de fechas y horas de corte. Crédito a facturas futuras. **Sí es remedio único**. | **Premium:** 4.32 min<br>**Estándar:** 43.2 min |
| Juan Antonio Mirón | **Cloud SQL** ([cloud.google.com/sql/sla](https://cloud.google.com/sql/sla), `[FECHA]`) | `[PENDIENTE JUAN: instancia única sin SLA vs. HA multizona]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` |
| Juan Antonio Mirón | **Cloud Storage** ([cloud.google.com/storage/sla](https://cloud.google.com/storage/sla), `[FECHA]`) | `[PENDIENTE JUAN: regional vs. multirregional]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` |

---

## 2. Cadena de dependencias y disponibilidad compuesta (Tabla 2)

Diagrama de arquitectura de dependencias: [docs/arquitectura/cadena_dependencias.png](../../docs/arquitectura/cadena_dependencias.png)

| Componente | SLA individual | SLA redundante | En serie o paralelo | Costo extra de la redundancia (USD/mes) |
| :--- | :--- | :--- | :--- | :--- |
| **DNS (Cloud DNS)** | 100.00% | 100.00% | Serie | $0 (incluido) |
| **Balanceador (Cloud Load Balancing)** | 99.90% (Estándar) | 99.99% (Premium) | Serie | ~$0–$5 (diferencia de tráfico Premium Tier) |
| **Cómputo (GKE Autopilot)** | 99.50% (Zonal CP) | 99.90% (Pods multizona) | Paralelo (réplicas entre zonas) | Incluido en Autopilot ($30–$60 base) |
| **Base de datos (Cloud SQL)** | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN: HA]` | Paralelo (primaria + standby) | ~$10–$25 extra (duplica instancia mínima) |
| **Objetos (Cloud Storage)** | `[PENDIENTE JUAN]` | `[PENDIENTE JUAN]` | Fuera de ruta crítica | ~$0–$2 |
| **Compuesto sin / con redundancia** | `[CALCULAR CON JUAN]` | `[CALCULAR CON JUAN]` | — | — |
| **Minutos al mes sin / con redundancia** | `[CALCULAR CON JUAN]` | `[CALCULAR CON JUAN]` | — | — |

---

## 3. SLOs y presupuesto de error del proyecto (Tabla 3)

Especificación completa y políticas de presupuesto de error en: [docs/slo.md](../../docs/slo.md) (enlazado desde [docs/fase2.md](../../docs/fase2.md)).

| SLO | SLI (buenos ÷ válidos) | Punto de medición | Ventana | Objetivo | Presupuesto (min) | Alertas (50% / 100%) | Herramienta |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Disponibilidad** | Peticiones HTTP válidas sin error `5xx` ÷ peticiones válidas totales (excluye health checks y `4xx`) | Cloud Load Balancing | 30 d | ≥ 99.5% | 216 min | 108 min / 216 min | Cloud Monitoring + UptimeRobot |
| **Latencia p95** | Redirecciones válidas (`301`/`302`) respondidas en ≤ 150 ms ÷ redirecciones válidas totales | Cloud Load Balancing | 30 d | ≥ 95.0% | 2,160 min-eq | 1,080 min-eq / 2,160 min-eq | Cloud Monitoring + Managed Prometheus |
| **De dominio (Frescura)** | Eventos de clic visibles en panel en ≤ 2 s ÷ clics publicados en Pub/Sub | Suscripción de Pub/Sub | 30 d | ≥ 99.0% | 432 min-eq | 216 min-eq / 432 min-eq | Cloud Monitoring (Pub/Sub metrics) |

---

## 4. Cláusula de SLA del equipo

**Acuerdo de Nivel de Servicio (SLA) — Servicio de Redirección de URLs:**
El equipo garantiza una disponibilidad mensual del endpoint público de redirección de al menos **99.0%** por mes calendario. Se considera **indisponibilidad** cualquier periodo de 1 minuto consecutivo o más en el que el balanceador de carga responda con errores de servidor (`5xx`) o ausencia total de respuesta ante peticiones válidas de redirección. **Exclusiones:** este acuerdo no aplica durante ventanas de mantenimiento programado notificadas con 48 horas de anticipación (máximo 2 horas semanales), fallas originadas por el cliente (errores `4xx` o enlaces malformados), eventos de fuerza mayor ni interrupciones atribuibles a la infraestructura base de Google Cloud fuera de nuestro control. **Créditos de servicio:** si la disponibilidad mensual es de 95.0% a menos de 99.0%, el cliente recibirá un crédito del **10%** sobre su cuota mensual; si es menor a 95.0%, recibirá un crédito del **25%**. **Reclamación:** el cliente deberá solicitar el crédito dentro de los 30 días naturales posteriores al cierre del mes adjuntando marcas de tiempo y registros de las peticiones fallidas.

Nuestro SLO interno (99.5%) es más estricto que este SLA contractual (99.0%) para contar con un margen de seguridad de 216 minutos mensuales que nos permita detectar degradaciones y congelar despliegues antes de incumplir la promesa económica con el cliente.

---

## 5. Preguntas de análisis

1. **Falla fuera del SLA del proveedor:** `[PENDIENTE: redactar ejemplo de imagen defectuosa / CrashLoopBackOff en GKE Autopilot, cae del lado del cliente según exclusión #3 del SLA de GKE y lo detecta nuestro SLI de disponibilidad 5xx en el balanceador]`.
2. **Caída de 8 horas vs. factura mensual:** `[PENDIENTE: 480 min / 43,200 = 1.11% indisponibilidad → 98.89% disponibilidad → crédito de 10% sobre $60–$120 USD = $6–$12 USD]`.
3. **99.99% y residencia de datos en México:** Aunque Google Cloud ya equiparó los compromisos de Querétaro (`northamerica-south1`) con el estándar global en Compute Engine (99.99% balanceo) y GKE (99.9% Autopilot Pods), solo existe **una región** de Google Cloud en México. Para alcanzar una disponibilidad compuesta de 99.99% eliminando el riesgo regional sin salir de territorio mexicano se requeriría una arquitectura híbrida o multi-nube activo-activo dentro del país (por ejemplo, combinando GCP Querétaro con AWS `mx-central-1` en Querétaro), lo que duplicaría el costo base de infraestructura (~$120–$240 USD/mes) más sincronización de datos entre nubes.
4. **Por qué el SLO no puede superar al compuesto:** `[PENDIENTE: completar tras calcular Tabla 2 con Juan]`.
5. **Incidente público (Cloudflare, 18 de noviembre de 2025):** `[PENDIENTE: analizar impacto en minutos contra nuestro presupuesto de 216 min]`.
6. **Consumo del 80% del presupuesto en la primera semana:** Si en la primera semana se consume el 80% del presupuesto (172.8 minutos de los 216 disponibles), el viernes **se cancela/congela el despliegue de la función nueva** aunque aún quede un 20% restante. De acuerdo con nuestra política de presupuesto de error, consumir más del 50% activa alerta preventiva y desplegar código nuevo con solo 43.2 minutos de margen para los 23 días restantes del mes pondría en riesgo crítico el SLO de 99.5% y el SLA externo de 99.0%; el equipo debe enfocarse en estabilizar el servicio antes de liberar cambios.

---

## 6. Lista de verificación, conclusiones y referencias

### Lista de verificación
* [x] Capturas oficiales de SLA de GKE y Cloud Load Balancing guardadas en `evidencias/P02/` (`DiegxMG`).
* [ ] Capturas oficiales de SLA de Cloud SQL y Cloud Storage guardadas en `evidencias/P02/` (Juan).
* [x] Especificación de SLOs completa en `docs/slo.md` y enlazada en `docs/fase2.md`.
* [x] Bitácora registrada en `bitacora/2026-09-15.md`.
* [ ] Diagrama de cadena de dependencias guardado en `docs/arquitectura/`.
* [ ] Commits individuales de todos los integrantes en el historial de Git.

### Conclusiones
`[PENDIENTE DE CIERRE EN EQUIPO]`

### Referencias
* Google Cloud. (2026). *Google Kubernetes Engine Service Level Agreement (SLA)*. https://cloud.google.com/kubernetes-engine/sla (Consultado el 26/11/2026).
* Google Cloud. (2026). *Compute Engine Service Level Agreement (SLA)*. https://cloud.google.com/compute/sla (Consultado el 26/11/2026).
* Beyer, B., Jones, C., Petoff, J., & Murphy, N. (2016). *Site Reliability Engineering*. O'Reilly Media.

### Uso de IA
Se utilizó asistencia de IA generativa (Gemini) para estructurar las tablas en formato Markdown, verificar las fórmulas de disponibilidad compuesta y presupuesto de error, y redactar el borrador inicial de `docs/slo.md` y la cláusula de SLA. Todos los porcentajes, exclusiones y plazos contractuales fueron verificados directamente en las páginas oficiales de Google Cloud por los integrantes del equipo.

### Tabla de contribución
| Integrante | Contribución |
| :--- | :--- |
| Diego Mendieta (`DiegxMG`) | Análisis de SLA de GKE y Cloud Load Balancing, redacción de `docs/slo.md`, `docs/fase2.md`, bitácora y estructura del reporte. |
| Juan Antonio Mirón | Análisis de SLA de Cloud SQL y Cloud Storage, cálculo de disponibilidad compuesta y diagrama de arquitectura. |