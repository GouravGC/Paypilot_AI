# 🛍️ PayPilot AI

**Your AI-powered commerce and payment copilot.**

PayPilot AI is a Python-based AI commerce assistant designed to help users clarify shopping requirements and explore relevant recommendations. It combines a Streamlit interface, a FastAPI backend, and OpenRouter-powered AI assistance, with Channel3 product discovery and PayPal Sandbox checkout planned as future integrations.

## ✨ Features

- **AI Shopping Assistant:** Convert natural-language shopping requests into useful, criteria-based recommendations.
- **LLM Integration:** Connect to OpenRouter using a configurable model.
- **FastAPI Backend:** Expose API endpoints for health monitoring and AI assistance.
- **Streamlit Frontend:** Provide a simple, interactive shopping-assistant interface.
- **Automated Testing:** Validate API endpoints using pytest.
- **Docker Support:** Package the backend for consistent deployment.
- **CI/CD with GitHub Actions:** Run tests, build and publish Docker images to GitHub Container Registry (GHCR), and trigger Render deployments.
- **Planned Integrations:** Channel3 product discovery and PayPal Developer Sandbox checkout.

> **Project status:** The AI assistance and backend API are implemented. Live product discovery, payment processing, and production checkout are planned integrations and should not be considered operational until implemented and tested.

## 🏗️ Architecture

```text
User
 |
 v
Streamlit Frontend
 |
 v
FastAPI Backend
 |
 v
OpenRouter AI
 |
 v
Shopping Assistance Response

GitHub Push to main
 |
 v
GitHub Actions
 |
 +--> Run pytest
 |
 +--> Build Docker image
 |
 +--> Publish image to GHCR
 |
 +--> Trigger Render deployment
 |
 v
Render-hosted FastAPI Backend
```

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Frontend | Streamlit |
| Backend | FastAPI |
| AI integration | OpenRouter |
| Configuration | python-dotenv, pydantic-settings |
| Testing | pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Container registry | GitHub Container Registry (GHCR) |
| Backend deployment | Render |
| Planned commerce integration | Channel3 |
| Planned payments integration | PayPal Developer Sandbox |

## 📁 Project Structure

```text
PayPilot AI/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── src/
│   └── paypilot/
│       ├── api/
│       │   └── main.py
│       ├── ai/
│       ├── commerce/
│       └── payments/
├── tests/
│   └── test_health.py
├── app.py
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
├── render.yaml
├── LICENSE
└── README.md
```

## ⚙️ Local Setup

### Prerequisites

- Python 3.11
- Conda or another Python virtual environment manager
- Git
- An OpenRouter API key for live AI responses
- Docker Desktop (optional, for container testing)

### 1. Clone the repository

```bash
git clone https://github.com/GouravGC/Paypilot_AI.git
cd Paypilot_AI
```

### 2. Create the Python environment

Using Conda:

```bash
conda create -n paypal python=3.11.10 -y
conda activate paypal
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Windows CMD:

```bat
copy .env.example .env
```

Edit `.env` and enter your own API key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free
```

Keep your real `.env` file private. Never commit API keys, access tokens, or deployment secrets.

### 5. Start the FastAPI backend

From the repository root:

```bash
python -m uvicorn src.paypilot.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Check the health endpoint:

http://127.0.0.1:8000/health

### 6. Start the Streamlit frontend

Open a second terminal, activate the same Conda environment, and run:

```bash
conda activate paypal
streamlit run app.py
```

Streamlit will display the local URL for the frontend, usually:

http://localhost:8501

Keep the backend running while testing frontend features that depend on the API.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Basic API information |
| GET | `/health` | Backend health check |
| POST | `/ai/assist` | AI assistance endpoint |

For request and response schemas, use the interactive documentation at `/docs`.

## 🧪 Run Automated Tests

From the project root:

```bash
python -m pytest -v
```

The current baseline tests cover the root and health endpoints.

## 🐳 Run with Docker

Build the backend image:

```bash
docker build -t paypilot-ai:local .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --env-file .env paypilot-ai:local
```

Verify the backend:

http://localhost:8000/health

Stop the container with `Ctrl+C`.

## 🚀 CI/CD Pipeline

The workflow is located at `.github/workflows/ci-cd.yml`.

On pushes to `main`, GitHub Actions is configured to:

1. Check out the repository.
2. Set up Python 3.11.
3. Install dependencies.
4. Run automated tests with pytest.
5. Build the backend Docker image after tests pass.
6. Publish the image to GHCR using both `latest` and the commit SHA tags.
7. Trigger the Render deployment hook when the corresponding GitHub secret is configured.

Pull requests targeting `main` run the automated test job. The image publishing and deployment job is restricted to pushes to `main`.

### Required GitHub configuration

Add this repository secret under **Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | Triggers the Render deployment |

The workflow uses GitHub's `GITHUB_TOKEN` to publish the container image. Ensure the workflow has `packages: write` permission.

### Container image

The workflow is configured to publish:

```text
ghcr.io/gouravgc/paypilot-ai:latest
ghcr.io/gouravgc/paypilot-ai:<commit-sha>
```

The Render backend service should use the `latest` image reference. Make sure Render can access the GHCR package.

### Verify a deployment

After pushing to `main`:

- Confirm the test job passes.
- Confirm the Docker image build and GHCR publishing succeed.
- Confirm the Render hook step succeeds.
- Check the deployment status and logs in Render.
- Verify the deployed `/health` endpoint.

A successful GitHub Actions run confirms that the configured workflow steps succeeded; verify the running service separately to confirm the application is healthy.

## ☁️ Deployment

### Backend — Render

Deploy the Docker image from GHCR using Render's existing-image deployment option. Configure the required runtime environment variables in the Render dashboard, including `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`.

### Frontend — Streamlit Community Cloud

Deploy `app.py` through Streamlit Community Cloud. Configure the frontend's API URL to point to the deployed Render backend rather than `127.0.0.1`.

Store frontend secrets in Streamlit's secrets configuration, not in source code.

## 🔐 Security

- Never commit `.env` or real API keys.
- Keep deployment hooks and tokens in the relevant platform's secret settings.
- Avoid embedding secrets in Docker image layers.
- Use sandbox credentials when implementing payment integrations.
- Verify authentication, authorization, validation, and error handling before exposing payment functionality publicly.

## 🗺️ Roadmap

- [x] Streamlit AI shopping-assistant interface
- [x] FastAPI backend and health endpoints
- [x] OpenRouter integration
- [x] Automated API tests
- [x] Docker-based backend packaging
- [x] GitHub Actions CI/CD workflow configuration
- [ ] Verify GHCR publishing and Render deployment end to end
- [ ] Deploy the Streamlit frontend
- [ ] Integrate Channel3 for live product discovery
- [ ] Integrate PayPal Developer Sandbox checkout
- [ ] Add integration tests and expanded error handling

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests.
4. Run `python -m pytest -v`.
5. Submit a pull request.

## 📄 License

This project is distributed under the license specified in the repository's `LICENSE` file.
