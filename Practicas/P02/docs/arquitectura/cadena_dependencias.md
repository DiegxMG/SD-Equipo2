graph TD
    subgraph Usuarios
        V[Visitante<br/>Abre enlace corto]
        C[Creador<br/>Consulta estadísticas]
    end

    subgraph Ruta Crítica Síncrona - En Serie
        DNS[Cloud DNS<br/>SLA: 100%]
        LB[Cloud Load Balancing<br/>SLA: 99.99% Premium]
        subgraph Cómputo Paralelo
            GKE[GKE Autopilot Pods Multizona<br/>SLA: 99.9%<br/>Caché en memoria TTL]
        end
        subgraph Base de Datos Paralelo HA
            SQL[(Cloud SQL PostgreSQL<br/>Instancia única vs. HA Multizona)]
        end
    end

    subgraph Rutas No Críticas - Asíncronas y Estáticas
        GCS[Cloud Storage<br/>Frontend Panel Web]
        PS[Pub/Sub<br/>Cola de clics]
        ANA[Microservicio Analítica<br/>GKE Autopilot]
        FS[(Firestore<br/>Historial de clics)]
    end

    V -->|HTTPS| DNS
    C -->|HTTPS| DNS
    DNS --> LB
    LB -->|Ruta crítica redirección| GKE
    GKE -->|Cache miss| SQL
    GKE -.->|No bloquea redirección| PS
    PS -.-> ANA
    ANA -.-> FS
    LB -.->|Archivos estáticos| GCS

    style DNS fill:#e1f5fe,stroke:#0288d1
    style LB fill:#e1f5fe,stroke:#0288d1
    style GKE fill:#e8f5e9,stroke:#388e3c
    style SQL fill:#fff3e0,stroke:#f57c00
    style GCS fill:#f3e5f5,stroke:#7b1fa2,stroke-dasharray: 5 5
    style PS fill:#f3e5f5,stroke:#7b1fa2,stroke-dasharray: 5 5
    style ANA fill:#f3e5f5,stroke:#7b1fa2,stroke-dasharray: 5 5
    style FS fill:#f3e5f5,stroke:#7b1fa2,stroke-dasharray: 5 5