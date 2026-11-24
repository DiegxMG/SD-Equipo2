# Práctica 1 · Modelos de servicio y despliegue: consolas, calculadoras de costos y alertas de presupuesto

- **Sistemas Distribuidos · Grupo 7CV1 · ESCOM-IPN · Semestre 27/1**
- **Profesor:** Rodrigo Ojeda Santillán
- **Equipo:** Equipo 2
- **Proveedores usados:** Google Cloud y Amazon Web Services (AWS)
- **Sesiones:** A (1 de septiembre de 2026) · B (8 de septiembre de 2026)
---

## 0. Integrantes

| # | Nombre | Boleta | Usuario GitHub | Correo donde llegan las alertas |
|---|--------|--------|----------------|---------------------------------|
| 1 | Diego Mendieta Gonzalez | [COMPLETAR boleta] | DiegxMG | dmendieta2005@gmail.com |
| 2 | Mirón Xochipa Juan Antonio | 2020630680 | Johnny06spider | [COMPLETAR correo] |

---

## 1. Cuentas del equipo y reconocimiento de la consola (Actividad A1)

### Tabla 1. Cuentas del equipo

| Integrante | Proveedor | Identificador de cuenta | Unidad de facturación | Región México | Créditos y vencimiento | Correo de alertas |
|---|---|---|---|---|---|---|
| Diego Mendieta Gonzalez | Google Cloud | ID del proyecto: `project-6800c28f-c7a6-492a-84e` (nombre: My First Project · número: 403204069542) | Cuenta de facturación + proyecto | Sí · `northamerica-south1` (Querétaro) | Crédito de bienvenida de MXN 5,344.19 (equivalente a los 300 USD de la prueba; la cuenta factura en pesos) · vence el 4 de enero de 2027 (41 días restantes al 24 nov 2026) | dmendieta2005@gmail.com |
| Diego Mendieta Gonzalez | AWS | ID de cuenta (12 dígitos): [COMPLETAR] | Cuenta de AWS | Sí · `mx-central-1` (Querétaro) | [COMPLETAR] USD · vence [COMPLETAR fecha] (plan gratuito: 6 meses o hasta agotar el crédito) | dmendieta2005@gmail.com |
| Mirón Xochipa Juan Antonio | Google Cloud | ID del proyecto: [COMPLETAR] | Cuenta de facturación + proyecto | Sí · `northamerica-south1` (Querétaro) | [COMPLETAR] | [COMPLETAR] |
| Mirón Xochipa Juan Antonio | AWS | ID de cuenta (12 dígitos): [COMPLETAR] | Cuenta de AWS | Sí · `mx-central-1` (Querétaro) | [COMPLETAR] | [COMPLETAR] |

### Evidencias A1 — Diego Mendieta Gonzalez (DiegxMG)

**Google Cloud**

| Captura | Archivo |
|---|---|
| Panel de inicio con ID del proyecto | ![](/P01/evidencias/P01/P01_A1_gcp_DiegxMG_1.png) |
| Lista de regiones con México visible | ![](/P01/evidencias/P01/P01_A1_gcp_DiegxMG_2.png) |
| Facturación: gasto del mes 0.00 y créditos con vencimiento | ![](/P01/evidencias/P01/P01_A1_gcp_DiegxMG_3.png) |

**AWS**

| Captura | Archivo |
|---|---|
| Consola con el ID de cuenta visible y selector de región | ![](/P01/evidencias/P01/P01_A1_aws_DiegxMG_1.png) |
| Lista de regiones con Mexico (Central) visible | ![](/P01/evidencias/P01/P01_A1_aws_DiegxMG_2.png) |
| Billing: gasto del mes 0.00 y créditos con vencimiento | ![](/P01/evidencias/P01/P01_A1_aws_DiegxMG_3.png) |

### Evidencias A1 — Mirón Xochipa Juan Antonio (Johnny06spider)

| Captura | Google Cloud | AWS |
|---|---|---|
| Panel de inicio con ID de cuenta/proyecto | ![](/P01/evidencias/P01/P01_A1_gcp_Johnny06spider_1.png) | ![](/P01/evidencias/P01/P01_A1_aws_Johnny06spider_1.png) |
| Lista de regiones con México | ![](/P01/evidencias/P01/P01_A1_gcp_Johnny06spider_2.png) | ![](/P01/evidencias/P01/P01_A1_aws_Johnny06spider_2.png) |
| Gasto 0.00 y créditos con vencimiento | ![](/P01/evidencias/P01/P01_A1_gcp_Johnny06spider_3.png) | ![](/P01/evidencias/P01/P01_A1_aws_Johnny06spider_3.png) |

