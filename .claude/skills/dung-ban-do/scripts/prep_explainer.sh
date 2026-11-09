#!/usr/bin/env bash
# prep_explainer.sh <K> [specsDir] — dựng thư mục dự án /tmp/v/<K> từ spec + vo/s1.wav + times.json rồi sinh scene.js/timeline.js
set -e
K="$1"; S="${2:-/home/user/mcp-server-demo/video-demo/videos}"; H="$(cd "$(dirname "$0")" && pwd)"; P=/tmp/v/$K
mkdir -p $P/vo; cd $P
for f in render.html engine.js; do cp /tmp/dn_base/$f .; done; cp -r /tmp/dn_base/fonts . ; ln -sfn /tmp/dn_base/assets assets
[ -f timeline.js ] || cp /tmp/dn_base/timeline.js .
bash $H/vo_prep.sh $P 1.0 > /dev/null
python3 $H/build_explainer.py $S/$K/spec.py $P --times $S/$K/times.json --vo f1.wav --vo-offset 0.5
node --check $P/scene.js && node --check $P/timeline.js
