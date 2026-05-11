#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  C Y B E R T O O L K I T  v2.0  —  by bash & jerry                 ║
║  Terminal-native · Matrix-aesthetic · Educational use only          ║
╚══════════════════════════════════════════════════════════════════════╝

Dependencies:
    pip install requests dnspython colorama
"""

import os, sys, time, socket, hashlib, re, threading, random, string
import subprocess, json, struct
from datetime import datetime
from collections import defaultdict

# ── optional deps ──────────────────────────────────────────────────────
try:
    import requests; HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import dns.resolver; HAS_DNS = True
except ImportError:
    HAS_DNS = False

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()

# ── colour palette ────────────────────────────────────────────────────
G  = Fore.GREEN
GB = Fore.GREEN  + Style.BRIGHT
C  = Fore.CYAN
CB = Fore.CYAN   + Style.BRIGHT
Y  = Fore.YELLOW
YB = Fore.YELLOW + Style.BRIGHT
R  = Fore.RED    + Style.BRIGHT
W  = Fore.WHITE  + Style.BRIGHT
DIM= Style.DIM
RST= Style.RESET_ALL
MAG= Fore.MAGENTA + Style.BRIGHT

MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF<>/|\\!@#$%^&*"

# ═══════════════════════════════════════════════════════════════════════
#  TERMINAL HELPERS
# ═══════════════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def ts():
    return datetime.now().strftime("%H:%M:%S")

def slow_print(text, delay=0.012, color=""):
    for ch in text:
        print(color + ch, end="", flush=True)
        time.sleep(delay)
    print(RST)

def glitch_print(text, color=GB):
    """Print text with a glitch/scramble animation then reveal."""
    chars = list(text)
    width = len(text)
    for _ in range(8):
        glitched = "".join(
            random.choice(MATRIX_CHARS) if random.random() < 0.4 else c
            for c in chars
        )
        print(f"\r{color}{glitched}{RST}", end="", flush=True)
        time.sleep(0.04)
    print(f"\r{color}{text}{RST}")

def matrix_rain(lines=6, width=72, duration=0.04):
    """Print a short burst of matrix rain."""
    for _ in range(lines):
        row = "".join(
            random.choice(MATRIX_CHARS) if random.random() > 0.7 else " "
            for _ in range(width)
        )
        density = random.random()
        if density > 0.8:
            print(GB + row)
        elif density > 0.5:
            print(G  + row)
        else:
            print(DIM + G + row)
        time.sleep(duration)
    print(RST, end="")

def spinner(stop_event, msg=""):
    frames = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    i = 0
    while not stop_event.is_set():
        print(f"\r{CB}[{frames[i % len(frames)]}]{RST} {G}{msg}{RST}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print(f"\r{' '*(len(msg)+6)}\r", end="", flush=True)

def box(title, width=70):
    bar  = "═" * (width - 4)
    side = "║"
    pad  = (width - 4 - len(title)) // 2
    print(f"\n{GB}╔{bar}╗")
    print(f"{side}{' '*pad}{CB}{title}{GB}{' '*(width-4-pad-len(title))}{side}")
    print(f"╚{bar}╝{RST}")

def hr(width=70, char="─", color=None):
    c = color or DIM + G
    print(c + char * width + RST)

def ok(msg):   print(f"  {GB}[✔]{RST} {G}{msg}{RST}")
def warn(msg): print(f"  {YB}[!]{RST} {Y}{msg}{RST}")
def err(msg):  print(f"  {R}[✗]{RST} {R}{msg}{RST}")
def info(msg): print(f"  {CB}[~]{RST} {C}{msg}{RST}")
def find(msg): print(f"  {MAG}[★]{RST} {MAG}{msg}{RST}")

def progress_bar(done, total, width=40, label=""):
    pct   = done / total if total else 0
    filled= int(pct * width)
    bar   = G + "█" * filled + DIM + G + "░" * (width - filled) + RST
    print(f"\r  [{bar}] {GB}{pct*100:5.1f}%{RST} {DIM}{label}{RST}", end="", flush=True)

def prompt(msg, default=""):
    val = input(f"\n{CB}  ╠══>{RST} {G}{msg}{RST} {DIM}[{default}]{RST}: ").strip()
    return val if val else default

def confirm(msg):
    ans = input(f"\n{YB}  [?]{RST} {Y}{msg}{RST} {DIM}(y/N){RST}: ").strip().lower()
    return ans == "y"

# ═══════════════════════════════════════════════════════════════════════
#  BOOT SEQUENCE
# ═══════════════════════════════════════════════════════════════════════

BANNER = r"""
  ██████╗██╗   ██╗██████╗ ███████╗██████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