---

## 2. Alertas de presupuesto (Actividad A2) — individuales

**Regla común:** presupuesto mensual de 5 USD llamado `P1-<usuario>-<proveedor>` (en AWS, además, el de gasto cero), mínimo tres umbrales y 100 % del pronóstico, con notificación por correo.

### 2.1 Diego Mendieta Gonzalez — Google Cloud

| Campo | Valor configurado |
|---|---|
| Nombre | `P1-DiegxMG-gcp` |
| Periodo | Mensual |
| Alcance | Esta cuenta de facturación (todos los proyectos) · todos los servicios |
| Créditos | Se **desmarcó** «Promotions and others» (para medir el consumo real contra los 300 USD) |
| Monto | 5.00 (importe especificado; la cuenta de facturación está en pesos mexicanos, MXN) <!-- La práctica pide 5 USD. Con el tipo de cambio de tu crédito (5,344.19 MXN = 300 USD) equivalen a ≈ 89 MXN. Si editas el presupuesto a 89 MXN, repite las capturas A2_1 y A2_4 y actualiza esta fila y la de umbrales. --> |
| Umbrales | 50 % ($2.50) · 90 % ($4.50) · 100 % ($5.00) del gasto real · 100 % ($5.00) del pronóstico (previsto) |
| Notificación | Alertas por correo a administradores de facturación y usuarios (dmendieta2005@gmail.com); alertas a propietarios del proyecto desactivadas |
| Créditos | La lista del presupuesto indica «No se usaron créditos» |
| ID de la cuenta/proyecto visible | `project-6800c28f-c7a6-492a-84e` (en la tarjeta «Project info» de la captura A1_1) |

| Fecha | Captura |
|---|---|
| 24 nov 2026 (presupuesto creado, `$0.00/$5.00`) | ![](/P01/evidencias/P01/P01_A2_gcp_DiegxMG_1.png) |
| [COMPLETAR fecha: día siguiente] (presupuesto vivo, 0.00) | ![](/P01/evidencias/P01/P01_A2_gcp_DiegxMG_2.png) |
| [COMPLETAR fecha: día de entrega] (estado OK) | ![](/P01/evidencias/P01/P01_A2_gcp_DiegxMG_3.png) |
| Detalle del presupuesto (umbrales y destinatario) | ![](/P01/evidencias/P01/P01_A2_gcp_DiegxMG_4.png) |

### 2.2 Diego Mendieta Gonzalez — AWS

| Campo | Presupuesto 1 | Presupuesto 2 |
|---|---|---|
| Nombre | `P1-DiegxMG-aws-cero` | `P1-DiegxMG-aws` |
| Tipo | Zero spend budget (plantilla simplificada) | Monthly cost budget (plantilla simplificada o Customize) |
| Monto | Avisa al superar 0.01 USD | 5 USD |
| Umbrales | Gasto mayor a 0.01 USD | 85 % y 100 % del gasto real + 100 % del pronóstico (plantilla simplificada) <!-- si usaste Customize: 50/80/100 % --> |
| Destinatario | dmendieta2005@gmail.com | dmendieta2005@gmail.com |

Además: en Billing preferences → Alert preferences se activó **AWS Free Tier alerts**: [COMPLETAR sí/no].

| Fecha | Captura |
|---|---|
| 1 sep 2026 (lista de Budgets con ambos) | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_1.png) |
| 2 sep 2026 (`Current: $0.00`) | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_2.png) |
| 8 sep 2026 (estado OK) | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_3.png) |
| Detalle del presupuesto de gasto cero | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_4.png) |
| Detalle del presupuesto mensual | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_5.png) |
| Free Tier alerts activadas | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_6.png) |

Correos recibidos del proveedor (si los hubo): [COMPLETAR o «ninguno»]

### 2.3 Mirón Xochipa Juan Antonio (Johnny06spider) — Google Cloud y AWS

| Campo | Google Cloud | AWS |
|---|---|---|
| Nombre(s) del presupuesto | `P1-Johnny06spider-gcp` | `P1-Johnny06spider-aws-cero` y `P1-Johnny06spider-aws` |
| Monto y periodo | 5 USD · mensual | 5 USD · mensual (más gasto cero) |
| Umbrales | [COMPLETAR] | [COMPLETAR] |
| Destinatario | [COMPLETAR] | [COMPLETAR] |

