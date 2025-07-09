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
