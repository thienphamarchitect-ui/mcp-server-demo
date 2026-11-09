#!/usr/bin/env python3
"""save_tts.py <file kết quả audio_synthesize> <project> -> <project>/vo/s1.wav; in thời lượng và link ký (dùng cho audio_transcribe)."""
import sys, json, base64, os
d = json.load(open(sys.argv[1])); P = sys.argv[2]; os.makedirs(P + '/vo', exist_ok=True)
open(P + '/vo/s1.wav', 'wb').write(base64.b64decode(d['audio_base64']))
print(round(d['duration_seconds'], 2)); print(d['url'])