| Fecha | Google Cloud | AWS |
|---|---|---|
| 1 sep 2026 | ![](/P01/evidencias/P01/P01_A2_gcp_Johnny06spider_1.png) | ![](/P01/evidencias/P01/P01_A2_aws_Johnny06spider_1.png) |
| 2 sep 2026 | ![](/P01/evidencias/P01/P01_A2_gcp_Johnny06spider_2.png) | ![](/P01/evidencias/P01/P01_A2_aws_Johnny06spider_2.png) |
| 8 sep 2026 | ![](/P01/evidencias/P01/P01_A2_gcp_Johnny06spider_3.png) | ![](/P01/evidencias/P01/P01_A2_aws_Johnny06spider_3.png) |
| Detalle | ![](/P01/evidencias/P01/P01_A2_gcp_Johnny06spider_4.png) | ![](/P01/evidencias/P01/P01_A2_aws_Johnny06spider_4.png) |

---

## 3. Estimación de costos (Actividad A3) — equipo

**Arquitectura de referencia (igual para todos los equipos):**
1 VM Linux 2 vCPU / 4 GB, 730 h/mes, 30 GB SSD · 1 BD relacional gestionada mínima (1–2 vCPU, 2–4 GB) con 20 GB · 50 GB de objetos con 100 000 solicitudes/mes · 1 balanceador de carga de aplicación · 100 GB de salida a internet/mes.

Comparación: región de México contra la región de EE. UU. más barata (`us-central1` en Google Cloud, `us-east-1` en AWS).

### Tabla 2a. Google Cloud

| Recurso | Unidad de cobro | Cantidad | Subtotal México (USD/mes) | Subtotal EE. UU. (USD/mes) | ¿Capa gratuita? |
|---|---|---|---|---|---|
| VM 2 vCPU / 4 GB + 30 GB SSD (Compute Engine, `e2-medium`: 2 vCPU / 4 GB) | vCPU-hora + GB-hora de RAM + GB-mes de disco | 730 h · 30 GB | 49.49 | 45.40 | No: el Always Free solo cubre 1 e2-micro en regiones de EE. UU.; se paga con el crédito de prueba |
| BD relacional gestionada (Cloud SQL para MySQL) | Instancia-hora + GB-mes | 730 h · 20 GB | 12.03 | 11.07 | No (se paga con el crédito de prueba) |
| Almacenamiento de objetos 50 GB (Cloud Storage, Standard) | GB-mes + solicitudes (clase A y B) | 50 GB · 100 000 | 1.53 | 1.12 | Parcial solo en EE. UU.: 5 GB-mes gratis en regiones de EE. UU.; en México no |
| Balanceador de carga de aplicación (Cloud Load Balancing, 1 regla de reenvío regional) | Hora de regla de reenvío + GB de datos | 730 h | 20.74 | 19.05 | No |
| Salida a internet 100 GB | GB de salida | 100 GB | Incluido en la fila del balanceador | Incluido en la fila del balanceador | No (la calculadora lo estimó como 100 GiB de datos del balanceador, sin línea separada) |
| **Total mensual** | | | **83.80** | **76.64** | |
| **Total anual** | | | **1,005.65** | **919.69** | |
| **Diferencia México vs. EE. UU. (%)** | | | **+9.34 %** (+7.16 USD/mes) | | |

Capturas: ![](/P01/evidencias/P01/P01_A3_gcp_DiegxMG_1.png) ![](/P01/evidencias/P01/P01_A3_gcp_DiegxMG_2.png)
Exportaciones: `evidencias/P01/costos/` → `gcp_mexico.csv`, `gcp_eeuu.csv`

### Tabla 2b. AWS

| Recurso | Unidad de cobro | Cantidad | Subtotal México (USD/mes) | Subtotal EE. UU. (USD/mes) | ¿Capa gratuita? |
|---|---|---|---|---|---|
| VM 2 vCPU / 4 GB + 30 GB SSD (EC2 `t3.medium`: 2 vCPU / 4 GB + EBS gp3) | Segundo/hora de instancia + GB-mes de disco | 730 h · 30 GB | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| BD relacional gestionada (RDS, p. ej. PostgreSQL `db.t3.small`: 2 vCPU / 2 GB) | Instancia-hora + GB-mes | 730 h · 20 GB | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| Almacenamiento de objetos 50 GB (S3 Standard) | GB-mes + solicitudes | 50 GB · 100 000 | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| Balanceador de carga de aplicación (ALB) | Hora de balanceador + LCU | 730 h | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| Salida a internet 100 GB (Data Transfer Out) | GB de salida | 100 GB | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| **Total mensual** | | | **[COMPLETAR]** | **[COMPLETAR]** | |
| **Total anual** | | | **[COMPLETAR]** | **[COMPLETAR]** | |
| **Diferencia México vs. EE. UU. (%)** | | | **[COMPLETAR]** | | |

