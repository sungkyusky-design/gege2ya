#!/usr/bin/env bash
# 웹(브라우저) 버전 확인: pygbag로 웹 버전을 띄우고, Playwright(크로미움)로 열어서
# 메뉴 -> 총게임 -> 시작 화면 -> (모드 키) -> 로드아웃 -> 게임까지 눌러 보고 스크린샷과 오류를 확인해요.
#
# 실행 (저장소 맨 위 폴더에서):
#   bash .claude/skills/strike-zone-dev/scripts/web_smoke.sh            # 캠페인
#   bash .claude/skills/strike-zone-dev/scripts/web_smoke.sh z          # 좀비 모드
#   bash .claude/skills/strike-zone-dev/scripts/web_smoke.sh o          # 미션
# 필요: pip install pygbag==0.9.3, node + playwright (클라우드 환경에는 이미 있어요)
# 결과: /tmp/strike_web/ 에 web_menu.png, web_loadout.png, web_game.png
set -e
MODE_KEY="${1:-Enter}"
OUT=/tmp/strike_web
rm -rf "$OUT" && mkdir -p "$OUT/app"
cp browser.py build_info.py game.py main.py shooter.py "$OUT/app/"
cd "$OUT/app"
(timeout 300 python -m pygbag --ume_block 0 . > "$OUT/pygbag.log" 2>&1 &)
cd "$OUT"
for i in $(seq 1 60); do
  curl -s -o /dev/null --noproxy localhost localhost:8000/ && break
  sleep 3
done
cat > "$OUT/smoke.js" <<EOF
const { chromium } = require('playwright');
(async () => {
  const opts = process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY, bypass: 'localhost,127.0.0.1' } } : {};
  const b = await chromium.launch(opts);
  const p = await b.newPage({ viewport: { width: 1100, height: 720 } });
  const errs = [];
  p.on('console', m => { const t = m.text(); if (/Traceback|Error|error:/.test(t) && !/BrowserFS|MEDIA|Failed to load resource/.test(t)) errs.push(t); });
  await p.goto('http://localhost:8000/', { waitUntil: 'load' });
  await p.waitForTimeout(25000);
  await p.keyboard.press('Enter'); await p.waitForTimeout(6000);           // pygbag 시작 화면
  await p.screenshot({ path: 'web_menu.png' });
  await p.keyboard.press('2'); await p.waitForTimeout(2500);               // 게임 메뉴에서 총게임
  await p.keyboard.press('${MODE_KEY}'); await p.waitForTimeout(2500);     // 모드 고르기
  if ('${MODE_KEY}' === 'o') { await p.keyboard.press('Enter'); await p.waitForTimeout(2000); }
  await p.screenshot({ path: 'web_loadout.png' });
  await p.keyboard.press('Enter'); await p.waitForTimeout(8000);           // 로드아웃 -> 게임
  await p.keyboard.down('f'); await p.waitForTimeout(1200); await p.keyboard.up('f');
  await p.screenshot({ path: 'web_game.png' });
  console.log('browser errors:', errs.slice(-5).join('\n') || 'none');
  await b.close();
})();
EOF
NODE_PATH="$(npm root -g 2>/dev/null)" timeout 200 node "$OUT/smoke.js"
echo "screenshots: $OUT/web_menu.png $OUT/web_loadout.png $OUT/web_game.png"
