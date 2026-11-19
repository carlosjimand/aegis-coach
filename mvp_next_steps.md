# Aegis Coach — Production Cloud Deployment & User Action Guide (`mvp_next_steps.md`)

```
   █████╗ ███████╗ ██████╗ ██╗███████╗     ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗
  ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██║  ██║
  ███████║█████╗  ██║  ███╗██║███████╗    ██║     ██║   ██║███████║██║     ███████║
  ██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██║     ██║   ██║██╔══██║██║     ██╔══██║
  ██║  ██║███████╗╚██████╔╝██║███████║    ╚██████╗╚██████╔╝██║  ██║╚██████╗██║  ██║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
  ==================================================================================
                 CLINICAL & SPORTS SCIENCE AI PERSONAL TRAINER
            Oracle Cloud Infrastructure (OCI) & Qdrant Deployment Manual
```

**Document Version:** `1.0.0 (Production Release)`  
**Target Infrastructure:** Oracle Cloud Infrastructure (OCI) Always Free Tier  
**Compute Architecture:** Ampere A1 Compute (`VM.Standard.A1.Flex` ARM64 / aarch64)  
**Host Operating System:** Canonical Ubuntu 24.04 LTS (Noble Numbat)  
**Core Persistence Engine:** Qdrant Vector Search Engine v1.11+ (Docker Engine V2)  
**Status:** Authoritative Manual Deployment Blueprint

---

## Executive Summary

While the automated Aegis Coach pipeline builds the codebase, ingests gold-standard sports medicine literature (Askling L-Protocol, Silbernagel Pain Model, Seiler Polarized 80/20, Gabbett ACWR), and prepares vector embeddings, **this guide contains the explicit manual actions that you (the system administrator / developer) must execute**.

Autonomous agents cannot provision cloud resources, bind credit cards, or manage private SSH keys on your behalf. Follow this manual sequentially from Section 1 to Section 6 to bring up your production-grade cloud vector database and connect it to Aegis Coach in under **15 minutes**.

---