def boot_sequence():
    clear()
    matrix_rain(lines=5, width=72, duration=0.025)
    print(GB + BANNER + RST)
    slow_print("         T O O L K I T   v 2 . 0   [ T E R M I N A L   E D I T I O N ]", 0.018, CB)
    print()
    slow_print("  ⚠  FOR AUTHORISED / EDUCATIONAL USE ONLY — bash & jerry", 0.01, YB)
    hr()

    boot_msgs = [
        "Initialising core modules",
        "Loading cryptographic engine",
        "Spawning thread pool",
        "Checking optional dependencies",
        "Calibrating network stack",
        "System ready",
    ]
    for msg in boot_msgs:
        dots = random.randint(2, 5)
        line = f"  {G}[{ts()}]{RST} {DIM}{msg}{'.' * dots}{RST}"
        print(line)
        time.sleep(random.uniform(0.07, 0.18))

    dep_r  = f"{GB}requests:✔{RST}" if HAS_REQUESTS else f"{R}requests:✘{RST}"
    dep_d  = f"{GB}dnspython:✔{RST}" if HAS_DNS      else f"{R}dnspython:✘{RST}"
    dep_c  = f"{GB}colorama:✔{RST}"  if HAS_COLOR     else f"{Y}colorama:✘{RST}"
    print(f"\n  {DIM}deps ─{RST} {dep_r}  {dep_d}  {dep_c}\n")
    time.sleep(0.4)


# ═══════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════════

MENU = [
    ("PORT SCANNER",       "Scan open TCP ports with banner grabbing"),
    ("PACKET SNIFFER",     "Capture live traffic via tcpdump/raw socket"),
    ("PASSWORD ANALYSER",  "Strength check + crack-time estimates + generator"),
    ("HASH LAB",           "Hash text/files · dictionary crack"),
    ("IP / DOMAIN OSINT",  "Resolve · GeoIP · WHOIS · DNS · HTTP headers"),
    ("SUBDOMAIN SCANNER",  "Brute-force subdomains via DNS resolution"),
    ("VULNERABILITY SCAN", "HTTP security headers · SSL · CORS · path enum"),
    ("NETWORK RECON",      "ARP sweep · traceroute · latency map  [NEW]"),
    ("CIPHER TOOLKIT",     "Encode/decode Base64 · ROT13 · XOR · Caesar  [NEW]"),
    ("SYSTEM AUDIT",       "Local OS info · listening ports · users · env  [NEW]"),
]

def main_menu():
    while True:
        matrix_rain(lines=2, width=72, duration=0.015)
        box("CYBERTOOLKIT v2.0 — MAIN MENU")
        print()
        for i, (name, desc) in enumerate(MENU, 1):
            idx   = f"{CB}[{i:02d}]{RST}"
            label = f"{GB}{name:<26}{RST}"
            dsc   = f"{DIM}{desc}{RST}"
            print(f"  {idx}  {label}  {dsc}")
        print()
        info("Type a number to select a module, or 'q' to quit.")
        hr()
        choice = input(f"\n{CB}  ╠══> SELECT MODULE {RST}").strip().lower()
        if choice in ("q","quit","exit"):
            farewell(); break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MENU):
                MODULE_MAP[idx]()
            else:
                err("Invalid selection.")
        except ValueError:
            err("Enter a number.")

def farewell():
    clear()
    matrix_rain(lines=8, width=72, duration=0.02)
    slow_print("\n  DISCONNECTING FROM THE MATRIX…\n", 0.025, GB)
    time.sleep(0.3)


# ═══════════════════════════════════════════════════════════════════════
#  1. PORT SCANNER
# ═══════════════════════════════════════════════════════════════════════
COMMON_PORTS = [21,22,23,25,53,80,110,111,135,139,143,
                443,445,993,995,1723,3306,3389,5900,8080,8443]

