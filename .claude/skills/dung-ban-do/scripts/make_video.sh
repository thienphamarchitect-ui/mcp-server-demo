#!/usr/bin/env bash
# Render toàn bộ khung hình (3 tiến trình song song), mix âm thanh, ghép MP4.
#   bash make_video.sh <projectDir> <out.mp4> [fromFrame toFrame]   (from/to: chỉ render lại một đoạn)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; P="$(cd "$1" && pwd)"; OUT="$2"
N=$(node -e "global.window={};eval(require('fs').readFileSync('$P/timeline.js','utf8'));const t=window.TL;console.log(Math.round(t.total*(t.fps||30)))")
A=${3:-0}; B=${4:-$N}; S=$(( (B-A+2)/3 ))
node "$HERE/render.js" "$P" full $A $((A+S)) > "$P/r1.log" 2>&1 &
node "$HERE/render.js" "$P" full $((A+S)) $((A+2*S)) > "$P/r2.log" 2>&1 &
node "$HERE/render.js" "$P" full $((A+2*S)) $B > "$P/r3.log" 2>&1 &
wait
grep -h "PAGE ERROR" "$P"/r?.log && exit 1 || true
python3 "$HERE/audio.py" "$P"
ffmpeg -v error -y -framerate 30 -i "$P/frames/f%05d.jpg" -i "$P/mix.wav" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -profile:v high -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
