"""Captura janelas reais do R e do editor nano para os dois relatórios.

Dependências: Xvfb, Openbox, stterm, xdotool, ImageMagick, nano e R.
As imagens são gravadas pelo comando import, sem desenhar ou alterar seu conteúdo.
"""
import argparse
import hashlib
import json
import os
import shlex
import shutil
import socket
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui-root", type=Path)
    parser.add_argument("--r", default=shutil.which("R"))
    args = parser.parse_args()
    if not args.r:
        parser.error("Informe --r com o caminho do executável R.")
    env = os.environ.copy()
    if args.gui_root:
        env["PATH"] = str(args.gui_root / "usr/bin") + ":" + env["PATH"]
        env["LD_LIBRARY_PATH"] = str(args.gui_root / "usr/lib/x86_64-linux-gnu")
        env["XDG_DATA_DIRS"] = str(args.gui_root / "usr/share") + ":/usr/share"
    env["DISPLAY"] = "127.0.0.1:96"
    env["LANG"] = "C.UTF-8"
    programs = {}
    for name in ["Xvfb", "openbox", "stterm", "xdotool", "import", "nano", "script"]:
        programs[name] = shutil.which(name, path=env["PATH"])
        if not programs[name]:
            raise RuntimeError(f"Programa ausente: {name}")

    def run(name, *values, **kwargs):
        return subprocess.run([programs[name], *map(str, values)], env=env,
                              check=True, capture_output=True, text=True, **kwargs)

    processes = []
    with tempfile.TemporaryDirectory(prefix="capturas_datalab9_") as temp:
        with open(Path(temp) / "interface.log", "w") as log:
            try:
                server = subprocess.Popen([
                    programs["Xvfb"], ":96", "-screen", "0", "1800x1700x24",
                    "-nolisten", "unix", "-nolisten", "local", "-listen", "tcp", "-ac"
                ], env=env, stdout=log, stderr=log)
                processes.append(server)
                for _ in range(50):
                    try:
                        with socket.create_connection(("127.0.0.1", 6096), timeout=.3):
                            break
                    except OSError:
                        if server.poll() is not None:
                            raise RuntimeError("Xvfb encerrou antes de abrir o display.")
                        time.sleep(.1)
                else:
                    raise RuntimeError("O display não ficou disponível.")
                manager = subprocess.Popen([programs["openbox"], "--sm-disable"],
                                           env=env, stdout=log, stderr=log)
                processes.append(manager)
                time.sleep(.8)

                def window(title, rows, command, cwd):
                    proc = subprocess.Popen([
                        programs["stterm"], "-g", f"100x{rows}+25+25",
                        "-f", "DejaVu Sans Mono:size=16", "-t", title,
                        "-e", *command
                    ], cwd=cwd, env=env, stdout=log, stderr=log)
                    processes.append(proc)
                    for _ in range(80):
                        found = subprocess.run([programs["xdotool"], "search", "--onlyvisible",
                                                "--name", "^" + title + "$"], env=env,
                                               capture_output=True, text=True)
                        if found.returncode == 0 and found.stdout.strip():
                            wid = found.stdout.splitlines()[-1]
                            run("xdotool", "windowactivate", "--sync", wid)
                            time.sleep(.5)
                            return proc, wid
                        if proc.poll() is not None:
                            log.flush()
                            raise RuntimeError(Path(log.name).read_text())
                        time.sleep(.1)
                    raise RuntimeError("Janela não encontrada: " + title)

                for folder, name, code_rows in [
                    ("datalab9", "Claudio", 47),
                    ("datalab9_lucas", "Lucas", 39)
                ]:
                    base = ROOT / folder
                    dest = base / "capturas"
                    dest.mkdir(exist_ok=True)
                    transcript = dest / "sessao_R.txt"
                    command = shlex.join([str(Path(args.r).resolve()), "--vanilla", "--quiet"])
                    proc, wid = window(f"R Console - {name} - DataLab 9", 38 if name == "Claudio" else 28,
                                       [programs["script"], "-qf", "-c", command, str(transcript)], base)
                    run("xdotool", "type", "--clearmodifiers", "--delay", "1", "R.version.string")
                    run("xdotool", "key", "Return")
                    time.sleep(.3)
                    run("xdotool", "type", "--clearmodifiers", "--delay", "1",
                        'source("indicadores_mercado_trabalho.R")')
                    run("xdotool", "key", "Return")
                    for _ in range(50):
                        if transcript.exists() and "nível" in transcript.read_text(errors="replace").lower():
                            break
                        time.sleep(.1)
                    else:
                        raise RuntimeError("O R não concluiu a execução: " + folder)
                    time.sleep(.4)
                    run("import", "-display", env["DISPLAY"], "-window", wid, "-frame",
                        dest / "console.png")
                    run("xdotool", "type", "--clearmodifiers", 'q("no")')
                    run("xdotool", "key", "Return")
                    proc.wait(timeout=10)
                    for index, line, count in [(1, 1, code_rows), (2, 1, 44 if name == "Claudio" else 35)]:
                        proc, wid = window(f"Codigo R - {name} - parte {index}", count,
                                           ["/usr/bin/env", "TERM=xterm-256color", programs["nano"], "-I", "-v", "-l", "-c", "-j",
                                            f"+{line}", "indicadores_mercado_trabalho.R"], base)
                        if index == 2:
                            run("xdotool", "key", "Next")
                        time.sleep(.4)
                        run("import", "-display", env["DISPLAY"], "-window", wid, "-frame",
                            dest / f"codigo_{index}.png")
                        run("xdotool", "key", "ctrl+x")
                        proc.wait(timeout=10)
                    manifest = {
                        "captura_utc": datetime.now(timezone.utc).isoformat(),
                        "interface_execucao": "R interativo em stterm",
                        "interface_codigo": "GNU nano em stterm, modo somente leitura",
                        "metodo": "ImageMagick import, captura direta da janela com moldura",
                        "codigo_sha256": sha(base / "indicadores_mercado_trabalho.R"),
                        "dados_sha256": sha(base / "dados_pnad.csv"),
                        "arquivos_sha256": {p.name: sha(p) for p in sorted(dest.glob("*.png"))},
                    }
                    (dest / "proveniencia.json").write_text(
                        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
                    print(f"{name}: console e duas páginas de código capturados.", flush=True)
            finally:
                for proc in reversed(processes):
                    if proc.poll() is None:
                        proc.terminate()
                        try:
                            proc.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            proc.kill()


if __name__ == "__main__":
    main()