Capturas: ![](/P01/evidencias/P01/P01_A3_aws_DiegxMG_1.png) ![](/P01/evidencias/P01/P01_A3_aws_DiegxMG_2.png)
Exportaciones: `evidencias/P01/costos/` → `aws_mexico.csv`, `aws_eeuu.csv`

> Cálculo de la diferencia: `(Total México − Total EE. UU.) / Total EE. UU. × 100`.

### Estimación preliminar del proyecto (punto de partida de la Tarea 14 y la Fase 1)

**Proveedor candidato:** [COMPLETAR Google Cloud o AWS]
**Idea del proyecto en una línea:** [COMPLETAR]
Captura: ![](/P01/evidencias/P01/P01_A3_proyecto_DiegxMG_1.png)

| Recurso del proyecto | Servicio | Unidad de cobro | Cantidad estimada | USD/mes | ¿Capa gratuita? |
|---|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| **Total mensual** | | | | **[COMPLETAR]** | |

---

## 4. Modelos de servicio en la consola (Actividad B1) — equipo

Se revisaron 7 servicios por proveedor **sin crear ningún recurso** (asistente cancelado o página pública de precios).

### Tabla 3. Modelos de servicio identificados


**Google Cloud**

| Servicio | Modelo | Administra el proveedor | Administras tú | Unidad de cobro | Capa gratuita | En México | Captura |
|---|---|---|---|---|---|---|---|
| Compute Engine | IaaS | Hardware, virtualización, red física | SO, runtime, aplicación, datos | Segundo de vCPU/RAM + GB-mes de disco + GB de salida | [COMPLETAR] | [COMPLETAR] | [1](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_1.png) |
| App Engine / Cloud Run | PaaS | SO, runtime, parches, escalado | Aplicación y datos | vCPU-segundo / instancia-hora | [COMPLETAR] | [COMPLETAR] | [2](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_2.png) |
| Cloud Run functions | FaaS | Ejecución, escalado, disponibilidad | Código de la función | Invocación + GB-segundo | [COMPLETAR] | [COMPLETAR] | [3](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_3.png) |
| Google Kubernetes Engine (GKE) | Contenedores gestionados | Plano de control del orquestador | Imágenes y manifiestos | Nodos por hora + cuota de clúster | [COMPLETAR] | [COMPLETAR] | [4](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_4.png) |
| Cloud SQL | BD gestionada | Instalación, parches, respaldos, réplicas | Esquema y datos | Instancia-hora + GB-mes | [COMPLETAR] | [COMPLETAR] | [5](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_5.png) |
| Cloud Storage | Almacenamiento de objetos | Durabilidad y replicación | Objetos y permisos | GB-mes + solicitudes + GB de salida | [COMPLETAR] | [COMPLETAR] | [6](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_6.png) |
| Vertex AI | IA gestionada | Modelo, GPU, inferencia | Prompts y datos | Por millón de tokens / hora de nodo | [COMPLETAR] | [COMPLETAR] | [7](/P01/evidencias/P01/P01_B1_gcp_DiegxMG_7.png) |

**AWS**

