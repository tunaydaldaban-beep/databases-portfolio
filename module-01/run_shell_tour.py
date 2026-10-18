"""Capture real sqlite3 CLI stdout, including its timer; run from any directory."""
import subprocess, shutil
from pathlib import Path
root=Path(__file__).resolve().parent.parent
shell=shutil.which('sqlite3')
if not shell:
    raise SystemExit('SQLite CLI is missing. Install it, reopen the terminal, and rerun this script.')
commands=(root/'module-01/tour-commands.sql').read_text()
r=subprocess.run([shell, 'module-01/tour.db'],input=commands,text=True,capture_output=True,cwd=root)
if r.returncode: raise SystemExit(r.stderr)
(root/'module-01/shell-tour.txt').write_text(r.stdout+r.stderr)
print('Saved real shell-tour.txt and tour.sql')
