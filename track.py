"""
╔══════════════════════════════════════════════════════════════╗
║          PHONEINTEL — Phone Intelligence Terminal            ║
║               Developed by: @BASH TECH UG                      ║
║          phonenumbers  |  geocoder  |  zoneinfo              ║
╚══════════════════════════════════════════════════════════════╝
"""

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import geocoder as geo
import datetime
import time
import sys
import os
import re
import random

# ─── Colors ──────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BLINK   = "\033[5m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    DARK    = "\033[90m"

# ─── Helpers ─────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def typewrite(text, delay=0.022, color=C.GREEN):
    for ch in text:
        sys.stdout.write(color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def glitch_text(text, color=C.CYAN):
    """Print text with a glitch reveal effect."""
    chars = "!@#$%^&*<>?/|\\[]{}~`0123456789ABCDEF"
    result = list(" " * len(text))
    indices = list(range(len(text)))
    random.shuffle(indices)
    for idx in indices:
        result[idx] = random.choice(chars)
        sys.stdout.write(f"\r{color}{''.join(result)}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.012)
        result[idx] = text[idx]
        sys.stdout.write(f"\r{color}{''.join(result)}{C.RESET}")
        sys.stdout.flush()
    print()

def spinner(label, duration=1.2, style="cyber"):
    """Animated spinner with cyber style."""
    if style == "cyber":
        frames = ["[■□□□□□□□□□]","[■■□□□□□□□□]","[■■■□□□□□□□]",
                  "[■■■■□□□□□□]","[■■■■■□□□□□]","[■■■■■■□□□□]",
                  "[■■■■■■■□□□]","[■■■■■■■■□□]","[■■■■■■■■■□]","[■■■■■■■■■■]"]
    else:
        frames = ["◐","◓","◑","◒"]

    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {C.CYAN}{frame}{C.RESET}  {C.DARK}{label}{C.RESET}  ")
        sys.stdout.flush()
        time.sleep(0.09)
        i += 1
    sys.stdout.write(f"\r  {C.GREEN}[■■■■■■■■■■]{C.RESET}  {C.GREEN}{label}{C.RESET}  ✓\n")
    sys.stdout.flush()

def fake_scan_line(label, value, delay=0.4):
    """Simulates a scanning line being resolved."""
    chars = "ABCDEF0123456789?#@!"
    sys.stdout.write(f"  {C.DARK}{'─'*16}{C.RESET}  {C.DARK}SCANNING...{C.RESET}")
    sys.stdout.flush()
    time.sleep(delay)
    fake = "".join(random.choice(chars) for _ in str(value))
    sys.stdout.write(f"\r  {C.DIM}{label:<16}{C.RESET}  {C.YELLOW}{fake}{C.RESET}  ")
    sys.stdout.flush()
    time.sleep(0.25)
    sys.stdout.write(f"\r  {C.DARK}{label:<16}{C.RESET}  {C.GREEN}{value}{C.RESET}          \n")
    sys.stdout.flush()

def divider(char="─", width=62, color=C.DARK):
    print(color + char * width + C.RESET)

def label_val(label, value, label_color=C.DARK, val_color=C.WHITE):
    print(f"  {label_color}{label:<18}{C.RESET}{val_color}{value}{C.RESET}")

def risk_bar(score):
    filled = int(score / 10)
    bar = "▓" * filled + "░" * (10 - filled)
    if score <= 30:   color = C.GREEN
    elif score <= 60: color = C.YELLOW
    else:             color = C.RED
    label = "LOW" if score <= 30 else ("MEDIUM" if score <= 60 else "HIGH")
    return f"{color}{bar}  {score}/100  [{label}]{C.RESET}"

# ─── Boot sequence ────────────────────────────────────────────
def boot_sequence():
    clear()
    boot_lines = [
        ("PHONEINTEL SYSTEM BOOT",         C.CYAN,    0.03),
        ("Loading modules............OK",  C.DARK,    0.02),
        ("phonenumbers lib...........OK",  C.DARK,    0.02),
        ("geocoder engine............OK",  C.DARK,    0.02),
        ("timezone resolver..........OK",  C.DARK,    0.02),
        ("terminal renderer..........OK",  C.DARK,    0.02),
        ("intelligence core..........OK",  C.GREEN,   0.02),
    ]
    print()
    for text, color, delay in boot_lines:
        typewrite(f"  >> {text}", delay, color)
        time.sleep(0.05)
    time.sleep(0.3)

# ─── Main banner ──────────────────────────────────────────────
def print_banner():
    clear()
    banner_lines = [
        f"  {C.CYAN}{C.BOLD}██████╗ ██╗  ██╗ ██████╗ ███╗  ██╗███████╗",
        f"  ██╔══██╗██║  ██║██╔═══██╗████╗ ██║██╔════╝",
        f"  ██████╔╝███████║██║   ██║██╔██╗██║█████╗  ",
        f"  ██╔═══╝ ██╔══██║██║   ██║██║╚████║██╔══╝  ",
        f"  ██║     ██║  ██║╚██████╔╝██║ ╚███║███████╗",
        f"  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚══╝╚══════╝{C.RESET}",
        f"",
        f"  {C.CYAN}██╗███╗  ██╗████████╗███████╗██╗     {C.DARK}v3.0{C.RESET}",
        f"  {C.CYAN}██║████╗ ██║╚══██╔══╝██╔════╝██║{C.RESET}",
        f"  {C.CYAN}██║██╔██╗██║   ██║   █████╗  ██║{C.RESET}",
        f"  {C.CYAN}██║██║╚████║   ██║   ██╔══╝  ██║{C.RESET}",
        f"  {C.CYAN}██║██║ ╚███║   ██║   ███████╗███████╗{C.RESET}",
        f"  {C.CYAN}╚═╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚══════╝{C.RESET}",
    ]
    for line in banner_lines:
        print(line)
        time.sleep(0.03)

    print(f"\n  {C.DARK}{'═'*62}{C.RESET}")
    print(f"  {C.MAGENTA}  [ PHONE NUMBER INTELLIGENCE & OSINT TERMINAL ]{C.RESET}")
    print(f"  {C.DARK}  Developed by: {C.CYAN}@BASH BASH{C.DARK}   |   Terminal v3.0{C.RESET}")
    print(f"  {C.DARK}{'═'*62}{C.RESET}\n")

# ─── Number type ─────────────────────────────────────────────
def decode_number_type(num_type):
    types = {
        0:  ("FIXED LINE",    C.BLUE),
        1:  ("MOBILE",        C.GREEN),
        2:  ("FIXED/MOBILE",  C.CYAN),
        3:  ("TOLL-FREE",     C.YELLOW),
        4:  ("PREMIUM RATE",  C.RED),
        5:  ("SHARED COST",   C.MAGENTA),
        6:  ("VoIP",          C.CYAN),
        7:  ("PERSONAL",      C.WHITE),
        8:  ("PAGER",         C.DARK),
        9:  ("UAN",           C.DARK),
        10: ("VOICEMAIL",     C.DARK),
        -1: ("UNKNOWN",       C.DARK),
    }
    return types.get(num_type, ("UNKNOWN", C.DARK))

# ─── Formats ─────────────────────────────────────────────────
def get_formats(number):
    return {
        "E.164":         phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164),
        "International": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "National":      phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL),
        "RFC3966":       phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.RFC3966),
    }

