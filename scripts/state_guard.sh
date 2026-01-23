#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:3000}"
TMP_JSON=$(mktemp)
trap 'rm -f "$TMP_JSON"' EXIT

http_code=$(curl -sS -w '%{http_code}' -o "$TMP_JSON" "$BASE/api/Challenges" || true)
if [ "$http_code" != "200" ]; then
  echo "ERROR: Unable to reach $BASE/api/Challenges (HTTP $http_code)" >&2
    exit 2
    fi

    python3 - "$TMP_JSON" <<'PY'
    import json,sys
    p=sys.argv[1]
    with open(p,'r',encoding='utf-8') as f:
      j=json.load(f)
      chs=j.get('data',[])
      hack_total=len(chs)
      coding_total=sum(1 for c in chs if c.get('hasCodingChallenge'))
      hack_solved=sum(1 for c in chs if c.get('solved'))
      coding_solved=sum(1 for c in chs if c.get('codingChallengeStatus')==2)
      unsolved=[c.get('key') for c in chs if not (c.get('solved') or c.get('codingChallengeStatus')==2)]
      print(f"hacking_solved={hack_solved}/{hack_total}")
      print(f"coding_solved={coding_solved}/{coding_total}")
      print(f"total_solved={hack_solved+coding_solved}/{hack_total+coding_total}")
      print("unsolved_keys=\n"+"\n".join(unsolved) if unsolved else "unsolved_keys=<none>")
      print("__ALL_SOLVED__" if (hack_solved==hack_total and coding_solved==coding_total) else "__NOT_ALL__")
      PY

      SENTINEL=$(tail -n1 <<<'') # placeholder to appease shellcheck-like
      SENTINEL=$(python3 - "$TMP_JSON" <<'PY'
      import json,sys
      chs=json.load(open(sys.argv[1])).get('data',[])
      print("__ALL_SOLVED__" if (sum(1 for c in chs if c.get('solved'))==len(chs) and sum(1 for c in chs if c.get('codingChallengeStatus')==2)==sum(1 for c in chs if c.get('hasCodingChallenge'))) else "__NOT_ALL__")
      PY
      )

      if [ "$SENTINEL" = "__ALL_SOLVED__" ] && [ "${FORCE:-}" != "1" ]; then
        echo "GUARD: Instance appears fully solved. Refusing to proceed. Set FORCE=1 to override." >&2
          exit 3
          fi

          echo "GUARD: Proceeding (not fully solved or FORCE=1)."
