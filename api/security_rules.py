# api/security_rules.py
import re

# LAYER 1: Known Malicious IP Threat Intel (Mocked Database)
BLACKLISTED_IPS = {
    "192.168.1.100",
    "10.0.0.55",
    "203.0.113.42",
    "185.15.59.22" # Common Botnet subnet
}

# LAYER 2: Bad User-Agent Detection
# Blocks known automated scraping tools and botnets before AI processing
BAD_USER_AGENTS = [
    "curl", "wget", "python-requests", "java", 
    "nmap", "sqlmap", "nikto", "dirbuster"
]

# LAYER 3: Advanced Military-Grade Static WAF Rules (Regular Expressions)
STATIC_RULES = [
    re.compile(r"(?i)(<script>.*?</script>|<img.*?onerror=.*?>)"),          # Advanced XSS
    re.compile(r"(?i)(UNION\s+SELECT|DROP\s+TABLE|OR\s+1=1|--\s*$)"),        # Advanced SQLi
    re.compile(r"(?i)(/etc/passwd|/bin/sh|\.\./\.\./)"),                     # Directory Traversal / RCE
    re.compile(r"(?i)(eval\(|base64_decode\(|system\()"),                    # Code Injection
    re.compile(r"(?i)(System Override:|Ignore all previous instructions)"),  # Hardcoded LLM Prompts
]

def check_static_rules(ip_address: str, payload: str, user_agent: str = "") -> dict:
    """
    Zero-Trust Static Filter: Runs BEFORE the AI Fusion Engine.
    Saves massive GPU/CPU power by blocking obvious threats instantly.
    """
    # 1. Check IP Blacklist
    if ip_address in BLACKLISTED_IPS:
        return {"blocked": True, "reason": "[STATIC WAF] IP Address is in the Global Threat Intel Blacklist."}

    # 2. Check User-Agent (Bot mitigation)
    if user_agent:
        ua_lower = user_agent.lower()
        if any(bad_bot in ua_lower for bad_bot in BAD_USER_AGENTS):
            return {"blocked": True, "reason": f"[STATIC WAF] Automated Bot/Scraper User-Agent detected."}

    # 3. Check advanced signature-based payloads
    if payload:
        for rule in STATIC_RULES:
            if rule.search(payload):
                return {"blocked": True, "reason": "[STATIC WAF] Known Malicious Signature matched (Heuristics)."}

    return {"blocked": False, "reason": "Passed Static Checks"}