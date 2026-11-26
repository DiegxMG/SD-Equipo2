# Despliegue en Google Cloud (GKE Autopilot)

> Esta guía no se ha ejecutado contra una cuenta real. Si algún comando falla, copia el error completo
> (y el comando) y se corrige. Todos los comandos se ejecutan en **Cloud Shell**
> (https://console.cloud.google.com, ícono `>_` arriba a la derecha). No instales nada en tu computadora.

**Cuidado con el gasto.** Un clúster, Cloud SQL y el balanceador cobran por hora aunque nadie los use.
Antes de empezar crea una **alerta de presupuesto** (Facturación → Presupuestos y alertas) al 50 %, 90 % y 100 %,
y al terminar cada sesión sigue la sección *Apagar y limpiar*.

## 0. Cuenta y proyecto

1. Entra a https://console.cloud.google.com con una cuenta de Google y activa la prueba gratuita (pide una tarjeta, no cobra mientras haya créditos).
2. Crea un proyecto nuevo (por ejemplo `acortador-urls`) y anota su **ID**.
3. En Cloud Shell, descarga el código (sube antes este proyecto a tu repositorio de GitHub):

```bash
git clone https://github.com/AntonyCanseco12/acortadorURLS_SD.git
cd acortadorURLS_SD
```

4. Define las variables (cámbialas y **vuelve a ejecutarlas** cada vez que Cloud Shell se reinicie):

```bash
export PROJECT_ID=tu-id-de-proyecto
export REGION=us-central1
export TAG=v1
export DB_PASSWORD=CambiaEstaClave123      # solo letras y números
gcloud config set project $PROJECT_ID
```

## 1. Activar las APIs

```bash
gcloud services enable container.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com \
  sqladmin.googleapis.com servicenetworking.googleapis.com compute.googleapis.com \
  pubsub.googleapis.com firestore.googleapis.com monitoring.googleapis.com
```

## 2. Red (VPC) con nodos privados

```bash
gcloud compute networks create acortador-vpc --subnet-mode=custom

gcloud compute networks subnets create acortador-subnet \
  --network=acortador-vpc --region=$REGION --range=10.10.0.0/20 \
  --secondary-range=pods=10.20.0.0/16,services=10.30.0.0/20 \
  --enable-private-ip-google-access

# Salida a Internet para los nodos privados
gcloud compute routers create acortador-router --network=acortador-vpc --region=$REGION
gcloud compute routers nats create acortador-nat --router=acortador-router --region=$REGION \
  --auto-allocate-nat-external-ips --nat-all-subnet-ip-ranges

# Acceso privado de Cloud SQL a esta red
gcloud compute addresses create google-managed-services-acortador \
  --global --purpose=VPC_PEERING --prefix-length=16 --network=acortador-vpc
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com \
  --ranges=google-managed-services-acortador --network=acortador-vpc
```

## 3. Construir y publicar las imágenes

```bash
gcloud artifacts repositories create acortador --repository-format=docker --location=$REGION

# Permisos que suelen faltar en proyectos nuevos (Cloud Build compila y los nodos descargan)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
COMPUTE_SA=$PROJECT_NUMBER-compute@developer.gserviceaccount.com
gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$COMPUTE_SA --role=roles/cloudbuild.builds.builder
gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$COMPUTE_SA --role=roles/artifactregistry.reader

for s in links redirect analytics; do
  gcloud builds submit services/$s --tag $REGION-docker.pkg.dev/$PROJECT_ID/acortador/$s:$TAG
done
```

## 4. Datos y mensajería

```bash
# PostgreSQL (IP privada, instancia mínima). Tarda unos 10 minutos.
gcloud sql instances create acortador-db --database-version=POSTGRES_16 --edition=ENTERPRISE \
  --tier=db-f1-micro --region=$REGION --network=acortador-vpc --no-assign-ip
gcloud sql databases create acortador --instance=acortador-db
gcloud sql users create acortador --instance=acortador-db --password=$DB_PASSWORD
export CLOUDSQL_CONNECTION=$(gcloud sql instances describe acortador-db --format='value(connectionName)')

# Cola de eventos de clic
gcloud pubsub topics create click-events
gcloud pubsub subscriptions create click-events-analytics --topic=click-events --ack-deadline=30

# Firestore (modo nativo)
gcloud firestore databases create --location=$REGION --type=firestore-native
```

La tabla `links` la crea automáticamente el servicio `links` al arrancar.

## 5. Permisos mínimos por servicio (IAM + Workload Identity)

```bash
SA() { echo acortador-$1@$PROJECT_ID.iam.gserviceaccount.com; }
for n in links redirect analytics; do gcloud iam service-accounts create acortador-$n; done

role() { gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$(SA $1) --role=$2 --condition=None >/dev/null; }
role links     roles/cloudsql.client
role redirect  roles/cloudsql.client
role redirect  roles/pubsub.publisher
role analytics roles/pubsub.subscriber
role analytics roles/datastore.user

# Cada cuenta de Kubernetes puede "ser" su cuenta de Google (sin llaves JSON)
for n in links redirect analytics; do
  gcloud iam service-accounts add-iam-policy-binding $(SA $n) \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:$PROJECT_ID.svc.id.goog[acortador/$n-sa]"
done
```

## 6. Clúster GKE Autopilot e IP pública

```bash
gcloud container clusters create-auto acortador --region=$REGION \
  --network=acortador-vpc --subnetwork=acortador-subnet \
  --cluster-secondary-range-name=pods --services-secondary-range-name=services \
  --enable-private-nodes
gcloud container clusters get-credentials acortador --region=$REGION

# IP fija para el balanceador
gcloud compute addresses create acortador-ip --global
export INGRESS_IP=$(gcloud compute addresses describe acortador-ip --global --format='value(address)')
echo $INGRESS_IP
```

## 7. Desplegar

```bash
kubectl apply -f k8s/00-namespace.yaml
kubectl -n acortador create secret generic db-credentials \
  --from-literal=DATABASE_URL="postgresql+psycopg2://acortador:$DB_PASSWORD@127.0.0.1:5432/acortador"

for f in k8s/*.yaml; do
  envsubst '${PROJECT_ID} ${REGION} ${TAG} ${CLOUDSQL_CONNECTION} ${INGRESS_IP}' < $f | kubectl apply -f -
done

kubectl -n acortador get pods -w          # espera a que todos estén 'Running' y 'READY' (Ctrl+C para salir)
kubectl -n acortador get ingress          # el balanceador tarda 5-10 minutos en quedar listo
```

Si un Pod queda en `ImagePullBackOff` por la imagen `cloud-sql-proxy:2.13.0`, busca la versión más reciente en
https://github.com/GoogleCloudPlatform/cloud-sql-proxy/releases y cámbiala en `k8s/20-links.yaml` y `k8s/21-redirect.yaml`.
Para ver errores de un Pod: `kubectl -n acortador logs deploy/redirect -c app` y `kubectl -n acortador describe pod <nombre>`.

## 8. Probar

```bash
curl http://$INGRESS_IP/api/docs -I
echo "Panel: http://$INGRESS_IP/app/"
```

Abre el panel, crea un enlace y visítalo varias veces.

## 9. Demostraciones para las fases siguientes

**Autoescalado (HPA).** Instala k6 en Cloud Shell o ejecútalo desde tu computadora:

```bash
k6 run -e BASE_URL=http://$INGRESS_IP loadtest/redirect.js     # en una pestaña
kubectl -n acortador get hpa -w                                # en otra: verás subir las réplicas
```

**Failover.** Con la carga corriendo, elimina Pods de la redirección y observa que el servicio sigue respondiendo:

```bash
kubectl -n acortador delete pod -l app=redirect --wait=false
kubectl -n acortador get pods -l app=redirect -w
```

**Métricas para los SLOs.** En la consola: *Monitoring → Explorador de métricas → PromQL*, por ejemplo:

```
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job="redirect"}[5m])))
```

Para Grafana, conéctalo a Managed Service for Prometheus (guía oficial de Google: "Query using Grafana").
Las alertas y el *uptime check* de disponibilidad se crean desde *Monitoring → Alertas* y *Comprobaciones de tiempo de actividad*.

## 10. Apagar y limpiar

Entre sesiones de trabajo (ahorra créditos, conserva los datos):

```bash
kubectl -n acortador scale deploy --all --replicas=0      # con 0 réplicas el autoescalado queda en pausa
gcloud sql instances patch acortador-db --activation-policy=NEVER     # detiene la base (para reanudar: ALWAYS)
```

Para reanudar: `ALWAYS` en la base y, con `kubectl scale`, vuelve a poner 1 réplica en `links` y `analytics` y 2 en `redirect`.
El balanceador (unos USD 18-25 al mes) sigue cobrando mientras exista el Ingress.

Al terminar el proyecto, para dejar de pagar todo:

```bash
kubectl -n acortador delete ingress acortador
gcloud container clusters delete acortador --region=$REGION --quiet
gcloud sql instances delete acortador-db --quiet
gcloud compute addresses delete acortador-ip --global --quiet
gcloud compute routers nats delete acortador-nat --router=acortador-router --region=$REGION --quiet
gcloud compute routers delete acortador-router --region=$REGION --quiet
# o, más simple, borra todo el proyecto:
# gcloud projects delete $PROJECT_ID
```