| Servicio | Modelo | Administra el proveedor | Administras tú | Unidad de cobro | Capa gratuita | En México | Captura |
|---|---|---|---|---|---|---|---|
| EC2 | IaaS | Hardware, virtualización, red física | SO, runtime, aplicación, datos | Segundo/hora de instancia + GB-mes de disco + GB de salida | [COMPLETAR] | [COMPLETAR] | [1](/P01/evidencias/P01/P01_B1_aws_DiegxMG_1.png) |
| Elastic Beanstalk / App Runner | PaaS | SO, runtime, parches, escalado | Aplicación y datos | Instancia-hora / vCPU-segundo | [COMPLETAR] | [COMPLETAR] | [2](/P01/evidencias/P01/P01_B1_aws_DiegxMG_2.png) |
| Lambda | FaaS | Ejecución, escalado, disponibilidad | Código de la función | Invocación + GB-segundo | [COMPLETAR] | [COMPLETAR] | [3](/P01/evidencias/P01/P01_B1_aws_DiegxMG_3.png) |
| EKS / ECS | Contenedores gestionados | Plano de control del orquestador | Imágenes y manifiestos | Nodos por hora; plano de control de EKS: 0.10 USD/h | [COMPLETAR] | [COMPLETAR] | [4](/P01/evidencias/P01/P01_B1_aws_DiegxMG_4.png) |
| RDS / DynamoDB | BD gestionada | Instalación, parches, respaldos, réplicas | Esquema y datos | Instancia-hora + GB-mes + IOPS | [COMPLETAR] | [COMPLETAR] | [5](/P01/evidencias/P01/P01_B1_aws_DiegxMG_5.png) |
| S3 | Almacenamiento de objetos | Durabilidad y replicación | Objetos y permisos | GB-mes + solicitudes + GB de salida | [COMPLETAR] | [COMPLETAR] | [6](/P01/evidencias/P01/P01_B1_aws_DiegxMG_6.png) |
| Bedrock | IA gestionada | Modelo, GPU, inferencia | Prompts y datos | Por millón de tokens | [COMPLETAR] | [COMPLETAR] | [7](/P01/evidencias/P01/P01_B1_aws_DiegxMG_7.png) |

### SaaS (captura de precios)

- **SaaS elegido:** GitHub (plan de pago por usuario) <!-- cámbialo si capturaste otro SaaS -->
- **Unidad de cobro:** usuario por mes — [COMPLETAR precio visto en la captura]
- **Captura:** ![](/P01/evidencias/P01/P01_B1_saas_DiegxMG_1.png)
- **¿Por qué no aparece en la consola de una nube de infraestructura?** Porque en SaaS el proveedor administra toda la pila y el cliente solo usa y configura la aplicación; las consolas de nube de infraestructura exponen servicios que el cliente combina y administra parcialmente (IaaS, PaaS, FaaS), no productos finales de licencia por usuario.

---

## 5. Las cinco características esenciales del NIST vistas en la consola (Actividad B2)

*(NIST SP 800-145, Mell y Grance, 2011)*

| Característica | Captura | Explicación (2 líneas) |
|---|---|---|
| Autoservicio bajo demanda | ![](/P01/evidencias/P01/P01_B2_gcp_DiegxMG_1.png) | El asistente «Crear una instancia» de Compute Engine permite elegir nombre, región, zona, tipo de máquina y sistema operativo, y lanzar una VM sin intervención de nadie del proveedor; la consola incluso estima el costo mensual. Se canceló antes de crear para no generar recursos. |
| Amplio acceso a la red | ![](/P01/evidencias/P01/P01_B2_gcp_DiegxMG_2.png) | La misma cuenta (dmendieta2005@gmail.com) y el mismo proyecto se manejan desde otro cliente distinto a la consola gráfica: Cloud Shell, una terminal en el navegador. El comando `gcloud config list` devuelve la cuenta y el proyecto activos, por lo que se accede por red desde cualquier dispositivo con navegador. |
| Agrupación de recursos | ![](/P01/evidencias/P01/P01_B2_gcp_DiegxMG_3.png) | La región `northamerica-south1` (México) ofrece tres zonas de disponibilidad (`-a`, `-b` y `-c`). Los recursos se asignan desde un conjunto de infraestructura compartido por muchos clientes, sin saber en qué servidor físico corren. |
| Elasticidad rápida | ![](/P01/evidencias/P01/P01_B2_gcp_DiegxMG_4.png) | El selector de series y tamaños (por ejemplo `e2-micro`, `e2-small` y `e2-medium`, con distintas cantidades de vCPU y memoria) permite escalar los recursos de una VM con un cambio de configuración, sin comprar hardware. |
| Servicio medido | ![](/P01/evidencias/P01/P01_B2_gcp_DiegxMG_5.png) | El informe de facturación agrupa el costo por producto en el mes actual, con gasto de MXN 0.00 y el saldo restante de los créditos de prueba gratuita. Todo uso se mide y se cobra, y el presupuesto `P1-DiegxMG-gcp` vigila ese gasto. |

---

## 6. Inventario, cero gasto y limpieza (Actividad B3)

### Diego Mendieta Gonzalez

