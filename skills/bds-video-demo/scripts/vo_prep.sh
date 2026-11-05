#!/usr/bin/env bash
# Chuẩn hoá giọng đọc và in các khoảng lặng để căn đồ hoạ theo từng cụm từ.
#   bash vo_prep.sh <projectDir> [tempo=1.06]
# Vào: <project>/vo/s1.wav, s2.wav ... (mỗi đoạn lời 1 file). Ra: <project>/vo/f1.wav ... (48 kHz mono, đã tăng tốc)
# In ra: thời lượng mỗi đoạn + silence_start/end (giây, theo file đã tăng tốc) -> dùng để đặt mốc trong timeline.js / render.html
set -e
P="$1"; T="${2:-1.06}"
for s in "$P"/vo/s*.wav; do
  n=$(basename "$s" .wav); n=${n#s}
  ffmpeg -v error -y -i "$s" -af "atempo=$T,aresample=48000" -ar 48000 -ac 1 "$P/vo/f$n.wav"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$P/vo/f$n.wav")
  echo "== f$n.wav  dur=$d"
  ffmpeg -i "$P/vo/f$n.wav" -af silencedetect=noise=-38dB:d=0.12 -f null - 2>&1 | grep -oE "silence_(start|end): [0-9.]+" | tr '\n' ' '; echo
done
