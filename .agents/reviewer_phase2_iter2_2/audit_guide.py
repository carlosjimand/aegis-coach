import re
from pathlib import Path

guide_path = Path("mvp_next_steps.md")
content = guide_path.read_text(encoding="utf-8")

checks = {
    "OCI Instance Shape (VM.Standard.A1.Flex)": r"VM\.Standard\.A1\.Flex",
    "Ubuntu 24.04 noble": r"Ubuntu\s+24\.04",
    "Docker Engine V2 install commands": r"download\.docker\.com/linux/ubuntu",
    "Qdrant Port 6333": r"6333",
    "Qdrant Port 6334": r"6334",
    "Qdrant API Key Env Var": r"QDRANT__SERVICE__API_KEY",
    "Docker Compose YAML block": r"services:\s*\n\s*qdrant:",
    "OCI VCN Ingress Rules": r"Ingress\s+Rule|Security\s+List",
    "UFW firewall commands": r"ufw\s+allow\s+6333",
    "iptables / netfilter-persistent commands": r"iptables.*6333.*ACCEPT",
    "Stage 1 Container verification": r"Stage\s*1.*Container|docker\s+ps",
    "Stage 2 REST healthcheck": r"Stage\s*2.*REST|curl.*6333/healthz",
    "Stage 3 Collection CRUD": r"Stage\s*3.*CRUD|PUT.*collections",
    "Stage 4 Web UI Dashboard": r"Stage\s*4.*Dashboard|http://.*6333/dashboard",
    "Stage 5 Python SDK verification": r"Stage\s*5.*Python|QdrantClient",
    "Complete .env template": r"TELEGRAM_BOT_TOKEN.*OPENAI_API_KEY.*QDRANT_API_KEY",
}

print(f"--- MVP Next Steps Guide Audit ---")
print(f"Total Lines: {len(content.splitlines())}, Total Bytes: {len(content)}")
all_pass = True
for label, pattern in checks.items():
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    status = "PASS" if match else "FAIL"
    if not match:
        all_pass = False
    print(f"[{status}] {label}")

print(f"\nOverall Guide Completeness: {'PASS' if all_pass else 'FAIL'}")
