# Technical Analysis: Aegis Coach User Action Guide & Cloud Infrastructure Specifications

**Author:** Explorer 1 (Systems Architecture & Infrastructure Analysis)  
**Target Output:** Specifications for `mvp_next_steps.md` (User Action Guide)  
**Date:** August 2026  
**Context:** Aegis Coach Phase 2 (Architecture & User Action Guide)  

---

## 1. Executive Summary & Objective

The primary objective of this investigation is to establish the definitive, concrete specifications for the **Aegis Coach User Action Guide** (`mvp_next_steps.md`). 

While automated agents in Phase 2 handle scientific literature acquisition (Askling L-Protocol, Silbernagel Pain Model, Seiler Polarized 80/20, Banister ACWR) and markdown parsing via `markitdown`, human administrators must execute manual cloud provisioning, security firewall configuration, and secret key generation that autonomous software cannot or should not execute unattended.

This analysis provides the complete technical blueprint, step-by-step procedures, configuration snippets, security hardening policies, `.env` templates, and verification commands required to publish an exhaustive, user-friendly, and foolproof `mvp_next_steps.md`.

---

## 2. Infrastructure Layer: Oracle Cloud Infrastructure (OCI) Free Tier

### 2.1 Compute VM Sizing & Shape Architecture
Oracle Cloud Infrastructure (OCI) provides the most generous Always Free tier in cloud computing. Aegis Coach requires low-latency vector indexing, multi-agent microservice execution, and data persistence.

| Specification Parameter | Recommended Production Target | Alternative Fallback Target | Rationale |
|---|---|---|---|
| **Compute Architecture** | **Ampere A1 Compute (ARM64)** | **AMD Standard Compute (x86_64)** | Qdrant and Docker run natively on ARM64 with high power-to-performance efficiency. |
| **Instance Shape** | `VM.Standard.A1.Flex` | `VM.Standard.E2.1.Micro` | Ampere allows 1 to 4 OCPUs and up to 24 GB RAM free forever. |
| **OCPU Allocation** | 2 to 4 OCPUs (ARM) | 1 OCPU (1/8 thread) | High multi-threaded performance for vector similarity calculations and background workers. |
| **RAM Allocation** | 12 GB to 24 GB RAM | 1 GB RAM | Ample memory for Qdrant HNSW vector indexes, OS page cache, and Docker containers. |
| **Operating System** | **Ubuntu 24.04 LTS** (Canonical) | **Ubuntu 22.04 LTS** | Modern Linux kernel (6.8+), native Docker support, standard APT packages. |
| **Boot Volume** | 50 GB to 100 GB (Always Free up to 200 GB) | 47 GB | Sufficient for Docker layers, Qdrant snapshots, and vector payloads. |
| **Public IP** | Ephemeral or Reserved IPv4 | Ephemeral IPv4 | Publicly reachable for REST/gRPC endpoints and webhook ingress. |

### 2.2 Step-by-Step Provisioning Procedure
1. **Log in to OCI Console**: Navigate to `cloud.oracle.com` and select your home region (e.g., `eu-madrid-1`, `eu-frankfurt-1`, `us-ashburn-1`).
2. **Launch Instance**:
   - Menu $\rightarrow$ **Compute** $\rightarrow$ **Instances** $\rightarrow$ **Create Instance**.
   - Name: `aegis-coach-core`.
   - Compartment: Select root or project compartment.
   - Placement: Default Availability Domain (AD-1).
3. **Image and Shape**:
   - Image: Click *Change Image* $\rightarrow$ Select **Ubuntu 24.04** (or Ubuntu 22.04 Minimal/Standard).
   - Shape: Click *Change Shape* $\rightarrow$ Select **Ampere** (ARM) $\rightarrow$ `VM.Standard.A1.Flex` $\rightarrow$ Allocate **2 OCPUs** and **12 GB Memory** (or up to 4 OCPUs / 24 GB).
4. **Networking (VCN)**:
   - Select *Create new virtual cloud network* (or use existing VCN).
   - Select *Create new public subnet*.
   - Ensure **Assign a public IPv4 address** is checked.