def module_port_scanner():
    box("MODULE 01 — PORT SCANNER")
    host       = prompt("Target host", "scanme.nmap.org")
    use_common = confirm("Scan common ports only (21 common ports)?")
    if use_common:
        ports = COMMON_PORTS
    else:
        start = int(prompt("Start port", "1"))
        end   = int(prompt("End port",   "1024"))
        ports = list(range(start, end + 1))
    threads  = int(prompt("Threads", "150"))
    timeout  = float(prompt("Timeout (s)", "0.5"))
    banner   = confirm("Attempt banner grab?")

    print()
    stop_ev = threading.Event()
    spin_t  = threading.Thread(target=spinner, args=(stop_ev, f"Resolving {host}…"), daemon=True)
    spin_t.start()
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        stop_ev.set(); err(f"DNS failed: {e}"); return
    stop_ev.set()

    hr()
    info(f"TARGET : {host}  ({ip})")
    info(f"PORTS  : {len(ports)}  |  THREADS: {threads}  |  TIMEOUT: {timeout}s")
    hr()
    print()

    open_ports = []
    done       = [0]
    total      = len(ports)
    sem        = threading.Semaphore(threads)
    lock       = threading.Lock()

    def probe(p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            if s.connect_ex((ip, p)) == 0:
                bstr = ""
                if banner:
                    try:
                        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                        bstr = s.recv(128).decode(errors="replace").split("\n")[0].strip()[:60]
                    except: pass
                with lock:
                    open_ports.append(p)
                    svc = _svc(p)
                    print(f"\r  {MAG}[OPEN]{RST}  {GB}{p:<6}{RST}  {C}{svc:<18}{RST}  {DIM}{bstr}{RST}")
            s.close()
        except: pass
        finally:
            with lock:
                done[0] += 1
                progress_bar(done[0], total, label=f"{done[0]}/{total}")
            sem.release()

    threads_list = []
    for p in ports:
        sem.acquire()
        t = threading.Thread(target=probe, args=(p,), daemon=True)
        threads_list.append(t); t.start()
    for t in threads_list: t.join()

    print()
    hr()
    find(f"SCAN COMPLETE — {len(open_ports)} open port(s) found out of {total} scanned.")
    hr()
    input(f"\n{DIM}  Press ENTER to return…{RST}")

def _svc(p):
    try: return socket.getservbyport(p)
    except: return "unknown"


# ═══════════════════════════════════════════════════════════════════════
#  2. PACKET SNIFFER
# ═══════════════════════════════════════════════════════════════════════

def module_packet_sniffer():
    box("MODULE 02 — PACKET SNIFFER")
    warn("Requires root/admin. Uses tcpdump or raw socket fallback.")
    iface = prompt("Interface", "eth0")
    filt  = prompt("tcpdump filter", "tcp port 80 or tcp port 443")
    limit = int(prompt("Packet limit", "50"))
    print()

    counts = defaultdict(int)

    def count_line(line):
        ll = line.lower()
        if "tcp" in ll:   counts["TCP"] += 1
        elif "udp" in ll: counts["UDP"] += 1
        else:             counts["OTHER"] += 1
        counts["total"] += 1

    stop_flag = [False]

    def print_stats():
        print(f"  {CB}packets:{RST} {counts['total']}  "
              f"{G}TCP:{counts['TCP']}  {Y}UDP:{counts['UDP']}  "
              f"{DIM}OTHER:{counts['OTHER']}{RST}")

    hr()
    # Try tcpdump
    try:
        cmd = ["tcpdump", "-i", iface, "-n", "-l", "-c", str(limit), filt]
        info(f"CMD: {' '.join(cmd)}")
        print()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        for line in proc.stdout:
            if stop_flag[0]: proc.terminate(); break
            count_line(line)
            proto = "TCP" if "tcp" in line.lower() else "UDP" if "udp" in line.lower() else "OTH"
            col   = G if proto=="TCP" else Y if proto=="UDP" else DIM+G
            print(f"  {CB}[{ts()}]{RST} {col}{line.rstrip()}{RST}")
        proc.wait()
    except FileNotFoundError:
        warn("tcpdump not found — falling back to raw socket…")
        try:
            import struct
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            info(f"Raw socket open — capturing {limit} packets")
            print()
            for n in range(1, limit+1):
                raw, addr = s.recvfrom(65535)
                proto_id = raw[23] if len(raw) > 23 else 0
                proto = {6:"TCP",17:"UDP"}.get(proto_id,"OTHER")
                counts[proto] += 1; counts["total"] += 1
                col = G if proto=="TCP" else Y if proto=="UDP" else DIM+G
                print(f"  {CB}#{n:<4}{RST} {col}{proto:<6}{RST}  src={addr[0]:<18}  len={len(raw)}")
            s.close()
        except PermissionError:
            err("Permission denied — run as root/sudo.")
        except Exception as e:
            err(f"Raw socket error: {e}")
    except PermissionError:
        err("Permission denied — run as root/sudo.")

    print()
    hr()
    print_stats()
    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  3. PASSWORD ANALYSER
# ═══════════════════════════════════════════════════════════════════════

def module_password():
    box("MODULE 03 — PASSWORD ANALYSER")
    while True:
        pw = input(f"\n{CB}  ╠══> Enter password (blank to quit){RST}: ")
        if not pw: break

        import math
        checks = {
            "Length ≥ 8":        len(pw) >= 8,
            "Length ≥ 12":       len(pw) >= 12,
            "Length ≥ 16":       len(pw) >= 16,
            "Uppercase letter":  bool(re.search(r"[A-Z]", pw)),
            "Lowercase letter":  bool(re.search(r"[a-z]", pw)),
            "Digit":             bool(re.search(r"\d",    pw)),
            "Symbol":            bool(re.search(r"[^a-zA-Z0-9]", pw)),
            "No common words":   not any(w in pw.lower() for w in
                                         ["password","123456","qwerty","admin","letmein"]),
            "No char repeat >3": not re.search(r"(.)\1{3,}", pw),
        }

        def charset(p):
            c = 0
            if re.search(r"[a-z]",p): c+=26
            if re.search(r"[A-Z]",p): c+=26
            if re.search(r"\d",p):    c+=10
            if re.search(r"[^a-zA-Z0-9]",p): c+=32
            return c or 1

        cs      = charset(pw)
        entropy = len(pw) * math.log2(cs) if cs else 0
        score   = sum(checks.values())
        pct     = score / len(checks)

        if pct < 0.3:   label,col = "CRITICAL", R
        elif pct < 0.5: label,col = "WEAK",     Y
        elif pct < 0.7: label,col = "FAIR",     YB
        elif pct < 0.9: label,col = "STRONG",   GB
        else:           label,col = "EXCELLENT", MAG

        print()
        hr()
        info(f"Length    : {len(pw)}")
        info(f"Charset   : {cs}")
        info(f"Entropy   : {entropy:.1f} bits")
        bar_w = 40
        filled = int(pct * bar_w)
        bar = col + "█"*filled + DIM+G + "░"*(bar_w-filled) + RST
        print(f"\n  STRENGTH  [{bar}]  {col}{label}{RST}\n")

        for name, passed in checks.items():
            if passed: ok(name)
            else:      err(name)

        def ht(s):
            if s<1:       return "< 1 second"
            if s<60:      return f"{s:.0f} seconds"
            if s<3600:    return f"{s/60:.0f} minutes"
            if s<86400:   return f"{s/3600:.1f} hours"
            if s<31536000:return f"{s/86400:.1f} days"
            if s<3.15e10: return f"{s/31536000:.1f} years"
            return "centuries"

        print()
        info("Crack time estimates:")
        for rate, lbl in [(1e6,"online (1M/s)"),(1e9,"fast hash (1B/s)"),(1e12,"GPU (1T/s)")]:
            secs = (cs ** len(pw)) / rate
            print(f"    {DIM}{lbl:<28}{RST}  {C}{ht(secs)}{RST}")
        hr()

    # Generator
    if confirm("Generate a strong password?"):
        length = int(prompt("Length", "24"))
        chars  = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pw = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        print(f"\n  {GB}GENERATED:{RST}  {YB}{pw}{RST}\n")
    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  4. HASH LAB
# ═══════════════════════════════════════════════════════════════════════
ALGOS = ["md5","sha1","sha224","sha256","sha384","sha512",
         "sha3_256","sha3_512","blake2b","blake2s"]

def module_hash_lab():
    box("MODULE 04 — HASH LAB")
    while True:
        print(f"\n  {CB}[1]{RST} Hash text    {CB}[2]{RST} Hash file    {CB}[3]{RST} Dictionary crack    {CB}[q]{RST} Back")
        ch = input(f"\n{CB}  ╠══>{RST} ").strip().lower()
        if ch in ("q",""):
            break
        elif ch == "1":
            txt  = prompt("Input text", "hello")
            algo = prompt("Algorithm", "sha256")
            try:
                h = hashlib.new(algo, txt.encode()).hexdigest()
                print(f"\n  {CB}[{algo.upper()}]{RST}  {YB}{h}{RST}\n")
            except Exception as e:
                err(str(e))

        elif ch == "2":
            path = prompt("File path", "")
            if not path or not os.path.isfile(path):
                err("File not found."); continue
            algo = prompt("Algorithm", "sha256")
            try:
                h = hashlib.new(algo)
                with open(path,"rb") as f:
                    for chunk in iter(lambda: f.read(65536), b""):
                        h.update(chunk)
                print(f"\n  {CB}[{algo.upper()}]{RST}  {os.path.basename(path)}")
                print(f"  {YB}{h.hexdigest()}{RST}\n")
            except Exception as e:
                err(str(e))

        elif ch == "3":
            target = prompt("Target hash", "").strip().lower()
            algo   = prompt("Algorithm",   "md5")
            wl_path= prompt("Wordlist path (blank = built-in)", "")
            if wl_path and os.path.isfile(wl_path):
                with open(wl_path,"r",errors="replace") as f:
                    words = [l.strip() for l in f]
            else:
                words = ["password","123456","admin","letmein","qwerty","abc123",
                         "password1","iloveyou","sunshine","monkey","dragon","master",
                         "hello","welcome","test","root","toor","pass","1234","12345",
                         "superman","batman","trustno1","shadow","football"]
                warn(f"Using {len(words)} built-in words.")

            hr()
            info(f"Target: {target}  |  algo: {algo}  |  words: {len(words)}")
            found = False
            for i, word in enumerate(words):
                try:
                    h = hashlib.new(algo, word.encode()).hexdigest()
                except: break
                if i % 2000 == 0:
                    progress_bar(i, len(words), label=word[:20])
                if h == target:
                    print()
                    find(f"CRACKED → '{word}'")
                    found = True; break
            print()
            if not found:
                warn("Not found in wordlist.")
            hr()

    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  5. IP / DOMAIN OSINT
# ═══════════════════════════════════════════════════════════════════════

def module_osint():
    box("MODULE 05 — IP / DOMAIN OSINT")
    target = prompt("Target (IP or domain)", "google.com")
    print()
    hr()

    # IP resolve
    print(f"\n  {CB}► IP RESOLUTION{RST}")
    try:
        ip = socket.gethostbyname(target)
        ok(f"IPv4 : {ip}")
        try:
            infos = socket.getaddrinfo(target, None)
            for v6 in {i[4][0] for i in infos if ":" in i[4][0]}:
                ok(f"IPv6 : {v6}")
        except: pass
    except Exception as e:
        err(str(e)); ip = None

    # Reverse DNS
    print(f"\n  {CB}► REVERSE DNS{RST}")
    if ip:
        try:
            ok(f"PTR : {socket.gethostbyaddr(ip)[0]}")
        except Exception as e:
            warn(str(e))

    # GeoIP
    print(f"\n  {CB}► GEO-IP  (ip-api.com){RST}")
    if ip and HAS_REQUESTS:
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=6).json()
            for k in ["country","regionName","city","isp","org","as","lat","lon"]:
                if r.get(k): info(f"{k:<16}: {r[k]}")
        except Exception as e:
            warn(str(e))
    elif not HAS_REQUESTS:
        warn("requests not installed (pip install requests)")

    # HTTP headers
    print(f"\n  {CB}► HTTP HEADERS{RST}")
    import urllib.request, ssl
    for scheme in ["https","http"]:
        try:
            req = urllib.request.Request(
                f"{scheme}://{target}", method="HEAD",
                headers={"User-Agent":"CyberToolkit/2.0"})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
                ok(f"Status : {resp.status} {scheme.upper()}")
                for k,v in list(resp.headers.items())[:14]:
                    info(f"{k:<28}: {v}")
            break
        except Exception as e:
            warn(f"{scheme}: {e}")

    # DNS records
    print(f"\n  {CB}► DNS RECORDS{RST}")
    if HAS_DNS:
        for rtype in ["A","AAAA","MX","NS","TXT","SOA"]:
            try:
                for rd in dns.resolver.resolve(target, rtype, lifetime=5):
                    ok(f"{rtype:<8} {rd}")
            except: pass
    else:
        warn("dnspython not installed (pip install dnspython)")

    # WHOIS
    print(f"\n  {CB}► WHOIS (raw){RST}")
    try:
        domain = target.lstrip("www.").strip()
        s = socket.socket(); s.settimeout(8)
        s.connect(("whois.iana.org", 43))
        s.send((domain + "\r\n").encode())
        resp = b""
        while True:
            d = s.recv(4096)
            if not d: break
            resp += d
        s.close()
        for line in resp.decode(errors="replace").splitlines()[:30]:
            print(f"  {DIM}{line}{RST}")
    except Exception as e:
        warn(str(e))

    hr()
    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  6. SUBDOMAIN SCANNER
