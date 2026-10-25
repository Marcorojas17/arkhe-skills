#!/usr/bin/env python3
"""
ARKHE VIDEO - Generador de video forense local.
Inspirado en la estructura de Google Omni Flash Skill, pero sin dependencias
de APIs externas. Usa ffmpeg + ARKHE SENTINEL para firmar cada video.
"""

import argparse
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ARKHE_SECRET = os.getenv("ARKHE_SECRET", "").encode()


def sanitize_error(err, max_len=500):
    """Redacta secretos de mensajes de error (patrón heredado de Google)."""
    if not err:
        return ""
    s = str(err)
    if ARKHE_SECRET and len(ARKHE_SECRET) >= 8:
        try:
            s = s.replace(ARKHE_SECRET.decode(), "[REDACTED_KEY]")
        except Exception:
            pass
    s = re.sub(r'AIza[0-9A-Za-z_\-]{30,}', '[REDACTED_KEY]', s)
    s = re.sub(r'AQ\.[0-9A-Za-z_\-]{20,}', '[REDACTED_KEY]', s)
    s = re.sub(r'ya29\.[0-9A-Za-z_\-]+', '[REDACTED_TOKEN]', s)
    s = re.sub(r'Bearer\s+[A-Za-z0-9_\-\.]+', 'Bearer [REDACTED]', s, flags=re.IGNORECASE)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:max_len] if len(s) > max_len else s


def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sign_video(video_path, agent_id="ARKHE-Video-Certifier"):
    """Firma el hash del video con HMAC usando ARKHE_SECRET."""
    if not ARKHE_SECRET:
        raise RuntimeError("ARKHE_SECRET no configurado. Exporta: export ARKHE_SECRET='...'")
    file_hash = compute_sha256(video_path)
    sig = hmac.new(ARKHE_SECRET, file_hash.encode(), hashlib.sha256).hexdigest()
    timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "video": os.path.basename(video_path),
        "sha256": file_hash,
        "agent_id": agent_id,
        "timestamp_utc": timestamp,
        "hmac_signature": sig,
        "protocol": "ARKHE-SENTINEL-v1",
        "author": "Marco Antonio Rojas Valdovinos",
        "pacto": "51% Humano / 49% IA"
    }


def run_ffmpeg(cmd, label="ffmpeg"):
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            raise RuntimeError(f"{label} falló (código {r.returncode})")
        return r
    except FileNotFoundError:
        raise RuntimeError("ffmpeg no encontrado. Instala: pkg install ffmpeg")


def build_slideshow(images, output, seconds=4, resolution="1080x1080", fps=30):
    for img in images:
        if not os.path.exists(img):
            raise FileNotFoundError(f"Imagen no encontrada: {img}")

    try:
        width, height = map(int, resolution.lower().split("x"))
        if width <= 0 or height <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Resolución inválida; usa, por ejemplo, 1080x1080")

    size = f"{width}:{height}"
    inputs, filters = [], []

    for i, img in enumerate(images):
        inputs += ["-loop", "1", "-t", str(seconds), "-i", img]
        filters.append(
            f"[{i}:v]scale={size}:force_original_aspect_ratio=decrease,"
            f"pad={size}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}]"
        )

    concat = "".join(f"[v{i}]" for i in range(len(images)))
    filters.append(f"{concat}concat=n={len(images)}:v=1:a=0[outv]")

    cmd = (
        ["ffmpeg", "-y"] + inputs +
        ["-filter_complex", ";".join(filters), "-map", "[outv]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), output]
    )
    run_ffmpeg(cmd, "Slideshow")


def build_text_card(text, output, resolution="1080x1080", seconds=5, color="0x0a0a0a", fontcolor="0x00ffcc"):
    """Crea un video de una sola tarjeta de texto (título de apertura/cierre)."""
    text_safe = text.replace("'", "\\'").replace(":", "\\:")
    vf = (
        f"drawtext=text='{text_safe}':fontcolor={fontcolor}:fontsize=48:"
        f"x=(w-text_w)/2:y=(h-text_h)/2:"
        f"fontfile=/system/fonts/Roboto-Regular.ttf"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c={color}:s={resolution}:d={seconds}",
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        output,
    ]
    run_ffmpeg(cmd, "Text card")


def cmd_slideshow(args):
    out = args.output or "arkhe_video.mp4"
    print(f"🎬 Slideshow: {len(args.inputs)} imágenes → {out}")
    build_slideshow(args.inputs, out, args.seconds, args.resolution)
    print(f"✅ Creado: {out} ({os.path.getsize(out):,} bytes)")
    if args.certify:
        cert = sign_video(out)
        cert_path = out + ".certificate.json"
        with open(cert_path, "w") as f:
            json.dump(cert, f, indent=2)
        print(f"🔐 Certificado: {cert_path}")
        print(f"   SHA-256: {cert['sha256']}")
        print(f"   HMAC:    {cert['hmac_signature'][:32]}...")


def cmd_text(args):
    out = args.output or "arkhe_title.mp4"
    build_text_card(" ".join(args.inputs), out, args.resolution, args.seconds)
    print(f"✅ Creado: {out}")


def cmd_verify(args):
    video = args.inputs[0]
    if not os.path.exists(video):
        raise FileNotFoundError(f"Video no encontrado: {video}")
    h = compute_sha256(video)
    print(f"📹 Video: {video}")
    print(f"🔐 SHA-256 actual: {h}")
    cert_path = video + ".certificate.json"
    if os.path.exists(cert_path):
        with open(cert_path) as f:
            cert = json.load(f)
        match = cert["sha256"] == h
        print(f"{'✅' if match else '❌'} Integridad: {'OK' if match else 'ALTERADO'}")
        print(f"   Firmado por: {cert.get('author')} · {cert.get('timestamp_utc')}")
    else:
        print("⚠️  No hay certificado asociado.")


def main():
    p = argparse.ArgumentParser(
        description="ARKHE VIDEO - Video forense local (ffmpeg + HMAC, sin APIs de Google).",
        epilog="Ej: python arkhe_video.py slideshow assets/*.png -o promo.mp4 --certify",
    )
    sub = p.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("slideshow", help="Crea un video a partir de imágenes")
    s.add_argument("inputs", nargs="+", help="Imágenes de entrada")
    s.add_argument("-o", "--output", help="Archivo de salida")
    s.add_argument("-s", "--seconds", type=int, default=4, help="Segundos por imagen (default 4)")
    s.add_argument("--resolution", default="1080x1080", help="Resolución (default 1080x1080)")
    s.add_argument("--certify", action="store_true", help="Firmar con HMAC de ARKHE")
    s.set_defaults(func=cmd_slideshow)

    t = sub.add_parser("title", help="Crea una tarjeta de texto (título/cierre)")
    t.add_argument("inputs", nargs="+", help="Texto de la tarjeta")
    t.add_argument("-o", "--output", help="Archivo de salida")
    t.add_argument("-s", "--seconds", type=int, default=5)
    t.add_argument("--resolution", default="1080x1080")
    t.set_defaults(func=cmd_text)

    v = sub.add_parser("verify", help="Verifica la integridad de un video certificado")
    v.add_argument("inputs", nargs=1, help="Video a verificar")
    v.set_defaults(func=cmd_verify)

    args = p.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {sanitize_error(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
