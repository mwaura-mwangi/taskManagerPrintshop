import subprocess
from typing import Any

# --- Quick path: lp command ---
def print_with_lp(filepath: str, printer: str = "PDF", options: dict | None = None) -> None:
    options = options or {}
    cmd = ["lp", "-d", printer]
    for k, v in options.items():
        cmd += ["-o", f"{k}={v}"]
    cmd.append(filepath)
    subprocess.run(cmd, check=True)

# --- Rich control: pycups ---
try:
    import cups  # type: ignore
except ImportError:
    cups: Any = None

def print_with_cups(filepath: str, printer: str = "PDF", options: dict | None = None) -> int:
    if cups is None:
        raise RuntimeError("pycups not installed. Install with `sudo apt install python3-cups`")
    conn = cups.Connection()
    if printer not in conn.getPrinters():
        # If not found, it can still work if CUPS default is set
        pass
    job_id = conn.printFile(printer, filepath, "PrintShop Job", options or {})
    return job_id