# ═══════════════════════════════════════════════════════════════════════
SUB_WORDLIST = [
    "www","mail","ftp","smtp","pop","ns1","ns2","webmail","admin","portal",
    "api","dev","staging","test","vpn","remote","secure","shop","blog",
    "static","cdn","img","images","media","assets","m","mobile","app",
    "dashboard","panel","cpanel","support","help","docs","wiki","status",
    "internal","intranet","cloud","git","gitlab","jenkins","jira","confluence",
    "auth","login","sso","owa","exchange","mx","mx1","mx2","ns3","ns4",
    "beta","old","new","v1","v2","api2","data","backup","db","database",
    "ldap","radius","proxy","firewall","router","switch","storage","nas",
]

def module_subdomain():
    box("MODULE 06 — SUBDOMAIN SCANNER")
    domain   = prompt("Target domain", "example.com")
    threads  = int(prompt("Threads", "30"))
    wl_path  = prompt("Custom wordlist (blank = built-in)", "")
    if wl_path and os.path.isfile(wl_path):
        with open(wl_path,"r",errors="replace") as f:
            words = [l.strip() for l in f if l.strip()]
    else:
        words = SUB_WORDLIST

    print()
    hr()
    info(f"Domain: {domain}  |  wordlist: {len(words)} entries  |  threads: {threads}")
    hr()
    print()

    found  = [0]
    done   = [0]
    total  = len(words)
    sem    = threading.Semaphore(threads)
    lock   = threading.Lock()

    def probe(sub):
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            with lock:
                found[0] += 1
                print(f"\r  {MAG}[+]{RST}  {GB}{fqdn:<50}{RST}  {C}{ip}{RST}")
        except: pass
        finally:
            with lock:
                done[0] += 1
                progress_bar(done[0], total, label=f"{done[0]}/{total}")
            sem.release()

    thread_list = []
    for w in words:
        sem.acquire()
        t = threading.Thread(target=probe, args=(w,), daemon=True)
        thread_list.append(t); t.start()
    for t in thread_list: t.join()

    print()
    hr()
    find(f"DONE — {found[0]} subdomain(s) resolved out of {total} tested.")
    hr()
    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  7. VULNERABILITY SCANNER
