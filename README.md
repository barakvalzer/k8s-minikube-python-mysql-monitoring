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
---

## 🔄 ArgoCD Sync via GitHub Actions

This repo includes a GitHub Actions workflow (`.github/workflows/deploy-argocd-helm.yaml`) that:

- Installs the ArgoCD CLI
- Logs in to your running ArgoCD server
- Syncs the `flask-monitoring-app` application

### Required GitHub Secrets

| Secret Name        | Description                          |
|--------------------|--------------------------------------|
| `ARGOCD_SERVER`    | Your ArgoCD hostname or IP           |
| `ARGOCD_USERNAME`  | Your ArgoCD username (e.g. `admin`)  |
| `ARGOCD_PASSWORD`  | Your ArgoCD password                 |---

## 🚀 Full Deployment Guide (Manual + GitHub Actions)

This guide shows how to deploy the full stack and connect ArgoCD with GitHub Actions.

---

### 🛠 1. Prerequisites

Ensure you have:
- A running Kubernetes cluster (Minikube, EKS, GKE, etc.)
- ArgoCD installed and accessible via hostname/IP
- `argocd-server` exposed (e.g., NodePort or Ingress)
- A valid ArgoCD username and password (e.g., admin)

---

### 🔐 2. Add GitHub Secrets

Go to your GitHub repo → **Settings** → **Secrets and Variables** → **Actions**

Click **New repository secret** and add the following:

| Secret Name        | Value Example               |
|--------------------|-----------------------------|
| `ARGOCD_SERVER`    | `argocd.example.com` or `localhost:8080` |
| `ARGOCD_USERNAME`  | `admin`                     |
| `ARGOCD_PASSWORD`  | Your ArgoCD admin password  |

---

### ⚙️ 3. Push Your Code to GitHub

Once the secrets are in place, any push to the `main` branch will trigger:

- ArgoCD CLI installation
- Login to your ArgoCD instance
- Sync of the `flask-monitoring-app` defined in `k8s/argo/argocd-app.yaml`

---

### 📦 ArgoCD Application Manifest

Located at: `k8s/argo/argocd-app.yaml`

Make sure this file points to the correct path and repo:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: flask-monitoring-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_USERNAME/YOUR_REPO
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

> Don't forget to replace `repoURL` with your actual GitHub repo!

---

### ✅ 4. Verify in ArgoCD UI

1. Port-forward ArgoCD if needed:
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

2. Visit [https://localhost:8080](https://localhost:8080)  
3. Login with the credentials you provided in the secrets  
4. You should see your `flask-monitoring-app` and its sync status

---

That's it! 🎉 You now have a full CI/CD pipeline for ArgoCD integrated with GitHub Actions.---

## 🔐 How to Generate Secrets for Local Minikube ArgoCD

If you're running ArgoCD inside **Minikube**, here's how to extract the credentials and configure GitHub Secrets manually:

---

### ✅ Step 1: Get ArgoCD Admin Password

Run this in your terminal:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

This will output the default admin password.

---

### ✅ Step 2: Port-forward ArgoCD (if needed)

Expose the ArgoCD UI and API locally:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Now your ArgoCD server is accessible at:  
**`https://localhost:8080`**

---

### ✅ Step 3: Add GitHub Secrets

Go to your repo → **Settings** → **Secrets and Variables** → **Actions**  
Click **New repository secret** and create:

| Secret Name         | Value                             |
|---------------------|------------------------------------|
| `ARGOCD_SERVER`     | `localhost:8080`                   |
| `ARGOCD_USERNAME`   | `admin`                            |
| `ARGOCD_PASSWORD`   | *(password from Step 1)*           |

⚠️ You must keep the port-forward command running locally while testing this.

---

### 🧪 Optional: Verify from CLI

```bash
argocd login localhost:8080 --username admin --password <your-password> --insecure
argocd app list
```

---

This allows your GitHub Actions workflow to authenticate with your locally running ArgoCD in Minikube.