| Verificación | Google Cloud | AWS |
|---|---|---|
| Inventario sin cómputo, red ni almacenamiento encendidos | ![](/P01/evidencias/P01/P01_B3_gcp_DiegxMG_1.png) | ![](/P01/evidencias/P01/P01_B3_aws_DiegxMG_1.png) |
| Gasto del mes 0.00 y saldo de créditos (con fecha visible) | ![](/P01/evidencias/P01/P01_B3_gcp_DiegxMG_2.png) | ![](/P01/evidencias/P01/P01_B3_aws_DiegxMG_2.png) |
| Listado de presupuestos en estado OK (8 sep) | ![](/P01/evidencias/P01/P01_A2_gcp_DiegxMG_3.png) | ![](/P01/evidencias/P01/P01_A2_aws_DiegxMG_3.png) |
| Recursos que existían y justificación | Ninguno: el panel de Compute Engine no muestra instancias | [COMPLETAR o «ninguno»] |

### Mirón Xochipa Juan Antonio (Johnny06spider)

| Verificación | Google Cloud | AWS |
|---|---|---|
| Inventario sin cómputo, red ni almacenamiento encendidos | ![](/P01/evidencias/P01/P01_B3_gcp_Johnny06spider_1.png) | ![](/P01/evidencias/P01/P01_B3_aws_Johnny06spider_1.png) |
| Gasto del mes 0.00 y saldo de créditos | ![](/P01/evidencias/P01/P01_B3_gcp_Johnny06spider_2.png) | ![](/P01/evidencias/P01/P01_B3_aws_Johnny06spider_2.png) |
| Listado de presupuestos en estado OK (8 sep) | ![](/P01/evidencias/P01/P01_A2_gcp_Johnny06spider_3.png) | ![](/P01/evidencias/P01/P01_A2_aws_Johnny06spider_3.png) |
| Recursos que existían y justificación | [COMPLETAR o «ninguno»] | [COMPLETAR o «ninguno»] |

---

## 7. Preguntas de análisis

<!-- Cada respuesta debe usar las cifras y capturas del equipo. Los párrafos son una base: sustituye los [COMPLETAR] y adapta lo que no coincida con lo que vieron. Cualquiera de los dos debe poder explicarlos en sesión. -->

**1. ¿Cuenta compartida del equipo o una por integrante?**
Google Cloud factura a nivel de cuenta de facturación y proyecto, y AWS a nivel de cuenta (con un ID de 12 dígitos), así que la decisión cambia quién paga y quién puede gastar. Una cuenta compartida concentra el crédito y facilita ver el gasto total del proyecto, pero implica compartir acceso: si una credencial se filtra, todo el equipo queda expuesto, y las cuentas del curso son personales y no se comparten. En AWS esto se agrava porque el usuario root controla la facturación y puede cerrar la cuenta. Una cuenta por integrante aísla el riesgo y el gasto, y cada quien conserva su propio crédito y su propia alerta, pero el despliegue se fragmenta. Para nuestro equipo de dos, la opción que más nos convence es una cuenta personal por integrante para practicar (cada quien con su crédito, su MFA y sus alertas) y, para el proyecto final, un proyecto o cuenta del equipo con usuarios de permisos mínimos para cada uno, también con presupuesto y alertas. Así el error de uno no gasta el crédito del otro ni expone sus credenciales.

**2. Región de México contra EE. UU.**
Con nuestras estimaciones, la región de México resultó 9.34 % más cara en Google Cloud (total de 83.80 vs. 76.64 USD/mes, es decir, 7.16 USD más al mes y unos 86 USD más al año) y [COMPLETAR]% más cara en AWS (total [COMPLETAR] vs. [COMPLETAR] USD/mes). En Google Cloud la mayor diferencia en dólares estuvo en la VM con su disco (49.49 vs. 45.40 USD, 4.09 USD de diferencia); en porcentaje fue el almacenamiento de objetos (1.53 vs. 1.12 USD, 36.6 %), aunque con montos pequeños. En AWS la mayor diferencia estuvo en [COMPLETAR recurso: VM / BD / balanceador / salida], con [COMPLETAR] USD. Elegiríamos México de todos modos cuando importe la latencia para usuarios en el país, cuando los datos personales deban quedar bajo jurisdicción mexicana o convenga facilitar el cumplimiento de la LFPDPPP, o cuando la residencia de datos sea un requisito del cliente. Para un proyecto escolar sin esas restricciones, la región de EE. UU. [COMPLETAR conclusión].