# ═══════════════════════════════════════════════════════════════════════

def _vuln_fetch(url, method="GET", extra_headers=None, timeout=8):
    import urllib.request, ssl
    headers = {"User-Agent": "CyberToolkit/2.0", **(extra_headers or {})}
    req = urllib.request.Request(url, method=method, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.status, dict(r.headers), r.read(4096).decode(errors="replace")

def module_vuln_scan():
    box("MODULE 07 — VULNERABILITY SCANNER")
    warn("For authorised penetration testing only.")
    url = prompt("Target URL", "http://testphp.vulnweb.com")
    print()

    checks = [
        ("Security Headers",      _vuln_sec_headers),
        ("Server Banner Leakage", _vuln_banner),
        ("SSL/TLS Info",          _vuln_ssl),
        ("Clickjacking",          _vuln_clickjack),
        ("CORS Misconfiguration", _vuln_cors),
        ("Sensitive Paths",       _vuln_paths),
        ("HTTP Methods",          _vuln_methods),
    ]

    for i, (name, fn) in enumerate(checks, 1):
        print(f"\n  {CB}[{i}/{len(checks)}]{RST}  {GB}{name}{RST}")
        hr(60, "·")
        try:
            fn(url)
        except Exception as e:
            err(f"Error: {e}")

    hr()
    find("Scan complete.")
    input(f"\n{DIM}  Press ENTER to return…{RST}")

def _vuln_sec_headers(url):
    REQUIRED = {
        "Strict-Transport-Security": "HSTS not set",
        "X-Content-Type-Options":    "X-Content-Type-Options missing",
        "X-Frame-Options":           "Clickjacking protection missing",
        "Content-Security-Policy":   "CSP not set",
        "Referrer-Policy":           "Referrer-Policy not set",
    }
    status, hdrs, _ = _vuln_fetch(url)
    info(f"HTTP {status}")
    for h, msg in REQUIRED.items():
        v = hdrs.get(h) or hdrs.get(h.lower())
        if v: ok(f"{h}: {v}")
        else: warn(f"MISSING — {msg}")

def _vuln_banner(url):
    _, hdrs, _ = _vuln_fetch(url)
    for h in ["Server","X-Powered-By","X-AspNet-Version","X-Generator"]:
        v = hdrs.get(h) or hdrs.get(h.lower())
        if v: warn(f"{h}: {v}  ← version disclosure")
        else: ok(f"{h}: not disclosed")

def _vuln_ssl(url):
    if not url.startswith("https"):
        warn("Not HTTPS — traffic unencrypted"); return
    import ssl
    host = url.split("//")[1].split("/")[0].split(":")[0]
    ctx  = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.create_connection((host,443),5), server_hostname=host) as s:
            ok(f"TLS    : {s.version()}")
            ok(f"Cipher : {s.cipher()[0]}")
            cert = s.getpeercert()
            if cert:
                ok(f"Expires: {cert.get('notAfter')}")
    except ssl.SSLCertVerificationError as e:
        warn(f"Cert error: {e}")
    except Exception as e:
        err(str(e))