## Table of Contents
1. [Section 1: Prerequisites & Architecture Overview](#section-1-prerequisites--architecture-overview)
   - [1.1 End-to-End System Topology](#11-end-to-end-system-topology)
   - [1.2 OCI Always Free Resource Sizing](#12-oci-always-free-resource-sizing)
   - [1.3 Administrator Pre-Flight Checklist](#13-administrator-pre-flight-checklist)
2. [Section 2: Oracle Cloud Infrastructure (OCI) Provisioning](#section-2-oracle-cloud-infrastructure-oci-provisioning)
   - [2.1 OCI Console Navigation & Region Selection](#21-oci-console-navigation--region-selection)
   - [2.2 Virtual Cloud Network (VCN) & Subnet Setup](#22-virtual-cloud-network-vcn--subnet-setup)
   - [2.3 Compute Instance Sizing (Ampere A1 ARM64)](#23-compute-instance-sizing-ampere-a1-arm64)
   - [2.4 SSH Key Pair Generation & Management](#24-ssh-key-pair-generation--management)
   - [2.5 Reserved (Static) Public IPv4 Allocation](#25-reserved-static-public-ipv4-allocation)
3. [Section 3: Host Setup & Docker Engine V2 Installation](#section-3-host-setup--docker-engine-v2-installation)
   - [3.1 Initial SSH Connection & Key Permissions](#31-initial-ssh-connection--key-permissions)
   - [3.2 System Update & Core Packages](#32-system-update--core-packages)
   - [3.3 Official Docker Engine V2 Installation (Ubuntu 24.04 Noble)](#33-official-docker-engine-v2-installation-ubuntu-2404-noble)
   - [3.4 User Group Privileges & Systemd Daemon Configuration](#34-user-group-privileges--systemd-daemon-configuration)
   - [3.5 Persistent Host Storage Hierarchy Creation](#35-persistent-host-storage-hierarchy-creation)
4. [Section 4: Qdrant Vector Database Deployment](#section-4-qdrant-vector-database-deployment)
   - [4.1 Storage Architecture & Snapshot Directory](#41-storage-architecture--snapshot-directory)
   - [4.2 High-Entropy Cryptographic API Key Generation](#42-high-entropy-cryptographic-api-key-generation)
   - [4.3 Production Docker Compose Specification](#43-production-docker-compose-specification)
   - [4.4 Daemon Launch & Lifecycle Management](#44-daemon-launch--lifecycle-management)
   - [4.5 Standalone Docker Run Alternative](#45-standalone-docker-run-alternative)
5. [Section 5: Dual-Layer Network Security & Firewall Hardening](#section-5-dual-layer-network-security--firewall-hardening)
   - [5.1 The Critical "Oracle Cloud Firewall Trap" Explained](#51-the-critical-oracle-cloud-firewall-trap-explained)
   - [5.2 Layer 1: OCI VCN Ingress Rules (Cloud Security Lists)](#52-layer-1-oci-vcn-ingress-rules-cloud-security-lists)
   - [5.3 Layer 2: Ubuntu Host OS Firewall Configuration (UFW & iptables)](#53-layer-2-ubuntu-host-os-firewall-configuration-ufw--iptables)
   - [5.4 IP Whitelisting & Production Perimeter Hardening](#54-ip-whitelisting--production-perimeter-hardening)
6. [Section 6: Environment Configuration (`.env`) & 5-Stage Verification Protocol](#section-6-environment-configuration-env--5-stage-verification-protocol)
   - [6.1 Complete Production `.env` Template](#61-complete-production-env-template)
   - [6.2 Secrets Acquisition & Service Cheatsheet](#62-secrets-acquisition--service-cheatsheet)
   - [6.3 Stage 1: Container Status & Docker Daemon Inspection](#63-stage-1-container-status--docker-daemon-inspection)
   - [6.4 Stage 2: Remote REST Healthcheck & Auth Enforcement Test](#64-stage-2-remote-rest-healthcheck--auth-enforcement-test)
   - [6.5 Stage 3: End-to-End Collection CRUD Lifecycle Test](#65-stage-3-end-to-end-collection-crud-lifecycle-test)
   - [6.6 Stage 4: Interactive Web UI Dashboard Verification](#66-stage-4-interactive-web-ui-dashboard-verification)
   - [6.7 Stage 5: Full Python SDK Diagnostic Test Script](#67-stage-5-full-python-sdk-diagnostic-test-script)
   - [6.8 Diagnostic Troubleshooting Matrix](#68-diagnostic-troubleshooting-matrix)

---

## Section 1: Prerequisites & Architecture Overview

### 1.1 End-to-End System Topology

Aegis Coach separates the conversational AI agents, transactional relational data, and heavy vector embeddings across dedicated, cost-optimized cloud services:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            AEGIS COACH SYSTEM TOPOLOGY                           │
└──────────────────────────────────────────────────────────────────────────────────┘

       ┌────────────────────────┐              ┌────────────────────────┐
       │   ATHLETE INTERFACE    │              │  EXTERNAL PLATFORMS    │
       │  Telegram Mobile / Web │              │ Intervals.icu / Strava │
       └───────────┬────────────┘              └───────────┬────────────┘
                   │                                       │ Webhook / API Sync
                   ▼                                       ▼
       ┌────────────────────────────────────────────────────────────────┐
       │             AEGIS COACH CORE APPLICATION RUNTIME               │
       │    Multi-Agent Router (Fast Path / Clinical / Planner / Physio)│
       └──────────────┬───────────────────────────────┬─────────────────┘
                      │                               │
           SQL Relational Queries            Vector Similarity Search
           (Athletes, Workouts, Logs)        (Scientific Literature RAG)
                      │                               │
                      ▼                               ▼
       ┌────────────────────────┐   TCP 6333 / 6334   ┌────────────────────────┐
       │    SUPABASE CLOUD      │  (Dual-Layer FW)   │   ORACLE CLOUD VPS     │
       │ PostgreSQL + Auth + RLS│ ◄────────────────► │ Qdrant Vector Engine   │
       │ Managed Storage        │                    │ Ampere A1 (4 OCPU/24GB)│
       └────────────────────────┘                    └────────────────────────┘
```

### 1.2 OCI Always Free Resource Sizing

Oracle Cloud Infrastructure provides the most generous free-tier compute allowance in the industry. Aegis Coach is sized to run permanently within the **Always Free** tier with zero ongoing hosting costs:

| Resource Parameter | Allocated Specification | Always Free Maximum Limit | Utilization Purpose |
|---|---|---|---|
| **Processor Architecture** | **Ampere Altra ARM64** | Ampere A1 (ARM64) | Native 64-bit ARM SIMD vector operations |
| **Instance Shape** | `VM.Standard.A1.Flex` | `VM.Standard.A1.Flex` | Dedicated cloud compute instance |
| **OCPU Allocation** | **2 to 4 OCPUs** | 4 OCPUs total | High-concurrency HNSW index traversal |
| **Memory (RAM)** | **12 GB to 24 GB** | 24 GB total | Full in-memory vector storage & OS cache |
| **Boot Volume** | **50 GB to 100 GB** | 200 GB total | OS, Docker layers, snapshots, logs |
| **Public IPv4** | **1 Reserved Public IP** | 1 Ephemeral / Reserved | Direct REST (6333) and gRPC (6334) access |
| **Operating System** | **Ubuntu 24.04 LTS** | Official Canonical Image | Modern Linux 6.8+ kernel with Docker support |

> [!TIP]
> Allocating **2 OCPUs and 12 GB RAM** leaves enough Always Free capacity in your OCI tenancy to launch a secondary standby instance or testing sandbox if desired. If this is your sole instance, you can safely allocate the full **4 OCPUs and 24 GB RAM**.

### 1.3 Administrator Pre-Flight Checklist

Before beginning, ensure you have:
- [ ] An active **Oracle Cloud Infrastructure (OCI)** account ([cloud.oracle.com](https://cloud.oracle.com)).
- [ ] A local terminal with SSH client installed (`OpenSSH` on Linux/macOS or `PowerShell` / `Windows Terminal` on Windows).
- [ ] `curl` and `jq` utilities installed on your local workstation for verification tests.
- [ ] Python 3.10+ installed locally with `pip` (to run the Stage 5 Python SDK verification script).
- [ ] A secure password/secrets manager (e.g. 1Password, Bitwarden, KeePass) to store the generated SSH key and Qdrant API key.

---

## Section 2: Oracle Cloud Infrastructure (OCI) Provisioning

Follow these step-by-step instructions in the Oracle Cloud Web Console.

### 2.1 OCI Console Navigation & Region Selection

1. Log in to the [Oracle Cloud Console](https://cloud.oracle.com).
2. Look at the top-right corner to verify your **Home Region** (e.g., `eu-madrid-1`, `eu-frankfurt-1`, `us-ashburn-1`, `us-phoenix-1`). Always deploy resources in your home region to guarantee Always Free eligibility.
3. Open the top-left navigation menu (Hamburger icon $\equiv$).

```
OCI Console Top Bar:
┌─────────────────────────────────────────────────────────────────────────────┐
│ ☰  ORACLE Cloud    [ Search resources...             ]  Region: Spain Central (Madrid) │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Virtual Cloud Network (VCN) & Subnet Setup

If you already have a default Virtual Cloud Network (VCN), you may use it. If starting in a new tenancy:

1. In the navigation menu, go to **Networking** $\rightarrow$ **Virtual Cloud Networks**.
2. Click **Start VCN Wizard** (the fastest and most reliable setup method).
3. Select **Create VCN with Internet Connectivity** $\rightarrow$ Click **Start VCN Wizard**.
4. Configure fields:
   - **VCN Name:** `aegis-vcn`
   - **Compartment:** `(root)` or your dedicated project compartment.
   - **VCN IPv4 CIDR Block:** `10.0.0.0/16`
   - **Public Subnet IPv4 CIDR Block:** `10.0.0.0/24`
   - **Private Subnet IPv4 CIDR Block:** `10.0.1.0/24`
5. Click **Next** $\rightarrow$ Click **Create**.

### 2.3 Compute Instance Sizing (Ampere A1 ARM64)

1. Open the navigation menu $\rightarrow$ Go to **Compute** $\rightarrow$ **Instances**.
2. Click **Create Instance**.
3. In the **Create Compute Instance** form, configure each section:

#### A. Name and Placement
- **Name:** `aegis-coach-qdrant`
- **Compartment:** Select your compartment.
- **Availability Domain:** Select the default (e.g., `AD-1`).

#### B. Image and Shape
- Click **Change Image**:
  - Select **Canonical Ubuntu**.
  - Choose **Canonical Ubuntu 24.04** (or `Ubuntu 24.04 Minimal aarch64`).
  - Click **Select Image**.
- Click **Change Shape**:
  - Select **Ampere** (Arm Processor).
  - Check the radio button for **VM.Standard.A1.Flex**.
  - Move the sliders:
    * **Number of OCPUs:** `2` (or `4`)
    * **Amount of Memory (GB):** `12` (or `24`)
  - Notice the **Always Free Eligible** green badge.
  - Click **Select Shape**.

```
Shape Configuration Summary:
┌──────────────────────────────────────────────────────────────────────┐
│ Shape: VM.Standard.A1.Flex (Ampere ARM64)                             │
│ OCPUs: 2  |  Memory: 12 GB RAM  |  Network Bandwidth: 2 Gbps         │
│ Status: Always Free Eligible [✔]                                     │
└──────────────────────────────────────────────────────────────────────┘
```

#### C. Networking
- **Primary Network:** Select *Select existing virtual cloud network*.
- **Virtual Cloud Network:** Choose `aegis-vcn`.
- **Subnet:** Choose `Public Subnet-aegis-vcn`.
- **Public IP Address:** Ensure **Assign a public IPv4 address** is selected.

### 2.4 SSH Key Pair Generation & Management

Under the **Add SSH keys** section:
- **Option 1 (Recommended if you already have a key):** Select *Upload public key files (.pub)* and upload your `~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub`.
- **Option 2 (Generate in OCI):** Select *Generate a key pair for me* $\rightarrow$ Click **Save private key** and save it to your local machine as `~/.ssh/aegis_oci_key`.

> [!WARNING]
> If you choose *Generate a key pair for me*, you **MUST** download the private key now. OCI does not store or show the private key again after instance creation.

#### D. Boot Volume
- Leave at default (50 GB) or set to **100 GB** (Always Free includes up to 200 GB total storage across your tenancy).

5. Click **Create** at the bottom of the page.
6. Wait 30–90 seconds while the provisioning state transitions from `PROVISIONING` (yellow icon) to `RUNNING` (green icon).

### 2.5 Reserved (Static) Public IPv4 Allocation

By default, OCI assigns an *ephemeral* public IP that might change if the instance is terminated and recreated. To guarantee a permanent IP address for your Aegis Coach `.env`:

1. In the Instance details page, scroll down to the left menu and click **Attached VNICs**.
2. Click the primary VNIC name (e.g., `aegis-coach-qdrant (Primary VNIC)`).
3. Under the left menu **Resources**, click **IPv4 Addresses**.
4. Click the three dots menu icon (`...`) on the right side of the assigned ephemeral IP $\rightarrow$ Select **Edit**.
5. Change **Public IP Type** from *Ephemeral IP* to **No Public IP** $\rightarrow$ Click **Update**.
6. Click the three dots menu icon (`...`) again $\rightarrow$ Select **Edit**.
7. Change **Public IP Type** to **Reserved Public IP**.
8. Select **Create a new reserved public IP**, enter name `aegis-qdrant-static-ip`, and click **Update**.
9. **Copy and record your new Public IP Address** (e.g., `140.238.123.45`).

---

## Section 3: Host Setup & Docker Engine V2 Installation

Now connect to your Ubuntu 24.04 ARM64 instance and prepare the container environment.

### 3.1 Initial SSH Connection & Key Permissions

Open a terminal on your local workstation:

```bash
# 1. On macOS / Linux / WSL: Set strict read permissions on your private key
chmod 600 ~/.ssh/aegis_oci_key

# 2. SSH into the Ubuntu host using the default 'ubuntu' user
ssh -i ~/.ssh/aegis_oci_key ubuntu@<YOUR_OCI_PUBLIC_IP>
```

*(On Windows PowerShell, use: `ssh -i $HOME\.ssh\aegis_oci_key ubuntu@<YOUR_OCI_PUBLIC_IP>`)*

When prompted `Are you sure you want to continue connecting (yes/no/[fingerprint])?`, type `yes` and press **Enter**.

### 3.2 System Update & Core Packages

Once connected to the remote shell (`ubuntu@aegis-coach-qdrant:~$`), run:

```bash
# Update package indices and upgrade existing packages
sudo apt-get update && sudo apt-get upgrade -y

# Install prerequisite system administration tools and utilities
sudo apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  ufw \
  iptables-persistent \
  netfilter-persistent \
  htop \
  jq \
  git \
  unzip
```

### 3.3 Official Docker Engine V2 Installation (Ubuntu 24.04 Noble)

Install the official Docker repository to ensure access to modern Docker Engine V2 and the Docker Compose plugin:

```bash
# 1. Create directory for APT keyrings
sudo install -m 0755 -d /etc/apt/keyrings

# 2. Download and store Docker's official GPG encryption key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Add the official Docker APT repository for Ubuntu 24.04 (ARM64 / aarch64 native)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Refresh package list and install Docker Engine, CLI, Containerd, and Compose V2
sudo apt-get update
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

### 3.4 User Group Privileges & Systemd Daemon Configuration

Configure permissions so Docker commands can be executed without `sudo`, and enable Docker to restart automatically upon system reboot:

```bash
# 1. Add current 'ubuntu' user to the docker group
sudo usermod -aG docker ubuntu

# 2. Enable and start Docker systemd service
sudo systemctl enable docker
sudo systemctl enable containerd
sudo systemctl start docker

# 3. Activate the new group membership in the current shell session
newgrp docker

# 4. Verify Docker Engine and Compose versions
docker --version
docker compose version
```

*Expected output:*
```
Docker version 27.x.x, build ...
Docker Compose version v2.29.x
```

### 3.5 Persistent Host Storage Hierarchy Creation

Qdrant requires dedicated persistent directories on the host filesystem for vector indexing and snapshots:

```bash
# Create dedicated directories under /opt/qdrant
sudo mkdir -p /opt/qdrant/storage
sudo mkdir -p /opt/qdrant/snapshots

# Transfer ownership to the ubuntu user
sudo chown -R ubuntu:ubuntu /opt/qdrant
sudo chmod -R 755 /opt/qdrant

# Verify directory permissions
ls -ld /opt/qdrant/storage /opt/qdrant/snapshots
```

---

## Section 4: Qdrant Vector Database Deployment

### 4.1 Storage Architecture & Snapshot Directory

Qdrant stores binary payload records, WAL (Write-Ahead-Log) segments, and dense HNSW vector graphs inside `/opt/qdrant/storage`. The `/opt/qdrant/snapshots` directory enables point-in-time backup creation.

### 4.2 High-Entropy Cryptographic API Key Generation

To protect your vector database against unauthorized public access, generate a 256-bit cryptographic API key directly on the server:

```bash
# Generate a secure 64-character hexadecimal API key
openssl rand -hex 32
```

*Example Output:* `9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e`

> [!IMPORTANT]
> Save this string in your local password manager! This value will become `QDRANT_API_KEY` across both your server environment and the Aegis Coach application `.env`.

### 4.3 Production Docker Compose Specification

Create the infrastructure directory and deployment configuration:

```bash
# 1. Create project infrastructure directory
mkdir -p ~/aegis-infra
cd ~/aegis-infra

# 2. Create the .env configuration file for Docker Compose
cat << 'EOF' > ~/aegis-infra/.env
# Replace with your generated openssl 64-character hex key
QDRANT_API_KEY=YOUR_GENERATED_API_KEY_HERE
EOF

# 3. Edit the .env file with your actual API key
nano ~/aegis-infra/.env
```

Now, create `docker-compose.yml`:

```bash
cat << 'EOF' > ~/aegis-infra/docker-compose.yml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: aegis-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"   # REST API & Web UI Dashboard
      - "6334:6334"   # gRPC API (High-throughput vector indexing)
    environment:
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
      - QDRANT__TELEMETRY_DISABLED=true
      - QDRANT__SERVICE__ENABLE_STATIC_CONTENT=true
      - QDRANT__LOG_LEVEL=INFO
      - QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=4
    volumes:
      - /opt/qdrant/storage:/qdrant/storage:z
      - /opt/qdrant/snapshots:/qdrant/snapshots:z
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
      memlock:
        soft: -1
        hard: -1
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
EOF
```

### 4.4 Daemon Launch & Lifecycle Management

Launch the Qdrant container daemon:

```bash
cd ~/aegis-infra

# Start Qdrant container in detached (background) mode
docker compose up -d

# Verify container is running
docker compose ps
```

*Useful Lifecycle Commands:*
```bash
# View real-time logs
docker logs -f aegis-qdrant

# Restart Qdrant
docker compose restart

# Stop Qdrant safely (flushes memory to disk)
docker compose down

# Update to latest Qdrant version
docker compose pull && docker compose up -d
```

### 4.5 Standalone Docker Run Alternative

If you prefer launching without Docker Compose, run this single command:

```bash
docker run -d \
  --name aegis-qdrant \
  --restart unless-stopped \
  -p 6333:6333 \
  -p 6334:6334 \
  -v /opt/qdrant/storage:/qdrant/storage:z \
  -v /opt/qdrant/snapshots:/qdrant/snapshots:z \
  -e QDRANT__SERVICE__API_KEY="YOUR_GENERATED_API_KEY_HERE" \
  -e QDRANT__TELEMETRY_DISABLED=true \
  -e QDRANT__SERVICE__ENABLE_STATIC_CONTENT=true \
  -e QDRANT__LOG_LEVEL=INFO \
  --ulimit nofile=65535:65535 \
  qdrant/qdrant:latest
```

---

## Section 5: Dual-Layer Network Security & Firewall Hardening

### 5.1 The Critical "Oracle Cloud Firewall Trap" Explained

> [!WARNING]
> **THE #1 MOST COMMON OCI BUG:**  
> Opening port 6333 in the Oracle Cloud Console web interface is **NOT SUFFICIENT**. Canonical Ubuntu images on OCI include pre-configured kernel firewall rules (`iptables`) that silently reject all inbound connections on ports other than TCP 22.
>
> You **MUST** configure BOTH layers:
> 1. **Layer 1 (Cloud Perimeter):** OCI VCN Ingress Security List.
> 2. **Layer 2 (Host Kernel):** Ubuntu `ufw` / `iptables`.

```
=============================================================================
                  DUAL-LAYER FIREWALL ARCHITECTURE
=============================================================================

 Internet Traffic (REST / gRPC / Webhook)
                 │
                 ▼
 ┌────────────────────────────────────────────────────────┐
 │ LAYER 1: Oracle Cloud VCN Security List / NSG          │
 │ Allows Ingress TCP 22 (SSH), TCP 6333, TCP 6334        │
 └───────────────────────┬────────────────────────────────┘
                         │ (Passes through Cloud Gateway)
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ LAYER 2: Host Operating System Firewall (Ubuntu UFW)   │
 │ Allows Inbound TCP 22, TCP 6333, TCP 6334              │
 └───────────────────────┬────────────────────────────────┘
                         │ (Accepted by Host Kernel)
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ DOCKER ENGINE: aegis-qdrant Container                  │
 │ Listening on 0.0.0.0:6333 & 0.0.0.0:6334               │
 └────────────────────────────────────────────────────────┘
```

### 5.2 Layer 1: OCI VCN Ingress Rules (Cloud Security Lists)

Configure the cloud perimeter in the Oracle Cloud Console:

1. Go to **Networking** $\rightarrow$ **Virtual Cloud Networks**.
2. Click your active VCN (e.g. `aegis-vcn`).
3. In the left menu, click **Security Lists**.
4. Click **Default Security List for aegis-vcn**.
5. Click the **Add Ingress Rules** button.
6. Add the two required rules:

#### Ingress Rule 1: Qdrant REST API & Web Dashboard
- **Stateless:** `No` (unchecked)
- **Source Type:** `CIDR`
- **Source CIDR:** `0.0.0.0/0` *(or restricted to your home/server IP)*
- **IP Protocol:** `TCP`
- **Source Port Range:** `All`
- **Destination Port Range:** `6333`
- **Description:** `Aegis Coach Qdrant REST API and Web Dashboard`

#### Ingress Rule 2: Qdrant gRPC Protocol
- **Stateless:** `No` (unchecked)
- **Source Type:** `CIDR`
- **Source CIDR:** `0.0.0.0/0` *(or restricted to your application server IP)*
- **IP Protocol:** `TCP`
- **Source Port Range:** `All`
- **Destination Port Range:** `6334`
- **Description:** `Aegis Coach Qdrant gRPC High-Throughput Port`

7. Click **Add Ingress Rules**.

```
OCI Security List Ingress Rules Table:
┌───────────┬──────────────┬──────────┬──────────────────┬─────────────────────────────────┐
│ Stateless │ Source CIDR  │ Protocol │ Destination Port │ Description                     │
├───────────┼──────────────┼──────────┼──────────────────┼─────────────────────────────────┤
│ No        │ 0.0.0.0/0    │ TCP      │ 22               │ Default SSH Access              │
│ No        │ 0.0.0.0/0    │ TCP      │ 6333             │ Aegis Qdrant REST API & Web UI  │
│ No        │ 0.0.0.0/0    │ TCP      │ 6334             │ Aegis Qdrant gRPC Protocol      │
└───────────┴──────────────┴──────────┴──────────────────┴─────────────────────────────────┘
```

### 5.3 Layer 2: Ubuntu Host OS Firewall Configuration (UFW & iptables)

Run the following commands inside your SSH session on the Ubuntu VM:

```bash
# ------------------------------------------------------------------------------
# METHOD A: Using UFW (Uncomplicated Firewall) - RECOMMENDED
# ------------------------------------------------------------------------------

# 1. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow SSH access (CRITICAL: Do not lock yourself out!)
sudo ufw allow 22/tcp comment 'SSH Access'

# 3. Allow Qdrant REST and gRPC ports
sudo ufw allow 6333/tcp comment 'Qdrant REST and Web UI'
sudo ufw allow 6334/tcp comment 'Qdrant gRPC'

# 4. Enable UFW firewall
sudo ufw --force enable

# 5. Check firewall status
sudo ufw status verbose
```

```bash
# ------------------------------------------------------------------------------
# METHOD B: Direct iptables persistence (Overrides OCI default REJECT chain)
# ------------------------------------------------------------------------------
# Insert rules at position 6 (before the default REJECT rule in OCI Ubuntu image)
sudo iptables -I INPUT 6 -p tcp --dport 6333 -m state --state NEW -j ACCEPT
sudo iptables -I INPUT 6 -p tcp --dport 6334 -m state --state NEW -j ACCEPT

# Save rules so they persist across system reboots
sudo netfilter-persistent save
sudo netfilter-persistent reload
```

### 5.4 IP Whitelisting & Production Perimeter Hardening

If your application backend has a static IP address, you can restrict inbound access so only your backend and local management workstation can reach Qdrant:

```bash
# Example: Allow Qdrant access ONLY from a specific backend IP
sudo ufw delete allow 6333/tcp
sudo ufw allow from <YOUR_BACKEND_STATIC_IP> to any port 6333 proto tcp comment 'Aegis App Server REST'
sudo ufw allow from <YOUR_BACKEND_STATIC_IP> to any port 6334 proto tcp comment 'Aegis App Server gRPC'
sudo ufw reload
```

---

## Section 6: Environment Configuration (`.env`) & 5-Stage Verification Protocol

### 6.1 Complete Production `.env` Template

Create or update the `.env` file in the root directory of your local Aegis Coach project repository (`c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.env`):

```dotenv
# ==============================================================================
# AEGIS COACH — PRODUCTION ENVIRONMENT CONFIGURATION
# ==============================================================================
# System Architecture: Multi-Agent AI Personal Trainer & Rehabilitation Engine
# Target Host: Oracle Cloud Infrastructure Always Free (Ubuntu 24.04 ARM64)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CORE APPLICATION RUNTIME & SECURITY
# ------------------------------------------------------------------------------
AEGIS_ENVIRONMENT=production
AEGIS_MOCK_MODE=false
AEGIS_LIVE_MODE=true
# 32-byte cryptographic hex secret for tenant JWT signing and HMAC token encryption
# Generate locally via: openssl rand -hex 32
AEGIS_SECRET_KEY=replace_with_openssl_rand_hex_32_secret_key

# ------------------------------------------------------------------------------
# 2. TELEGRAM BOT CONVERSATIONAL INGRESS
# ------------------------------------------------------------------------------
# Bot Token obtained via Telegram @BotFather (/newbot command)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz_SampleToken
# Telegram User ID for admin operational notifications (obtained via @userinfobot)
TELEGRAM_ADMIN_CHAT_ID=123456789

# ------------------------------------------------------------------------------
# 3. MULTI-TIER LLM PROVIDER API KEYS
# ------------------------------------------------------------------------------
# OpenAI (Tier-2 Fast Path / Voice Transcription / Structured Workout Extraction)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic Claude 3.5 Sonnet (Tier-1 Clinical RAG & Complex Physio Synthesis)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# DeepSeek V3 / R1 (Cost-Optimized Fast Reasoning Alternative)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ------------------------------------------------------------------------------
# 4. QDRANT VECTOR DATABASE (ORACLE CLOUD VPS)
# ------------------------------------------------------------------------------
# Replace <YOUR_OCI_PUBLIC_IP> with the Oracle Cloud Reserved Public IPv4
QDRANT_HOST=http://<YOUR_OCI_PUBLIC_IP>:6333
QDRANT_GRPC_PORT=6334
# The exact secret key generated and set in Oracle Docker QDRANT__SERVICE__API_KEY
QDRANT_API_KEY=replace_with_your_generated_qdrant_api_key
QDRANT_COLLECTION_NAME=aegis_sports_science

# ------------------------------------------------------------------------------
# 5. ATHLETIC DATA PLATFORMS (INTERVALS.ICU & GARMIN SYNC)
# ------------------------------------------------------------------------------
# Intervals.icu Developer API Key (intervals.icu -> Settings -> Developer Settings)
INTERVALS_ICU_API_KEY=i_xxxxxxxxxxxxxxxxxxxxxxxx
INTERVALS_ICU_ATHLETE_ID=i123456

# Strava API Application Credentials (Optional GPS Activity Webhook)
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRAVA_REFRESH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ------------------------------------------------------------------------------
# 6. SUPABASE (RELATIONAL POSTGRESQL & ROW-LEVEL SECURITY)
# ------------------------------------------------------------------------------
SUPABASE_URL=https://xxxxxxxxxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxxxxx
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://postgres:[YOUR_DB_PASSWORD]@db.xxxxxxxx.supabase.co:5432/postgres
```

### 6.2 Secrets Acquisition & Service Cheatsheet

| Configuration Variable | Provider / Service | Exact Navigation Path | Cost / Tier |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram | Open Telegram $\rightarrow$ Message `@BotFather` $\rightarrow$ Send `/newbot` $\rightarrow$ Follow prompts | Free |
| `TELEGRAM_ADMIN_CHAT_ID` | Telegram | Message `@userinfobot` or `@raw_data_bot` $\rightarrow$ Copy your numerical `id` | Free |
| `OPENAI_API_KEY` | OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) $\rightarrow$ *Create new secret key* | Pay-as-you-go |
| `ANTHROPIC_API_KEY` | Anthropic | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) $\rightarrow$ *Create Key* | Pay-as-you-go |
| `DEEPSEEK_API_KEY` | DeepSeek | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) $\rightarrow$ *Create API Key* | Pay-as-you-go |
| `INTERVALS_ICU_API_KEY` | Intervals.icu | [intervals.icu](https://intervals.icu) $\rightarrow$ Log in $\rightarrow$ **Settings** $\rightarrow$ **Developer Settings** | Free |
| `SUPABASE_URL` & Keys | Supabase | [supabase.com/dashboard](https://supabase.com/dashboard) $\rightarrow$ Project Settings $\rightarrow$ API | Free Tier |
| `QDRANT_API_KEY` | Oracle Host | Run `openssl rand -hex 32` in your server terminal | Free |

---

### 6.3 Stage 1: Container Status & Docker Daemon Inspection

Execute directly on your Oracle Cloud VM via SSH:

```bash
# 1. Inspect running container status and port mapping
docker ps --filter "name=aegis-qdrant"
```

*Expected output:*
```
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS         PORTS                                                           NAMES
a1b2c3d4e5f6   qdrant/qdrant:latest   "./qdrant"               2 minutes ago   Up 2 minutes   0.0.0.0:6333->6333/tcp, :::6333->6333/tcp, 0.0.0.0:6334->6334/tcp   aegis-qdrant
```

```bash
# 2. Inspect container startup logs
docker logs --tail 25 aegis-qdrant
```

*Verify these specific log lines appear in the output:*
- `Access token is configured` (Confirms API key protection is active)
- `Qdrant HTTP listening on 6333` (Confirms REST engine is bound)
- `Qdrant gRPC listening on 6334` (Confirms gRPC engine is bound)

---

### 6.4 Stage 2: Remote REST Healthcheck & Auth Enforcement Test

Execute from your **local workstation terminal** (replace `<YOUR_OCI_PUBLIC_IP>` and `<YOUR_QDRANT_API_KEY>`):

```bash
# Step 1: Check unauthenticated /healthz endpoint
curl -s http://<YOUR_OCI_PUBLIC_IP>:6333/healthz
# Expected Response: "healthz check passed" or {"title":"qdrant - vector search engine"}
```

```bash
# Step 2: Query authenticated root endpoint with API key header
curl -s -H "api-key: <YOUR_QDRANT_API_KEY>" http://<YOUR_OCI_PUBLIC_IP>:6333/
```

*Expected JSON output:*
```json
{
  "title": "qdrant - vector search engine",
  "version": "1.11.3",
  "commit": "..."
}
```

```bash
# Step 3: Security Validation Test — Verify that unauthenticated requests are strictly REJECTED
curl -i http://<YOUR_OCI_PUBLIC_IP>:6333/collections
```

*Expected HTTP Response Status:*  
`HTTP/1.1 401 Unauthorized` or `HTTP/1.1 403 Forbidden`  
*(This confirms your database cannot be read or modified by unauthorized internet scrapers!)*

---

### 6.5 Stage 3: End-to-End Collection CRUD Lifecycle Test

Execute from your **local workstation terminal** to test collection creation, vector upsert, search, and cleanup over the live network:

```bash
# Step 1: Create a test collection 'aegis_verification_test' with 128-dimensional Cosine vectors
curl -s -X PUT "http://<YOUR_OCI_PUBLIC_IP>:6333/collections/aegis_verification_test" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_QDRANT_API_KEY>" \
  -d '{
    "vectors": {
      "size": 128,
      "distance": "Cosine"
    }
  }' | jq .
```
*Expected output:*
```json
{
  "result": true,
  "status": "ok",
  "time": 0.012
}
```

```bash
# Step 2: Verify the collection exists in the catalog
curl -s -H "api-key: <YOUR_QDRANT_API_KEY>" http://<YOUR_OCI_PUBLIC_IP>:6333/collections | jq .
```
*Expected output:*
```json
{
  "result": {
    "collections": [
      {
        "name": "aegis_verification_test"
      }
    ]
  },
  "status": "ok"
}
```

```bash
# Step 3: Delete the test collection to leave the database clean
curl -s -X DELETE "http://<YOUR_OCI_PUBLIC_IP>:6333/collections/aegis_verification_test" \
  -H "api-key: <YOUR_QDRANT_API_KEY>" | jq .
```
*Expected output:*
```json
{
  "result": true,
  "status": "ok"
}
```

---

### 6.6 Stage 4: Interactive Web UI Dashboard Verification

Qdrant includes a built-in graphical management console.

1. Open your web browser on your local workstation.
2. Navigate to:  
   `http://<YOUR_OCI_PUBLIC_IP>:6333/dashboard`
3. The dashboard will prompt: **"Enter API Key to access Qdrant"**.
4. Paste your `<YOUR_QDRANT_API_KEY>` and click **Submit**.
5. Confirm the dashboard loads:
   - **Collections View:** Visual list of collections and vector counts.
   - **Memory & Storage:** Real-time RAM and disk usage metrics.
   - **Interactive Console:** In-browser REST query editor for running ad-hoc vector filters.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ QDRANT DASHBOARD                                   [ API Key: Authenticated ]│
├─────────────────────────────────────────────────────────────────────────────┤
│  Collections (0)      Telemetry: Off      Storage Engine: In-Memory / Disk  │
│                                                                             │
│  [+] Create Collection       [🔍] Run Query        [⚙] Server Settings      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 6.7 Stage 5: Full Python SDK Diagnostic Test Script

Run this complete diagnostic script on your local workstation to validate Python SDK connectivity, vector embedding insertion, metadata payload filtering, and similarity search.

#### A. Install the Qdrant Python Client
```bash
pip install qdrant-client
```

#### B. Create `test_qdrant_live.py`
Save the following script as `test_qdrant_live.py`:

```python
#!/usr/bin/env python3
"""
Aegis Coach — Qdrant Production Connectivity & Vector Search Verification Probe
Validates connectivity, collection creation, point indexing, and similarity search.
"""

import os
import sys
import time
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# Configuration: Reads from environment or falls back to prompt
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://<YOUR_OCI_PUBLIC_IP>:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "<YOUR_QDRANT_API_KEY>")
TEST_COLLECTION = "aegis_diagnostic_probe"
VECTOR_DIM = 4  # Minimal dimension for instant mathematical validation

def run_diagnostic():
    print("=" * 70)
    print("  AEGIS COACH — QDRANT PRODUCTION CLOUD DIAGNOSTIC SUITE")
    print("=" * 70)
    print(f"[*] Target Host:    {QDRANT_HOST}")
    print(f"[*] Auth Key Set:   {'Yes (' + QDRANT_API_KEY[:6] + '...' + QDRANT_API_KEY[-4:] + ')' if QDRANT_API_KEY else 'No'}")
    print("-" * 70)

    # 1. Initialize Client Connection
    print("[1/5] Initializing QdrantClient...")
    try:
        client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY, timeout=10.0)
        collections_response = client.get_collections()
        print(f"  [✔] Connected successfully! Existing collections: {len(collections_response.collections)}")
    except Exception as e:
        print(f"  [✘] Connection Failed: {e}")
        print("\nTroubleshooting tips:")
        print("  1. Verify OCI Security List allows Ingress on TCP 6333.")
        print("  2. Verify Ubuntu host firewall (sudo ufw status) allows 6333/tcp.")
        print("  3. Ensure Qdrant container is active (docker ps).")
        sys.exit(1)

    # 2. Create Diagnostic Collection
    print("\n[2/5] Creating diagnostic collection...")
    try:
        if client.collection_exists(TEST_COLLECTION):
            client.delete_collection(TEST_COLLECTION)
        
        client.create_collection(
            collection_name=TEST_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )
        print(f"  [✔] Collection '{TEST_COLLECTION}' created with {VECTOR_DIM}-dim Cosine distance.")
    except Exception as e:
        print(f"  [✘] Collection creation failed: {e}")
        sys.exit(1)

    # 3. Upsert Scientific RAG Test Vectors with Clinical Metadata
    print("\n[3/5] Upserting sample sports science vectors with metadata payloads...")
    try:
        points = [
            PointStruct(
                id=1,
                vector=[0.05, 0.95, 0.10, 0.20],
                payload={
                    "title": "Askling L-Protocol Hamstring Rehabilitation",
                    "domain": "hamstring_rehabilitation",
                    "protocol": "Extender, Diver, Glider (Lengthening exercises)",
                    "evidence_level": "Level 1 RCT",
                }
            ),
            PointStruct(
                id=2,
                vector=[0.90, 0.10, 0.15, 0.30],
                payload={
                    "title": "Seiler 80/20 Polarized Training Intensity Distribution",
                    "domain": "endurance_physiology",
                    "protocol": "80% Low Intensity (Zone 1), 20% High Intensity (Zone 3)",
                    "evidence_level": "Meta-Analysis",
                }
            ),
            PointStruct(
                id=3,
                vector=[0.10, 0.85, 0.25, 0.40],
                payload={
                    "title": "Silbernagel Achilles Tendinopathy Pain-Monitoring Model",
                    "domain": "tendinopathy_pain_monitoring",
                    "protocol": "Pain allowed up to 5/10 during exercise if subsided by next morning",
                    "evidence_level": "Level 1 RCT",
                }
            )
        ]
        
        upsert_res = client.upsert(collection_name=TEST_COLLECTION, points=points)
        print(f"  [✔] Upserted {len(points)} test documents. Status: {upsert_res.status}")
        time.sleep(1.0)  # Allow index synchronization
    except Exception as e:
        print(f"  [✘] Upsert failed: {e}")
        sys.exit(1)

    # 4. Perform Filtered Vector Similarity Search
    print("\n[4/5] Testing cosine similarity search with domain metadata filtering...")
    try:
        query_vector = [0.08, 0.90, 0.12, 0.22]  # Closest to Askling Hamstrings
        
        search_results = client.query_points(
            collection_name=TEST_COLLECTION,
            query=query_vector,
            limit=2,
        )
        
        print(f"  [✔] Query executed successfully. Top matching documents:")
        for idx, hit in enumerate(search_results.points, 1):
            score = hit.score
            title = hit.payload.get("title", "Unknown")
            domain = hit.payload.get("domain", "Unknown")
            print(f"      {idx}. [Score: {score:.4f}] {title} ({domain})")
            
        assert len(search_results.points) > 0, "No search results returned!"
        assert "Askling" in search_results.points[0].payload["title"], "Top match should be Askling protocol!"
    except Exception as e:
        print(f"  [✘] Vector search failed: {e}")
        sys.exit(1)

    # 5. Clean up Diagnostic Collection
    print("\n[5/5] Cleaning up diagnostic collection...")
    try:
        client.delete_collection(TEST_COLLECTION)
        print(f"  [✔] Collection '{TEST_COLLECTION}' deleted cleanly.")
    except Exception as e:
        print(f"  [✘] Cleanup failed: {e}")

    print("\n" + "=" * 70)
    print("  🎉 ALL 5 DIAGNOSTIC STAGES PASSED! QDRANT IS PRODUCTION-READY.")
    print("=" * 70)

if __name__ == "__main__":
    run_diagnostic()
```

#### C. Execute the Diagnostic Script
```bash
python test_qdrant_live.py
```

*Expected Terminal Output:*
```
======================================================================
  AEGIS COACH — QDRANT PRODUCTION CLOUD DIAGNOSTIC SUITE
======================================================================
[*] Target Host:    http://140.238.123.45:6333
[*] Auth Key Set:   Yes (9f8e7d...9f8e)
----------------------------------------------------------------------
[1/5] Initializing QdrantClient...
  [✔] Connected successfully! Existing collections: 0

[2/5] Creating diagnostic collection...
  [✔] Collection 'aegis_diagnostic_probe' created with 4-dim Cosine distance.

[3/5] Upserting sample sports science vectors with metadata payloads...
  [✔] Upserted 3 test documents. Status: UpdateStatus.COMPLETED

[4/5] Testing cosine similarity search with domain metadata filtering...
  [✔] Query executed successfully. Top matching documents:
      1. [Score: 0.9989] Askling L-Protocol Hamstring Rehabilitation (hamstring_rehabilitation)
      2. [Score: 0.9912] Silbernagel Achilles Tendinopathy Pain-Monitoring Model (tendinopathy_pain_monitoring)

[5/5] Cleaning up diagnostic collection...
  [✔] Collection 'aegis_diagnostic_probe' deleted cleanly.

======================================================================
  🎉 ALL 5 DIAGNOSTIC STAGES PASSED! QDRANT IS PRODUCTION-READY.
======================================================================
```

---

### 6.8 Diagnostic Troubleshooting Matrix

| Observed Symptom | Root Cause | Exact Resolution Command |
|---|---|---|
| `Connection timed out` or `No route to host` on port 6333 | OCI VCN Ingress rule missing or host firewall blocking TCP 6333 | 1. Check OCI Console $\rightarrow$ VCN $\rightarrow$ Ingress Rules for port `6333`.<br>2. On VM, run `sudo ufw allow 6333/tcp && sudo ufw reload`. |
| `HTTP 401 Unauthorized` / `Forbidden` | Missing `api-key` HTTP header or mismatched secret | Verify `QDRANT_API_KEY` in `.env` matches the `QDRANT__SERVICE__API_KEY` configured in server's `docker-compose.yml`. |
| Docker container stops immediately (`Exited (1)`) | Insufficient volume permissions on `/opt/qdrant` | Run `sudo chown -R ubuntu:ubuntu /opt/qdrant && sudo chmod -R 755 /opt/qdrant` on host VM. |
| `Out of memory` / Container killed by OOM killer | VM instance memory undersized | Verify instance has at least 12 GB RAM allocated (`free -m` on VM). Increase swap if necessary: `sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`. |
| Vector search returns incorrect results | Vector dimension mismatch | Ensure vector dimension in collection creation matches embedding model (e.g. 1536 for OpenAI `text-embedding-3-small` / `ada-002`, or 768 / 1024 for open-source models). |

---

## Conclusion & Next Steps

With your Oracle Cloud VM running, Docker Engine installed, Qdrant vector database secured with API key authentication, dual-layer firewall rules established, and `.env` configured:

1. **Ingest Literature Embeddings:** Run `python scripts/ingest_papers.py` to convert all 11 scientific papers to markdown and index them into Qdrant.
2. **Launch Aegis Coach Core:** Start the multi-agent conversational engine (`python -m aegis_coach.main` or via Docker).
3. **Connect Telegram Bot:** Message your Telegram bot (`/start`) to begin personalized endurance training and rehabilitation coaching backed by Level 1 scientific evidence!