5. **SSH Key Pair**:
   - Select *Generate a key pair for me* (and download private key) OR *Upload public key* (`~/.ssh/id_ed25519.pub`).
6. **Create**: Click **Create** and wait $\sim 60\text{ seconds}$ until status changes to **RUNNING**. Record the **Public IP Address**.

---

## 3. Host System Setup & Container Runtime (Docker & Compose)

### 3.1 Initial SSH Connection & System Hardening
From the user's local terminal (Linux/macOS/Windows PowerShell):
```bash
# Secure private key permissions (Linux/macOS)
chmod 600 ~/.ssh/aegis_oci_key

# SSH into the Ubuntu VM
ssh -i ~/.ssh/aegis_oci_key ubuntu@<INSTANCE_PUBLIC_IP>
```

### 3.2 Automated Package Update & Docker Engine Installation
Execute on the remote Ubuntu VM:
```bash
# 1. Update package indexes and install base utilities
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release ufw iptables-persistent htop jq

# 2. Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Set up the stable Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker Engine, CLI, Containerd, and Docker Compose Plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Enable non-root docker execution and auto-start on boot
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# Apply group changes without logout
newgrp docker
```

---

## 4. Qdrant Vector Database Deployment

### 4.1 Storage Architecture & Directory Structure
Qdrant requires persistent host volume mounts for its vector storage (`/qdrant/storage`) and collection snapshots (`/qdrant/snapshots`):

```bash
# Create dedicated directory hierarchy
sudo mkdir -p /opt/qdrant/storage /opt/qdrant/snapshots
sudo chown -R ubuntu:ubuntu /opt/qdrant
```

### 4.2 API Key Generation
To secure the database against unauthorized public access, generate an unguessable 256-bit cryptographic API key:
```bash
# Generate high-entropy API key
openssl rand -hex 32
# Example Output: e8b5f392a10c7d42e6840d21a995cf5807693d258161726a42a033c4ef4e1178
```

### 4.3 Deployment Option A: Docker Compose (Production Standard)
Create project directory and compose file:
```bash
mkdir -p ~/aegis-infra && cd ~/aegis-infra
cat << 'EOF' > docker-compose.yml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: aegis-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"   # REST API & Web UI Dashboard
      - "6334:6334"   # gRPC API (High-performance vector operations)
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
      - QDRANT__TELEMETRY_DISABLED=true
      - QDRANT__SERVICE__ENABLE_STATIC_CONTENT=true
      - QDRANT__LOG_LEVEL=INFO
    volumes:
      - /opt/qdrant/storage:/qdrant/storage
      - /opt/qdrant/snapshots:/qdrant/snapshots
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
EOF
```

Create `.env` inside `~/aegis-infra/.env`:
```bash
cat << EOF > ~/aegis-infra/.env
QDRANT_API_KEY=$(openssl rand -hex 32)
EOF
```

Launch Qdrant daemon:
```bash
docker compose up -d
```

### 4.4 Deployment Option B: Standalone Docker Run Command
For instant single-command execution:
```bash
docker run -d \
  --name aegis-qdrant \
  --restart unless-stopped \
  -p 6333:6333 \
  -p 6334:6334 \
  -v /opt/qdrant/storage:/qdrant/storage \
  -v /opt/qdrant/snapshots:/qdrant/snapshots \
  -e QDRANT__SERVICE__API_KEY="YOUR_GENERATED_API_KEY" \
  -e QDRANT__TELEMETRY_DISABLED=true \
  -e QDRANT__SERVICE__ENABLE_STATIC_CONTENT=true \
  qdrant/qdrant:latest
```

---

## 5. Network Security & Dual-Layer Firewall Configuration

### 5.1 The "Oracle Cloud Firewall Trap" (Critical Technical Nuance)
A common pitfall on OCI is opening ports in the Cloud Console Security List while failing to open them inside Ubuntu's default OS firewall. **Oracle's official Ubuntu images ship with strict iptables rules that DROP all incoming traffic on non-SSH ports by default.**