def _vuln_clickjack(url):
    _, hdrs, _ = _vuln_fetch(url)
    xfo = hdrs.get("X-Frame-Options") or hdrs.get("x-frame-options")
    csp = hdrs.get("Content-Security-Policy","")
    if xfo:                          ok(f"X-Frame-Options: {xfo}")
    elif "frame-ancestors" in csp:   ok("CSP frame-ancestors set")
    else:                            warn("Potentially vulnerable to Clickjacking")

def _vuln_cors(url):
    _, hdrs, _ = _vuln_fetch(url, extra_headers={"Origin":"https://evil.com"})
    acao = hdrs.get("Access-Control-Allow-Origin") or hdrs.get("access-control-allow-origin")
    if not acao:            ok("No CORS header returned")
    elif acao == "*":       warn("ACAO: * — wildcard (public API or miscfg?)")
    elif "evil.com" in acao:err("CORS reflects arbitrary origin — VULNERABLE")
    else:                   ok(f"ACAO: {acao}")

def _vuln_paths(url):
    PATHS = ["/.git/config","/.env","/config.php","/wp-config.php",
             "/admin","/phpmyadmin","/robots.txt","/.htaccess",
             "/backup.zip","/server-status","/api/v1","/api/swagger.json"]
    base = url.rstrip("/")
    for path in PATHS:
        try:
            status, _, body = _vuln_fetch(base+path)
            if status == 200:
                warn(f"{status} {path}  → {body[:50].replace(chr(10),' ')}")
            else:
                print(f"  {DIM}  {status} {path}{RST}")
        except: pass