**3. ¿Qué sigue cobrando si apago la máquina virtual?**
En la arquitectura de referencia siguen cobrando: el disco SSD de 30 GB (GB-mes), las instantáneas si existen (GB-mes), la dirección IPv4 pública (en AWS 0.005 USD por hora, unos 3.6 USD al mes), el balanceador de carga (por hora, haya o no tráfico), la base de datos gestionada (instancia-hora, aunque nadie la consulte), el almacenamiento de objetos de 50 GB (GB-mes más solicitudes) y el tráfico de salida a internet (por GB). Apagar la VM solo detiene el cargo del cómputo; los demás recursos deben eliminarse o detenerse por separado. <!-- opcional: añade los montos que vieron en su calculadora -->

**4. Modelo de servicio para el cómputo del proyecto**
Para [COMPLETAR idea del proyecto] conviene [COMPLETAR: IaaS / PaaS / contenedores / serverless] porque [COMPLETAR: p. ej., permite escalar a cero y pagar solo por ejecución; evita administrar el SO]. Eso implica una unidad de cobro de [COMPLETAR: vCPU-segundo + GB-segundo + solicitudes (Cloud Run), invocación + GB-segundo (Lambda), nodo-hora (GKE/EKS), segundo de VM (Compute Engine/EC2)]. En la consola vimos que [COMPLETAR: qué mostraba la pantalla de precios, si el servicio tenía capa gratuita y si estaba disponible en México].

**5. Mecanismo para detener el gasto automáticamente**
Las alertas avisan pero no detienen el gasto. En AWS, AWS Budgets permite configurar **acciones de presupuesto** que se ejecutan cuando se cruza un umbral: aplicar una política IAM o de control de servicios que restrinja crear recursos, o detener instancias EC2 y RDS específicas. Lo configuraríamos así: (1) crear la acción dentro del presupuesto mensual, asociada al umbral del 100 %; (2) darle un rol con permisos solo para detener los recursos indicados; (3) elegir ejecución automática o con aprobación manual; (4) probarla antes de depender de ella. En Google Cloud, el presupuesto puede publicar sus notificaciones en un tema de Pub/Sub, y una Cloud Function suscrita puede desvincular la cuenta de facturación del proyecto o apagar instancias. En una cuenta individual de AWS (que no es cuenta de administración de una organización) no se pueden aplicar SCP, pero sí una política IAM de denegación o apuntar a instancias EC2 o RDS específicas, y las acciones de IAM y SCP se reinician al inicio de cada periodo del presupuesto, mientras que las de apagar instancias no (AWS, 2026a; AWS, 2020). Ninguno de estos mecanismos sustituye revisar la consola: solo limitan el daño.

**6. Dependencia de capas gratuitas**
Los dos casos muestran que una capa gratuita es una promoción que el proveedor puede reducir o cerrar: Oracle redujo el ARM de Always Free a la mitad en junio de 2026 sin anuncio público, y AWS cambió en julio de 2025 a un plan gratuito que se cierra solo a los seis meses; ese plan es el que usamos en AWS, así que nuestro crédito tiene fecha de vencimiento. En Google Cloud la prueba dura 90 días: el crédito de bienvenida (MXN 5,344.19, equivalente a 300 USD) de la cuenta de Diego finaliza el 4 de enero de 2027, y se acaba antes si se consume todo el saldo. Nuestro equipo haría lo siguiente: (1) repartir el proyecto entre dos nubes para no depender de un solo crédito; (2) mantener la infraestructura como código y los despliegues en contenedores dentro del repositorio, para poder recrearlos en otra cuenta; (3) anotar en un calendario las fechas de vencimiento de cada crédito y planear con antelación qué se migra o se apaga; (4) mantener alertas activas en todas las cuentas; y (5) decidir antes de la demo final si conviene pasar una de las cuentas a plan de pago con presupuesto y límites estrictos.

---

## 8. Lista de verificación de seguridad y costos