# ─── Coordinates ─────────────────────────────────────────────
def get_coordinates(location_str):
    try:
        g = geo.osm(location_str, headers={"User-Agent": "PhoneIntelTerminal/3.0"})
        if g.ok:
            return g.lat, g.lng, g.address
        g2 = geo.arcgis(location_str)
        if g2.ok:
            return g2.lat, g2.lng, g2.address
    except Exception:
        pass
    return None, None, None

# ─── Risk engine ─────────────────────────────────────────────
def calculate_risk(number, is_valid, num_type, carr):
    score = 0
    flags = []

    if not is_valid:
        score += 40
        flags.append("Number failed validity check")

    if num_type == 6:   # VoIP
        score += 25
        flags.append("VoIP number — common in fraud/spam")
    elif num_type == 4: # Premium rate
        score += 30
        flags.append("Premium rate — potential scam vector")
    elif num_type == 3: # Toll-free
        score += 10
        flags.append("Toll-free — verify caller identity")

    if not carr or carr.strip() in ("", "Unknown"):
        score += 15
        flags.append("Carrier unresolved — may be MVNO or virtual")

    score = min(score, 100)
    return score, flags

# ─── Build intel summary ─────────────────────────────────────
def build_intel(phone_data: dict, risk_score: int, risk_flags: list):
    """
    Generate a structured intelligence summary using
    local logic — no external AI API required.
    """
    num_type   = phone_data["number_type"]
    region     = phone_data["region"]
    carr       = phone_data["carrier"]
    tz_str     = phone_data["timezones"]
    local_time = phone_data["local_time"]
    lat        = phone_data["latitude"]
    lng        = phone_data["longitude"]
    is_valid   = phone_data["is_valid"]

    lines = []

    lines.append(f"{C.CYAN}┌─ IDENTITY PROFILE {'─'*41}┐{C.RESET}")
    if num_type in ("MOBILE", "FIXED LINE", "FIXED/MOBILE"):
        lines.append(f"{C.DARK}│{C.RESET}  Type    : {C.GREEN}Likely personal/consumer registered number{C.RESET}")
    elif num_type == "VoIP":
        lines.append(f"{C.DARK}│{C.RESET}  Type    : {C.YELLOW}VoIP — internet-based, may be virtual/temporary{C.RESET}")
    elif num_type == "TOLL-FREE":
        lines.append(f"{C.DARK}│{C.RESET}  Type    : {C.YELLOW}Toll-free — typically business or call center{C.RESET}")
    elif num_type == "PREMIUM RATE":
        lines.append(f"{C.DARK}│{C.RESET}  Type    : {C.RED}Premium rate — charges caller, high scam risk{C.RESET}")
    else:
        lines.append(f"{C.DARK}│{C.RESET}  Type    : {C.DARK}Unclassified — treat with caution{C.RESET}")

    validity_note = "Passes all structural checks" if is_valid else "FAILED validity — may be fake or malformed"
    v_color = C.GREEN if is_valid else C.RED
    lines.append(f"{C.DARK}│{C.RESET}  Status  : {v_color}{validity_note}{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  Carrier : {C.CYAN}{carr}{C.RESET}")
    lines.append(f"{C.CYAN}├─ GEO-INTELLIGENCE {'─'*41}┤{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  Region  : {C.GREEN}{region}{C.RESET}")
    if lat and lng:
        lines.append(f"{C.DARK}│{C.RESET}  Coords  : {C.WHITE}{lat:.5f}°N  {lng:.5f}°E{C.RESET}")
        lines.append(f"{C.DARK}│{C.RESET}  MapLink : {C.BLUE}https://www.openstreetmap.org/?mlat={lat:.4f}&mlon={lng:.4f}&zoom=8{C.RESET}")
    else:
        lines.append(f"{C.DARK}│{C.RESET}  Coords  : {C.DARK}Not resolvable from registration data{C.RESET}")

    lines.append(f"{C.CYAN}├─ TIMEZONE & ACTIVITY {'─'*38}┤{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  Zone    : {C.WHITE}{tz_str}{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  Local   : {C.MAGENTA}{local_time}{C.RESET}")

    # Estimate business hours window
    try:
        local_hour = int(local_time.split(":")[0]) if local_time != "Unknown" else -1
        if 8 <= local_hour < 12:
            activity = "Morning — high activity window"
            act_color = C.GREEN
        elif 12 <= local_hour < 18:
            activity = "Afternoon — peak contact hours"
            act_color = C.GREEN
        elif 18 <= local_hour < 22:
            activity = "Evening — moderate activity"
            act_color = C.YELLOW
        else:
            activity = "Off-hours — low response likelihood"
            act_color = C.DARK
    except Exception:
        activity = "Unable to determine"
        act_color = C.DARK
    lines.append(f"{C.DARK}│{C.RESET}  Window  : {act_color}{activity}{C.RESET}")

    lines.append(f"{C.CYAN}├─ RISK ASSESSMENT {'─'*42}┤{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  Score   : {risk_bar(risk_score)}")
    if risk_flags:
        for flag in risk_flags:
            lines.append(f"{C.DARK}│{C.RESET}  {C.YELLOW}⚑ {flag}{C.RESET}")
    else:
        lines.append(f"{C.DARK}│{C.RESET}  {C.GREEN}✔ No significant risk flags detected{C.RESET}")

    lines.append(f"{C.CYAN}├─ OSINT TIPS {'─'*47}┤{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  {C.DIM}1. Search E.164 format on Google, Truecaller, WhoCalledMe{C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  {C.DIM}2. Check reverse-lookup: sync.me, numverify (free tier){C.RESET}")
    lines.append(f"{C.DARK}│{C.RESET}  {C.DIM}3. Search region telecom regulator for carrier ownership{C.RESET}")
    lines.append(f"{C.CYAN}└{'─'*60}┘{C.RESET}")

    return lines