Security must be configured on **both layers**:
1. **Cloud Layer**: OCI VCN Ingress Rules (Security Lists / Network Security Groups).
2. **Host OS Layer**: Ubuntu `iptables` / `ufw`.

```
           INTERNET (User / App / Webhook)
                         │
                         ▼
      ┌─────────────────────────────────────┐
      │  LAYER 1: OCI VCN Security List     │
      │  (Allows TCP 22, 6333, 6334)        │
      └──────────────────┬──────────────────┘
                         │
                         ▼
      ┌─────────────────────────────────────┐
      │  LAYER 2: Host OS Firewall (Ubuntu) │
      │  (UFW / iptables rules open ports)  │
      └──────────────────┬──────────────────┘
                         │
                         ▼
      ┌─────────────────────────────────────┐
      │  DOCKER ENGINE / QDRANT CONTAINER   │
      └─────────────────────────────────────┘
```

### 5.2 Layer 1: OCI VCN Ingress Rule Configuration
1. In OCI Console, navigate to **Networking** $\rightarrow$ **Virtual Cloud Networks**.
2. Click your active VCN $\rightarrow$ Click **Security Lists** $\rightarrow$ **Default Security List for [VCN Name]**.
3. Click **Add Ingress Rules**:
   - **Ingress Rule 1 (Qdrant REST API & Dashboard)**:
     * Stateless: No
     * Source Type: CIDR
     * Source CIDR: `0.0.0.0/0` (or restricted to your static IP)
     * IP Protocol: `TCP`
     * Source Port Range: All
     * Destination Port Range: `6333`
     * Description: `Aegis Coach Qdrant REST API and Dashboard`
   - **Ingress Rule 2 (Qdrant gRPC API)**:
     * Stateless: No
     * Source Type: CIDR
     * Source CIDR: `0.0.0.0/0` (or restricted to application server CIDR)
     * IP Protocol: `TCP`
     * Source Port Range: All
     * Destination Port Range: `6334`
     * Description: `Aegis Coach Qdrant gRPC API`
4. Click **Add Ingress Rules**.

### 5.3 Layer 2: Host OS Firewall (Ubuntu UFW & iptables)
Run the following commands on the Ubuntu VM to ensure OS-level traffic routing:

```bash
# Method A: Using UFW (Uncomplicated Firewall)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH Access'
sudo ufw allow 6333/tcp comment 'Qdrant REST & UI'
sudo ufw allow 6334/tcp comment 'Qdrant gRPC'
sudo ufw --force enable
sudo ufw status verbose

# Method B: Direct iptables rule persistence (Fixes OCI default REJECT chain)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 6333 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 6334 -j ACCEPT
sudo netfilter-persistent save
```

---

## 6. Environment Variables & Secrets Management

### 6.1 Complete Production `.env` Template
This template must be populated by the user in the Aegis Coach application root (`aegis-coach/.env`):

