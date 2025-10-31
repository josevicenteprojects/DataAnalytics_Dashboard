# Guía de Capturas y GIF (Data Analytics Dashboard)

## 1) Grabación
- Página: http://localhost:8002
- Mostrar: dashboard (gráficos) + filtros + exportación (si aplica)
- 20–25s

## 2) Conversión MP4 → GIF
```bash
# Windows
ffmpeg -y -i .\docs\gifs\demo.mp4 -vf "fps=15,scale=1280:-1:flags=lanczos,palettegen" .\docs\gifs\palette.png
ffmpeg -y -i .\docs\gifs\demo.mp4 -i .\docs\gifs\palette.png -lavfi "fps=15,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=sierra2_4a" .\docs\gifs\demo_20s.gif

# Linux/Mac
ffmpeg -y -i ./docs/gifs/demo.mp4 -vf "fps=15,scale=1280:-1:flags=lanczos,palettegen" ./docs/gifs/palette.png
ffmpeg -y -i ./docs/gifs/demo.mp4 -i ./docs/gifs/palette.png -lavfi "fps=15,scale=1280:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=sierra2_4a" ./docs/gifs/demo_20s.gif
```

## 3) Nombres
- Capturas: `docs/capturas/01_dashboard.png`, `02_endpoint_metrics.png`, `03_filters.png`
- GIF: `docs/gifs/demo_20s.gif`
