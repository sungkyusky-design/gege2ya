#!/usr/bin/env bash
# 배포 확인: main에 병합한 뒤, GitHub Actions가 새 exe / 맥 앱을 다 만들었는지 확인해요.
# 릴리스의 version.txt가 병합 커밋 번호(앞 7자리)와 같아지면 끝난 거예요 (보통 5~10분).
#
# 실행:
#   bash .claude/skills/strike-zone-dev/scripts/release_check.sh <병합 커밋 sha>
URL=https://github.com/sungkyusky-design/gege2ya/releases/latest/download/version.txt
SHA="${1:?병합 커밋 sha를 넣어 주세요}"
SHORT="${SHA:0:7}"
for i in $(seq 1 60); do
  v=$(curl -sL "$URL" 2>/dev/null | head -c 20)
  if [ "$v" = "$SHORT" ]; then
    echo "ready: release version $v"
    echo "Mac:     https://github.com/sungkyusky-design/gege2ya/releases/latest/download/Games-mac.zip"
    echo "Windows: https://github.com/sungkyusky-design/gege2ya/releases/latest/download/Games.exe"
    exit 0
  fi
  sleep 15
done
echo "not ready after 15 minutes (release version: ${v:-unknown}). Check the Actions tab."
exit 1