- [ ] Las cuentas de ambos integrantes tienen presupuesto de 5 USD con al menos tres umbrales + pronóstico (en AWS, además, el de gasto cero)
- [ ] El presupuesto sigue vivo y en estado OK el 8 de septiembre
- [ ] Hay capturas del 1, 2 y 8 de septiembre por cuenta
- [ ] Cuatro estimaciones de la arquitectura de referencia exportadas
- [ ] Estimación preliminar del proyecto incluida
- [ ] Tabla 3 con los 14 servicios + SaaS
- [ ] Cinco capturas NIST con explicación
- [ ] Inventario en cero (o recursos justificados) y gasto 0.00 en cada cuenta
- [ ] MFA activado en root y en el usuario IAM de AWS; no se activó IAM Identity Center ni AWS Organizations
- [ ] No se crearon llaves de acceso de AWS
- [ ] Ninguna captura muestra llaves, tokens, contraseñas ni datos de tarjeta
- [ ] No hay archivos `.env`, `.pem` ni JSON de credenciales en el repositorio (ni el CSV de credenciales de IAM)
- [ ] La verificación automática de GitHub Actions está en verde
- [ ] Ambos integrantes tienen al menos un commit con sus evidencias
- [ ] Bitácoras `2026-09-01.md` y `2026-09-08.md` creadas el mismo día de cada sesión

---

## 9. Conclusiones

Esta práctica mostró que en la nube todo uso se mide y se cobra, por lo que un descuido (una VM olvidada, una IP pública sin usar, una llave filtrada) puede convertirse en una factura real. Por eso el primer paso con cualquier cuenta es configurar presupuestos con alertas y estimar los costos antes de desplegar, y revisar la consola para confirmar que no quedó nada encendido. También comprobamos que una alerta solo avisa y que detener el gasto requiere acciones adicionales (acciones de presupuesto en AWS, Pub/Sub y funciones en Google Cloud) y disciplina de limpieza.

Al comparar Google Cloud y AWS vimos que las unidades de cobro, la organización de la cuenta y la disponibilidad de servicios en la región de México difieren entre proveedores, y que la región de México suele costar más que la de Estados Unidos. [COMPLETAR: una frase con su conclusión sobre qué proveedor conviene para el proyecto, apoyada en una cifra de sus estimaciones.] A partir de ahora adoptaremos como hábito de FinOps crear el presupuesto y las alertas antes de lanzar cualquier recurso y revisar el gasto al terminar cada sesión.

---

## 10. Referencias

AWS. (2025, 15 de julio). *AWS Free Tier now offers $200 in credits and 6-month free plan*. https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/
AWS. (2026). *Using a budget template (simplified)*. AWS Cost Management User Guide. https://docs.aws.amazon.com/cost-management/latest/userguide/budget-templates.html
AWS. (2024). *New – AWS Public IPv4 Address Charge*. https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/
AWS. (2026a). *Configuring budget actions*. AWS Cost Management User Guide. https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html
AWS. (2020, 15 de octubre). *Announcing AWS Budgets Actions*. https://aws.amazon.com/about-aws/whats-new/2020/10/announcing-aws-budgets-actions/
AWS. (2026). *AWS Pricing Calculator*. https://calculator.aws/
Google Cloud. (2026). *Free Trial and Free Tier*. https://cloud.google.com/free
Google Cloud. (2026). *Create, edit, or delete budgets and budget alerts*. https://cloud.google.com/billing/docs/how-to/budgets
Google Cloud. (2026). *Pricing Calculator*. https://cloud.google.com/products/calculator
Wiggers, S. (2026, 3 de julio). *Oracle Quietly Halves Free Tier Ampere A1 Compute Limits with No Public Announcement*. InfoQ. https://www.infoq.com/news/2026/07/oracle-cloud-free-tier-limits/
Mell, P. y Grance, T. (2011). *The NIST Definition of Cloud Computing* (SP 800-145). NIST. https://doi.org/10.6028/NIST.SP.800-145
FinOps Foundation. (2026). *FinOps Framework*. https://www.finops.org/framework/
[COMPLETAR: añadan cualquier otra fuente que usen en las respuestas]

---

## 11. Uso de IA

| Herramienta | Para qué se usó |
|---|---|
| Claude (Anthropic) | Plantilla del README|

---

## 12. Tabla de contribución

| Integrante | Contribución |
|---|---|
| Diego Mendieta Gonzalez (DiegxMG) | Registro y configuración de sus cuentas de Google Cloud y AWS; presupuestos y alertas de ambas; estimaciones de costo (A3); identificación de servicios (B1) y evidencias NIST (B2); inventario y cero gasto (B3); redacción del reporte. |
| Mirón Xochipa Juan Antonio (Johnny06spider) | [COMPLETAR: p. ej., alertas de presupuesto en sus cuentas, capturas A1/A2/B3, estimaciones] |