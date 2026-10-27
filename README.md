# Kubernetes: Two Services Talking in the Same Namespace

A small hands-on example showing how two services in the **same namespace**
communicate using **just the Service name** (no IP, no namespace, no FQDN).

```
 Browser ──► frontend-service ──► frontend pod
                                      │
                                      │  http://backend-service:5000
                                      ▼
                              backend-service ──► backend pods (x2)
```

Both services live in the `demo-app` namespace. The frontend simply calls
`http://backend-service:5000`, and Kubernetes DNS resolves it.

## Project layout

```
.
├── backend/            Flask API  (port 5000)
├── frontend/           Flask app that calls the backend (port 8080)
└── k8s/
    ├── namespace.yaml
    ├── backend.yaml    Deployment + ClusterIP Service
    └── frontend.yaml   Deployment + LoadBalancer Service
```

## 1. Build and push the images

Replace `YOUR_DOCKERHUB_USER` with your Docker Hub username.

```bash
docker build -t YOUR_DOCKERHUB_USER/backend:1.0  ./backend
docker build -t YOUR_DOCKERHUB_USER/frontend:1.0 ./frontend

docker login
docker push YOUR_DOCKERHUB_USER/backend:1.0
docker push YOUR_DOCKERHUB_USER/frontend:1.0
```

Then update the `image:` lines in `k8s/backend.yaml` and `k8s/frontend.yaml`.

## 2. Deploy

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

kubectl get all -n demo-app
```

## 3. Test

```bash
# Easiest on any cluster (minikube, kind, AKS):
kubectl port-forward svc/frontend-service 8080:80 -n demo-app
curl http://localhost:8080/
```

Expected response:

```json
{
  "service": "frontend",
  "called": "http://backend-service:5000",
  "backend_response": {
    "service": "backend",
    "message": "Hello from the BACKEND service!",
    "pod": "backend-xxxxxxxxxx-xxxxx"
  }
}
```

Refresh a few times and the `pod` value changes, because the Service
load-balances across both backend replicas.

## How the name resolves

| Caller location | URL to use |
|---|---|
| Same namespace | `http://backend-service:5000` |
| Different namespace | `http://backend-service.demo-app:5000` |
| Fully qualified | `http://backend-service.demo-app.svc.cluster.local:5000` |

## Clean up

```bash
kubectl delete namespace demo-app
```

## Push this project to GitHub

```bash
git init
git add .
git commit -m "Two services communicating in the same namespace"
git branch -M main
git remote add origin https://github.com/<your-username>/k8s-service-communication.git
git push -u origin main
```
