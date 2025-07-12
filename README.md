# K8s Minikube Python + MySQL + Grafana Monitoring

A simple Kubernetes setup using Minikube that deploys:
- Flask app with Prometheus metrics
- MySQL database
- Prometheus + Grafana dashboards

## Usage

```bash
minikube start
eval $(minikube docker-env)
docker build -t flask-app:latest ./app
kubectl apply -f k8s/
minikube service grafana
```


---

## ArgoCD Setup

1. **Install ArgoCD**:
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. **Access ArgoCD UI**:
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
- Open in browser: https://localhost:8080
- Default login:
  - **Username**: `admin`
  - **Password**: Run:
    ```bash
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
    ```

3. **Deploy ArgoCD Application**:
```bash
kubectl apply -f k8s/argo/argocd-app.yaml -n argocd
```

4. **(Optional) Sync from GitHub Actions**:
Make sure you set a GitHub secret named `ARGOCD_PASSWORD` and update the ArgoCD server address in `.github/workflows/argocd-sync.yaml`.