```dotenv
# ==============================================================================
# AEGIS COACH — PRODUCTION ENVIRONMENT CONFIGURATION
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CORE APPLICATION RUNTIME & SECURITY
# ------------------------------------------------------------------------------
AEGIS_ENVIRONMENT=production
AEGIS_MOCK_MODE=false
AEGIS_LIVE_MODE=true
# 32-byte hex secret key for tenant JWT signing and token HMAC encryption
AEGIS_SECRET_KEY=replace_with_openssl_rand_hex_32

# ------------------------------------------------------------------------------
# 2. TELEGRAM BOT INTERFACE (CONVERSATIONAL INGRESS)
# ------------------------------------------------------------------------------
# Obtained via Telegram @BotFather -> /newbot
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz_SampleToken
# User ID obtained via @userinfobot or @raw_data_bot for admin diagnostic alerts
TELEGRAM_ADMIN_CHAT_ID=123456789

# ------------------------------------------------------------------------------
# 3. LLM PROVIDER API KEYS (MULTI-TIER AI ORCHESTRATION)
# ------------------------------------------------------------------------------
# Fast Path / Intent Routing / Voice Transcription / Extraction (Tier-2)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Clinical RAG / Deep Sports Medicine Synthesis (Tier-1)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Cost-Optimized Fast Reasoning Alternative (Optional Tier-2)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ------------------------------------------------------------------------------
# 4. QDRANT VECTOR DATABASE (ORACLE CLOUD VM)
# ------------------------------------------------------------------------------
# Replace <YOUR_OCI_PUBLIC_IP> with the actual Oracle Cloud VM public IPv4 address
QDRANT_HOST=http://<YOUR_OCI_PUBLIC_IP>:6333
QDRANT_GRPC_PORT=6334
# The exact secret key generated and configured in Oracle Docker QDRANT__SERVICE__API_KEY
QDRANT_API_KEY=replace_with_your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=aegis_sports_science

# ------------------------------------------------------------------------------
# 5. ATHLETIC DATA PLATFORMS (INTERVALS.ICU & GARMIN SYNC)
# ------------------------------------------------------------------------------
# Obtained at intervals.icu -> Settings -> Developer Settings
INTERVALS_ICU_API_KEY=i_xxxxxxxxxxxxxxxxxxxxxxxx
INTERVALS_ICU_ATHLETE_ID=i123456

# Strava Developer App Credentials (Optional Strava GPS Activity Webhook)
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRAVA_REFRESH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ------------------------------------------------------------------------------
# 6. SUPABASE (RELATIONAL DATABASE & ROW-LEVEL SECURITY)
# ------------------------------------------------------------------------------
SUPABASE_URL=https://xxxxxxxxxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
DATABASE_URL=postgresql://postgres:[YOUR_DB_PASSWORD]@db.xxxxxxxx.supabase.co:5432/postgres
```

### 6.2 Step-by-Step Secrets Acquisition Cheatsheet

| Secret Variable | Service Portal | Direct Navigation Path | Cost / Quota |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram Messenger | Search `@BotFather` $\rightarrow$ Send `/newbot` $\rightarrow$ Name bot $\rightarrow$ Copy HTTP API Token | Free |
| `OPENAI_API_KEY` | OpenAI Platform | `platform.openai.com/api-keys` $\rightarrow$ *Create new secret key* $\rightarrow$ Set permissions to Model Capabilities | Pay-as-you-go |
| `ANTHROPIC_API_KEY` | Anthropic Console | `console.anthropic.com/settings/keys` $\rightarrow$ *Create Key* | Pay-as-you-go |
| `DEEPSEEK_API_KEY` | DeepSeek Platform | `platform.deepseek.com/api_keys` $\rightarrow$ *Create API Key* | Pay-as-you-go |
| `INTERVALS_ICU_API_KEY` | Intervals.icu | `intervals.icu` $\rightarrow$ Log in $\rightarrow$ **Settings** $\rightarrow$ Scroll to **Developer Settings** $\rightarrow$ Copy API Key & Athlete ID | Free |
| `QDRANT_API_KEY` | Oracle Host Terminal | Run `openssl rand -hex 32` locally on host | Free |

---

## 7. Verification & Diagnostic Test Protocols

To ensure that the user can verify their Qdrant vector database and cloud infrastructure with 100% confidence, provide this multi-stage verification suite:

### 7.1 Stage 1: Container Status & Process Health
Execute directly on the Oracle Ubuntu VM:
```bash
# Check Docker container status
docker ps --filter "name=aegis-qdrant"
# Output should show: STATUS Up ... 0.0.0.0:6333->6333/tcp, 0.0.0.0:6334->6334/tcp

# View real-time container startup logs
docker logs --tail 20 aegis-qdrant
# Look for: "Qdrant HTTP listening on 6333", "Qdrant gRPC listening on 6334", "Access token is configured"
```

### 7.2 Stage 2: Remote HTTP REST API & Health Check
Execute from user's local workstation (e.g. Windows PowerShell or Mac/Linux terminal):

