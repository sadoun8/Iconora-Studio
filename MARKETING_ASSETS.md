Marketing assets & production notes

1) Required assets
- Short product video (30s) - hero feature montage
- Tutorial video (5m) - quick walkthrough (logo designer)
- GIFs (3): Icon converter, Logo generation, Signature engine
- Screenshots (6): key screens at 1920×1080 and mobile 1080×1920
- Social banners: 1200×628 (Twitter), 1080×1080 (Instagram)

2) Tools recommended
- Screen capture: OBS Studio
- Video editor: DaVinci Resolve (free) or Shotcut
- GIF: ezgif.com or convert via ffmpeg

3) Sample FFmpeg commands
- Create GIF from MP4 (short clip):
```bash
ffmpeg -ss 00:00:02 -t 5 -i demo.mp4 -vf "fps=15,scale=640:-1:flags=lanczos" -loop 0 out.gif
```
- Create trimmed MP4 for YouTube:
```bash
ffmpeg -i raw.mp4 -ss 00:00:10 -to 00:00:40 -c:v libx264 -crf 23 -preset veryfast out_trimmed.mp4
```

4) Branding guidelines
- Primary color: #667eea
- Accent gradient: #667eea → #764ba2
- Font for marketing: Inter or Poppins
- Logo clearspace: 20px around icon

5) Copy examples (short)
- Headline: "Design Like a Pro — Iconora Studio"
- Subhead: "Icons, logos, signatures — one app. One-time price."
- CTA: "Download Demo" / "Buy Pro — $29"

6) Deliverables checklist
- [ ] 30s hero video
- [ ] 5m tutorial
- [ ] 3 GIFs
- [ ] 6 screenshots
- [ ] Social banners
- [ ] ProductHunt assets (images + description)