# ─── Save report ─────────────────────────────────────────────
def save_report(phone_data: dict, risk_score: int, risk_flags: list):
    timestamp  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_num   = re.sub(r'[^\d+]', '', phone_data.get("input", "unknown"))
    filename   = f"phoneintel_{safe_num}_{timestamp}.txt"

    sep = "=" * 62
    lines = [
        sep,
        "  PHONEINTEL — Intelligence Report",
        f"  Generated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Developed : @BASH BASH",
        sep, "",
        "── PHONE DATA " + "─" * 48,
    ]
    for k, v in phone_data.items():
        lines.append(f"  {k:<22}: {v}")

    lines += ["", "── RISK ASSESSMENT " + "─" * 43]
    lines.append(f"  Score  : {risk_score}/100")
    for flag in risk_flags:
        lines.append(f"  Flag   : {flag}")
    lines += ["", "── FORMATS " + "─" * 51]
    for k in ("format_e164","format_intl","format_national","format_rfc3966"):
        lines.append(f"  {k:<22}: {phone_data.get(k,'')}")
    lines += ["", sep]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename

# ─── Core tracker ────────────────────────────────────────────
def track_phone_number():
    boot_sequence()
    print_banner()
    session_count = 0

    while True:
        print(f"  {C.CYAN}TARGET NUMBER{C.RESET}  {C.DARK}(E.164 format — include + and country code){C.RESET}")
        print(f"  {C.DARK}Examples: +256771075383   +14155552671   +447911123456{C.RESET}\n")

        try:
            phone = input(f"  {C.YELLOW}PHONEINTEL >{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.DARK}Session terminated.{C.RESET}\n")
            break

        if phone.lower() in ("exit", "quit", "q", "x"):
            print(f"\n  {C.GREEN}[SESSION CLOSED]{C.RESET}  {C.DARK}Tracked {session_count} number(s).  Stay safe.{C.RESET}\n")
            break

        if not phone:
            print(f"  {C.RED}[ERR]{C.RESET} No input. Enter a number.\n")
            continue

        print()

        # ── Parse ──────────────────────────────────────────────
        try:
            spinner("Initializing number parser       ", 0.5)
            number = phonenumbers.parse(phone, None)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            print(f"\n  {C.RED}[PARSE ERROR]{C.RESET} {e}")
            print(f"  {C.DARK}Tip: Always include + and country code.{C.RESET}\n")
            continue

        # ── Scanning animation ─────────────────────────────────
        spinner("Validating number structure      ", 0.6)
        spinner("Resolving carrier & operator     ", 0.9)
        spinner("Triangulating geolocation data   ", 1.1)
        spinner("Enumerating timezone metadata    ", 0.7)
        spinner("Running risk analysis engine     ", 0.8)
        spinner("Compiling intelligence report    ", 0.6)
        print()

        # ── Gather all data ────────────────────────────────────
        is_valid    = phonenumbers.is_valid_number(number)
        is_possible = phonenumbers.is_possible_number(number)
        loc         = geocoder.description_for_number(number, "en") or "Unknown"
        carr        = carrier.name_for_number(number, "en") or "Unknown"
        tz          = timezone.time_zones_for_number(number)
        tz_str      = ", ".join(tz) if tz else "Unknown"
        num_type    = phonenumbers.number_type(number)
        type_name, type_color = decode_number_type(num_type)
        formats     = get_formats(number)
        lat, lng, address = get_coordinates(loc)

        local_time = "Unknown"
        try:
            if tz:
                from zoneinfo import ZoneInfo
                zt = ZoneInfo(tz[0])
                local_time = datetime.datetime.now(zt).strftime("%H:%M  %Z  (%Y-%m-%d)")
        except Exception:
            try:
                import pytz
                zt = pytz.timezone(tz[0])
                local_time = datetime.datetime.now(zt).strftime("%H:%M  %Z  (%Y-%m-%d)")
            except Exception:
                pass

        phone_data = {
            "input":           phone,
            "country_code":    f"+{number.country_code}",
            "national_number": str(number.national_number),
            "is_valid":        is_valid,
            "is_possible":     is_possible,
            "number_type":     type_name,
            "region":          loc,
            "carrier":         carr,
            "timezones":       tz_str,
            "local_time":      local_time,
            "latitude":        lat,
            "longitude":       lng,
            "address":         address or "Not available",
            "format_e164":     formats["E.164"],
            "format_intl":     formats["International"],
            "format_national": formats["National"],
            "format_rfc3966":  formats["RFC3966"],
        }

        risk_score, risk_flags = calculate_risk(number, is_valid, num_type, carr)

        # ── Header ─────────────────────────────────────────────
        divider("═", 62, C.CYAN)
        glitch_text(f"  PHONEINTEL  //  TARGET ACQUIRED  //  {datetime.datetime.now().strftime('%H:%M:%S')}", C.CYAN)
        divider("═", 62, C.CYAN)
        print()

        # ── Scan-style data reveal ─────────────────────────────
        print(f"  {C.CYAN}[ SIGNAL TRACE ]{C.RESET}")
        print()
        fake_scan_line("INPUT",           phone,                        0.3)
        fake_scan_line("COUNTRY CODE",    f"+{number.country_code}",    0.3)
        fake_scan_line("NATIONAL #",      str(number.national_number),  0.3)
        fake_scan_line("TYPE",            type_name,                    0.25)
        fake_scan_line("REGION",          loc,                          0.3)
        fake_scan_line("CARRIER",         carr,                         0.3)
        fake_scan_line("TIMEZONE",        tz_str,                       0.25)
        fake_scan_line("LOCAL TIME",      local_time,                   0.25)
        if lat:
            fake_scan_line("LATITUDE",    f"{lat:.5f}°",                0.25)
            fake_scan_line("LONGITUDE",   f"{lng:.5f}°",                0.25)
        else:
            fake_scan_line("COORDINATES", "UNRESOLVED",                 0.25)
        fake_scan_line("VALID",           "YES ✓" if is_valid else "NO ✗", 0.2)
        fake_scan_line("POSSIBLE",        "YES" if is_possible else "NO",  0.2)

        # ── Formats ────────────────────────────────────────────
        print()
        print(f"  {C.CYAN}[ NUMBER FORMATS ]{C.RESET}")
        print()
        for fmt_name, fmt_val in formats.items():
            label_val(f"  {fmt_name}", fmt_val, C.DARK, C.CYAN)

        # ── Intelligence report ────────────────────────────────
        print()
        print(f"  {C.CYAN}[ INTELLIGENCE REPORT ]{C.RESET}")
        print()
        intel_lines = build_intel(phone_data, risk_score, risk_flags)
        for line in intel_lines:
            print(f"  {line}")
            time.sleep(0.04)

        divider("═", 62, C.CYAN)
        session_count += 1

        # ── Post-scan menu ─────────────────────────────────────
        while True:
            print(f"\n  {C.DARK}{'─'*58}{C.RESET}")
            print(f"  {C.BOLD}NEXT ACTION:{C.RESET}")
            print(f"  {C.CYAN}[1]{C.RESET}  Save intelligence report to file")
            print(f"  {C.CYAN}[2]{C.RESET}  Track another number")
            print(f"  {C.CYAN}[3]{C.RESET}  Reprint this report")
            print(f"  {C.CYAN}[4]{C.RESET}  Exit terminal")
            print(f"  {C.DARK}{'─'*58}{C.RESET}")

            try:
                choice = input(f"  {C.YELLOW}PHONEINTEL >{C.RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                choice = "4"

            if choice == "1":
                fname = save_report(phone_data, risk_score, risk_flags)
                typewrite(f"  >> Report written: {fname}", 0.02, C.GREEN)

            elif choice == "2":
                print()
                print_banner()
                break

            elif choice == "3":
                print()
                for line in intel_lines:
                    print(f"  {line}")
                    time.sleep(0.02)

            elif choice == "4":
                print(f"\n  {C.GREEN}[SESSION CLOSED]{C.RESET}")
                typewrite(f"  >> {session_count} number(s) tracked  |  @BASH BASH  |  PhoneIntel v3.0", 0.015, C.DARK)
                print()
                return

            else:
                print(f"  {C.RED}[ERR]{C.RESET} Invalid choice.")

# ─── Entry ────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        track_phone_number()
    except KeyboardInterrupt:
        print(f"\n\n  {C.DARK}[SIGINT] Terminal closed.{C.RESET}\n")