def _vuln_methods(url):
    for method in ["GET","POST","OPTIONS","PUT","DELETE","TRACE","HEAD"]:
        try:
            status, hdrs, _ = _vuln_fetch(url, method=method)
            allow = hdrs.get("Allow","")
            if method in ("TRACE","PUT","DELETE") and status < 400:
                warn(f"{method:<8} → {status}  {allow}")
            else:
                ok(f"{method:<8} → {status}  {allow}")
        except Exception as e:
            print(f"  {DIM}  {method:<8} → {e}{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  8. NETWORK RECON  [NEW]
# ═══════════════════════════════════════════════════════════════════════

def module_network_recon():
    box("MODULE 08 — NETWORK RECON")
    while True:
        print(f"\n  {CB}[1]{RST} ARP / host discovery  {CB}[2]{RST} Traceroute  {CB}[3]{RST} Latency sweep  {CB}[q]{RST} Back")
        ch = input(f"\n{CB}  ╠══>{RST} ").strip().lower()
        if ch in ("q",""):
            break

        elif ch == "1":
            subnet = prompt("Subnet (e.g. 192.168.1)", "192.168.1")
            end    = int(prompt("Last octet range end", "20"))
            print()
            hr()
            found = 0
            for i in range(1, end+1):
                ip = f"{subnet}.{i}"
                progress_bar(i, end, label=ip)
                try:
                    r = subprocess.run(["ping","-c","1","-W","1",ip],
                                       capture_output=True, timeout=2)
                    if r.returncode == 0:
                        try:    host = socket.gethostbyaddr(ip)[0]
                        except: host = "?"
                        print(f"\r  {MAG}[UP]{RST}  {GB}{ip:<18}{RST}  {C}{host}{RST}")
                        found += 1
                except: pass
            print()
            find(f"{found} host(s) up in {subnet}.1-{end}")

        elif ch == "2":
            host = prompt("Target host", "8.8.8.8")
            max_hops = int(prompt("Max hops", "20"))
            print()
            hr()
            info(f"Traceroute → {host}  (max {max_hops} hops)")
            print()
            cmd = (["tracert","-h",str(max_hops),host]
                   if os.name=="nt"
                   else ["traceroute","-m",str(max_hops),host])
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    print(f"  {G}{line.rstrip()}{RST}")
                proc.wait()
            except FileNotFoundError:
                err("traceroute/tracert not found.")
            except Exception as e:
                err(str(e))

        elif ch == "3":
            hosts = []
            info("Enter hosts to ping (blank line to start):")
            while True:
                h = input(f"  {DIM}host > {RST}").strip()
                if not h: break
                hosts.append(h)
            if not hosts:
                hosts = ["8.8.8.8","1.1.1.1","google.com"]

            print()
            hr()
            for h in hosts:
                try:
                    t0 = time.time()
                    socket.setdefaulttimeout(2)
                    socket.getaddrinfo(h, 80)
                    lat = (time.time()-t0)*1000
                    bar_w = 30
                    filled = min(bar_w, int(lat/5))
                    bar = G + "▓"*filled + DIM+G + "░"*(bar_w-filled) + RST
                    print(f"  {GB}{h:<30}{RST}  [{bar}]  {YB}{lat:6.1f} ms{RST}")
                except Exception as e:
                    print(f"  {R}{h:<30}{RST}  unreachable ({e})")

    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  9. CIPHER TOOLKIT  [NEW]
# ═══════════════════════════════════════════════════════════════════════

import base64

def module_cipher():
    box("MODULE 09 — CIPHER TOOLKIT")
    while True:
        print(f"""
  {CB}[1]{RST} Base64 encode/decode
  {CB}[2]{RST} ROT13
  {CB}[3]{RST} Caesar cipher
  {CB}[4]{RST} XOR cipher
  {CB}[5]{RST} Hex encode/decode
  {CB}[6]{RST} URL encode/decode
  {CB}[7]{RST} Binary encode/decode
  {CB}[q]{RST} Back""")
        ch = input(f"\n{CB}  ╠══>{RST} ").strip().lower()
        if ch in ("q",""): break

        text = prompt("Input text", "Hello World")

        if ch == "1":
            print(f"\n  {CB}Encode:{RST}  {YB}{base64.b64encode(text.encode()).decode()}{RST}")
            try:
                print(f"  {CB}Decode:{RST}  {YB}{base64.b64decode(text).decode()}{RST}")
            except: warn("Not valid base64 for decoding.")

        elif ch == "2":
            import codecs
            print(f"\n  {CB}ROT13:{RST}  {YB}{codecs.encode(text, 'rot_13')}{RST}")

        elif ch == "3":
            shift = int(prompt("Shift", "3"))
            enc = ""
            for c in text:
                if c.isalpha():
                    base = ord('A') if c.isupper() else ord('a')
                    enc += chr((ord(c)-base+shift)%26+base)
                else:
                    enc += c
            print(f"\n  {CB}Encrypted (shift {shift}):{RST}  {YB}{enc}{RST}")
            dec = ""
            for c in text:
                if c.isalpha():
                    base = ord('A') if c.isupper() else ord('a')
                    dec += chr((ord(c)-base-shift)%26+base)
                else:
                    dec += c
            print(f"  {CB}Decrypted (shift {shift}):{RST}  {YB}{dec}{RST}")

        elif ch == "4":
            key = ord(prompt("XOR key (single char)", "K")[0])
            xored = bytes(b ^ key for b in text.encode())
            print(f"\n  {CB}XOR hex:{RST}  {YB}{xored.hex()}{RST}")
            print(f"  {CB}XOR b64:{RST}  {YB}{base64.b64encode(xored).decode()}{RST}")

        elif ch == "5":
            print(f"\n  {CB}Hex encode:{RST}  {YB}{text.encode().hex()}{RST}")
            try:
                print(f"  {CB}Hex decode:{RST}  {YB}{bytes.fromhex(text).decode()}{RST}")
            except: warn("Not valid hex for decoding.")

        elif ch == "6":
            import urllib.parse
            print(f"\n  {CB}URL encode:{RST}  {YB}{urllib.parse.quote(text)}{RST}")
            print(f"  {CB}URL decode:{RST}  {YB}{urllib.parse.unquote(text)}{RST}")

        elif ch == "7":
            b = " ".join(f"{ord(c):08b}" for c in text)
            print(f"\n  {CB}Binary:{RST}  {YB}{b}{RST}")
            try:
                bits = text.replace(" ","")
                dec  = "".join(chr(int(bits[i:i+8],2)) for i in range(0,len(bits),8))
                print(f"  {CB}From binary:{RST}  {YB}{dec}{RST}")
            except: warn("Not valid binary string for decoding.")

    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  10. SYSTEM AUDIT  [NEW]
# ═══════════════════════════════════════════════════════════════════════

def module_sysaudit():
    box("MODULE 10 — SYSTEM AUDIT")
    print()

    # OS info
    import platform
    print(f"  {CB}► OS INFO{RST}")
    info(f"System   : {platform.system()} {platform.release()} {platform.machine()}")
    info(f"Node     : {platform.node()}")
    info(f"Python   : {platform.python_version()}")

    # Hostname / IP
    print(f"\n  {CB}► NETWORK{RST}")
    try:
        hn = socket.gethostname()
        ip = socket.gethostbyname(hn)
        info(f"Hostname : {hn}")
        info(f"Local IP : {ip}")
    except: pass

    # Listening ports
    print(f"\n  {CB}► LISTENING PORTS{RST}")
    cmd = (["netstat","-ano"] if os.name=="nt"
           else ["ss","-tlnp"])
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, timeout=8)
        for line in out.splitlines()[:25]:
            print(f"  {DIM}{line}{RST}")
    except Exception as e:
        warn(str(e))

    # Logged-in users
    print(f"\n  {CB}► LOGGED-IN USERS{RST}")
    try:
        out = subprocess.check_output(["who"], stderr=subprocess.DEVNULL,
                                      text=True, timeout=5)
        for line in out.splitlines():
            info(line)
    except Exception as e:
        warn(str(e))

    # Environment
    print(f"\n  {CB}► KEY ENV VARIABLES{RST}")
    for k in ["PATH","HOME","USER","SHELL","LANG","HOSTNAME",
              "TERM","LOGNAME","PWD"]:
        v = os.environ.get(k,"—")
        if v != "—": info(f"{k:<14}: {v}")

    hr()
    input(f"\n{DIM}  Press ENTER to return…{RST}")


# ═══════════════════════════════════════════════════════════════════════
#  MODULE MAP
# ═══════════════════════════════════════════════════════════════════════
MODULE_MAP = {
    0: module_port_scanner,
    1: module_packet_sniffer,
    2: module_password,
    3: module_hash_lab,
    4: module_osint,
    5: module_subdomain,
    6: module_vuln_scan,
    7: module_network_recon,
    8: module_cipher,
    9: module_sysaudit,
}

# ═══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        boot_sequence()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{YB}  [!] Interrupted.{RST}\n")
        sys.exit(0)
