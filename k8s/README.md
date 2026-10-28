# k8s/ · Rol 5 coordina

Manifiestos de Kubernetes. Todos llevan `namespace: virtual4insanity`. La lista de archivos y su dueño está en CONTRATO.md, sección 10.

Orden para aplicarlos:

```bash
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/
```

`secret.yaml` no está en el repo: se crea copiando `secret.example.yaml` y poniendo la contraseña real.
