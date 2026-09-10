# 🚀 n8n Standalone Deployment on Render (Step-by-Step Guide)

This package contains everything needed to deploy and run **n8n** as an independent, standalone cloud automation service on **Render**.

---

## 📁 Package Structure

```text
n8n_standalone/
├── Dockerfile                   # Official n8n Docker image configured for Render
├── render.yaml                  # 1-Click Render Infrastructure Blueprint
├── .env.example                 # Environment variables reference
├── RENDER_DEPLOY_GUIDE.md       # This complete guide
└── workflows/
    ├── 1_live_crash_monitor_and_ingestion.json   # Incident ingestion & severity filter
    └── 2_multi_channel_ads_automation.json       # Google, Meta, Snapchat ads dispatcher
```

---

## 🛠️ Step 1: Push `n8n_standalone` to GitHub
Ensure this `n8n_standalone` folder is committed and pushed on your branch:
```powershell
git add n8n_standalone
git commit -m "Add standalone n8n deployment package and workflows"
git push origin ashok
```

---

## 🌐 Step 2: Deploy to Render (Free or Starter Plan)

1. Go to **[https://dashboard.render.com/](https://dashboard.render.com/)** and log in.
2. Click **"New +"** (top right) $\rightarrow$ select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and connect your GitHub repository (`georgia_crash_app`).
4. Select branch: **`ashok`**.
5. Configure the Web Service:
   - **Name:** `n8n-georgia-automation`
   - **Language / Runtime:** **Docker**
   - **Root Directory:** `n8n_standalone`
   - **Region:** Any (e.g. *Oregon (US West)* or *Ohio (US East)*)
   - **Instance Type:** **Free** (or *Starter $7/mo* for persistent disk and no spin-down)

---

## 🔑 Step 3: Add Environment Variables in Render

In the Render Web Service settings, go to **Environment** $\rightarrow$ **Add Environment Variable**:

| Key | Value | Description |
| :--- | :--- | :--- |
| `N8N_PORT` | `5678` | Internal n8n port |
| `PORT` | `5678` | Render mapped port |
| `N8N_PROTOCOL` | `https` | Ensures SSL webhooks work |
| `WEBHOOK_URL` | `https://n8n-georgia-automation.onrender.com/` | Replace with your exact Render URL |
| `N8N_ENCRYPTION_KEY` | *(Click "Generate" in Render or paste 32 random chars)* | Encrypts credentials |
| `GENERIC_TIMEZONE` | `America/New_York` | Georgia timezone |
| `DJANGO_BACKEND_URL` | `https://your-django-backend.vercel.app/` | Your Django API domain |

6. Click **"Create Web Service"**.
7. Render will build the Docker container and provide you with a live URL (e.g. `https://n8n-georgia-automation.onrender.com`).

---

## 📥 Step 4: Import Workflows into n8n

1. Open your live Render n8n URL in your browser.
2. Set up your admin email and password.
3. Click **"Workflows"** $\rightarrow$ Click **"Add workflow"** $\rightarrow$ Click **Menu (3 dots) top right** $\rightarrow$ **"Import from File"**.
4. Import both JSON files:
   - `workflows/1_live_crash_monitor_and_ingestion.json`
   - `workflows/2_multi_channel_ads_automation.json`
5. Click **"Publish / Activate"** toggle on both workflows.

---

## 🎯 Step 5: Test Webhook Endpoints

Your live webhook URLs are ready to receive data:
- **Incident Ingestion Webhook:**
  `POST https://n8n-georgia-automation.onrender.com/webhook/ingest-live-crash`
- **Ads Pipeline Webhook:**
  `POST https://n8n-georgia-automation.onrender.com/webhook/trigger-crash-ads`