```bash
# 1. Unauthenticated root health check
curl -s http://<YOUR_OCI_PUBLIC_IP>:6333/healthz
# Expected Response: "healthz check passed" or {"title":"qdrant - vector search engine"}

# 2. Authenticated Telemetry & Cluster Metadata Check
curl -s -H "api-key: <YOUR_QDRANT_API_KEY>" http://<YOUR_OCI_PUBLIC_IP>:6333/
# Expected JSON Response:
# {
#   "title": "qdrant - vector search engine",
#   "version": "1.11.x",
#   "commit": "..."
# }

# 3. Unauthorized Access Rejection Test (Validates API key security)
curl -i http://<YOUR_OCI_PUBLIC_IP>:6333/collections
# Expected HTTP Status: 401 Unauthorized / 403 Forbidden
```

### 7.3 Stage 3: End-to-End Collection Lifecycle Test (Create, Insert, Search, Drop)
Execute from local terminal:

```bash
# 1. Create a test collection 'aegis_verification_test' (128 dimensions, Cosine distance)
curl -s -X PUT "http://<YOUR_OCI_PUBLIC_IP>:6333/collections/aegis_verification_test" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_QDRANT_API_KEY>" \
  -d '{
    "vectors": {
      "size": 128,
      "distance": "Cosine"
    }
  }' | jq .
# Expected Output: { "result": true, "status": "ok", "time": 0.00... }

# 2. Verify collection exists
curl -s -H "api-key: <YOUR_QDRANT_API_KEY>" http://<YOUR_OCI_PUBLIC_IP>:6333/collections | jq .
# Expected Output: { "result": { "collections": [ { "name": "aegis_verification_test" } ] } }

# 3. Clean up / Delete test collection
curl -s -X DELETE "http://<YOUR_OCI_PUBLIC_IP>:6333/collections/aegis_verification_test" \
  -H "api-key: <YOUR_QDRANT_API_KEY>" | jq .
# Expected Output: { "result": true, "status": "ok" }
```

### 7.4 Stage 4: Web UI Dashboard Access Test
1. Open web browser and navigate to: `http://<YOUR_OCI_PUBLIC_IP>:6333/dashboard`.
2. The Qdrant Web UI will prompt for **API Key**.
3. Paste `<YOUR_QDRANT_API_KEY>`.
4. Confirm interactive dashboard loads showing:
   - Collections explorer
   - Storage size & memory allocations
   - Interactive console for running REST requests

### 7.5 Stage 5: Python SDK Live Connection Script
Provide a ready-to-run diagnostic script (`test_qdrant_connection.py`):

```python
import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

QDRANT_HOST = os.getenv("QDRANT_HOST", "http://<YOUR_OCI_PUBLIC_IP>:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "<YOUR_QDRANT_API_KEY>")

print(f"Connecting to Qdrant at {QDRANT_HOST}...")
client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY, timeout=10.0)

# Check server health
collections = client.get_collections()
print(f"✅ Success! Connected to Qdrant. Active Collections: {collections.collections}")
```

---

## 8. Summary of Deliverables for `mvp_next_steps.md`

Based on this analysis, the final user-facing guide `mvp_next_steps.md` must be organized into 6 clean, actionable, step-by-step sections:
1. **Phase Overview & Prerequisites**: What the user needs before starting (Free OCI account, Telegram account, API keys).
2. **Oracle Cloud Free Tier VM Setup**: Step-by-step UI walkthrough with screenshots/field mappings for Ampere A1 ARM instance creation.
3. **Docker & Container Runtime Installation**: Copy-paste shell commands for Ubuntu 24.04.
4. **Qdrant Vector Database Deployment**: Docker Compose file, API key generation, and background container startup.
5. **Dual-Layer Firewall & Security**: OCI VCN Ingress Rules + Ubuntu UFW/iptables commands (with explicit warning about the OCI iptables trap).
6. **Environment Configuration & Verification Suite**: Complete `.env` file template and 5-stage verification test commands.

---
*End of Technical Analysis.*
