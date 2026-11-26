// Prueba de carga con k6 sobre la redirección.
//   k6 run loadtest/redirect.js                                   (local, puerto 8080)
//   k6 run -e BASE_URL=http://IP_DEL_INGRESS loadtest/redirect.js  (Google Cloud)
// Los umbrales son los SLOs de la Fase 2: p95 < 50 ms y menos de 0.1% de errores.
import http from 'k6/http';
import { check } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '1m', target: 200 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<50'],
    http_req_failed: ['rate<0.001'],
  },
};

export function setup() {
  const res = http.post(
    `${BASE}/api/links`,
    JSON.stringify({ url: 'https://example.com/prueba-de-carga' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  check(res, { 'enlace creado': (r) => r.status === 201 });
  return { code: res.json('code') };
}

export default function (data) {
  const res = http.get(`${BASE}/${data.code}`, { redirects: 0 });
  check(res, { 'responde 302': (r) => r.status === 302 });
}
