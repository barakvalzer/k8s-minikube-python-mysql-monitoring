# K8s Minikube Python + MySQL + Prometheus/Grafana Monitoring + ArgoCD + GitHub Actions

A complete DevOps project that deploys a Flask app, MySQL, and monitoring using Prometheus and Grafana on Kubernetes.
It uses **ArgoCD** for GitOps-style continuous delivery and **GitHub Actions** to automate deployment and ArgoCD installation via Helm.

---

## ✅ Features

- Flask API app with Prometheus metrics endpoint (`/metrics`)
- MySQL deployment
- Prometheus + Grafana monitoring
- ArgoCD installed via Helm
- ArgoCD user/password generated and pushed to GitHub Secrets dynamically via Python script
- GitHub Actions CI/CD pipeline:
  - Installs ArgoCD
  - Logs in using secrets
  - Syncs your application

---

## 🚀 Quick Start (Local)

```bash
minikube start --cpus=4 --memory=6g
eval $(minikube docker-env)
docker build -t flask-app:latest ./app
kubectl apply -f k8s/
minikube service grafana
```

---

## 📦 ArgoCD Setup via GitHub Actions

### GitHub Secrets Required

| Secret Name        | Description                    |
|--------------------|--------------------------------|
| `GH_PAT`           | GitHub personal access token with `repo` and `admin:repo_hook` permissions |
| `ARGOCD_SERVER`    | Your ArgoCD server URL (e.g., `argocd.example.com`) |

> You do **not** need to manually define `ARGOCD_USERNAME` or `ARGOCD_PASSWORD`. They will be generated dynamically.

---

## 🔐 Generate ArgoCD Username/Password Automatically

The GitHub Actions workflow will:

1. Run the script `scripts/create_github_secrets.py`
2. Generate a random username and password
3. Upload them as:
   - `ARGOCD_USERNAME`
   - `ARGOCD_PASSWORD`

These secrets are then used for:
- Installing ArgoCD via Helm with your chosen password
- Logging into ArgoCD from GitHub Actions
- Syncing your application (`flask-monitoring-app`)

---

## 🛠 GitHub Actions Workflow Summary

Located at: `.github/workflows/deploy-argocd-helm.yaml`

```yaml
- Generates username/password with Python
- Pushes to GitHub Secrets
- Installs ArgoCD via Helm with custom password
- Waits for ArgoCD to be ready
- Logs in to ArgoCD using secrets
- Syncs your ArgoCD Application
```

---

## 📁 Repo Structure

```
.
├── app/                       # Flask app
├── k8s/
│   ├── app/                   # Flask app deployment YAML
│   ├── db/                    # MySQL deployment YAML
│   ├── monitoring/            # Prometheus/Grafana YAML
│   └── argo/argocd-app.yaml   # ArgoCD Application definition
├── scripts/
│   └── create_github_secrets.py
├── .github/workflows/
│   └── deploy-argocd-helm.yaml
└── README.md
```

---

## 👨‍💻 Contributors

Maintained by [@barakvalzer](https://github.com/barakvalzer)