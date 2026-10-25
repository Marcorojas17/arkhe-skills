---
name: arkhe-video
description: Forensic video generator with ffmpeg + SHA-256 + HMAC certification. Use when the user asks to create a slideshow, promotional video, or certify a video with cryptographic integrity. Runs 100% offline, no external APIs.
---

# ARKHE VIDEO

## When to activate
User says: "create video", "slideshow", "promo video", "certify video", "forensic video".

## Instructions
1. Ensure `ARKHE_SECRET` is exported in the environment.
2. Run: `python arkhe_video.py slideshow <images> -o <output.mp4> --certify`
3. Report: video path, SHA-256, HMAC signature, certificate path.
4. To verify: `python arkhe_video.py verify <video>`

## Golden rule
Never call external video APIs. Use local ffmpeg + ARKHE SENTINEL HMAC.
Faster, offline, auditable.
