#!/usr/bin/env bash
# Dedicated Actions checkout only. No queue, lease, or video writes.
set -euo pipefail
branch="${BRANCH:-main}"
if [[ "$branch" != main ]]; then
  echo 'Site alerts publish only from main.' >&2
  exit 1
fi

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'

publish_state() {
  if [[ -z "$(git status --porcelain -- ops/site-alert-state.json)" ]]; then
    return 0
  fi
  git add ops/site-alert-state.json || exit 1
  git commit -m "$1" || exit 1
  git push origin HEAD:main
}

for attempt in 1 2 3 4; do
  # Any fetch/reset failure must stop, not send using a stale canonical snapshot.
  git fetch origin main
  git reset --hard origin/main
  python3 scripts/site_alerts.py . --prepare
  if ! publish_state 'Site alerts: publish delivery intent before Relay'; then
    echo "Prepare CAS rejected ($attempt/4); no message sent."
    continue
  fi
  # Read back remote canonical state before sending, including concurrent updates.
  git fetch origin main
  git reset --hard origin/main
  # V2 receiver can now verify the exact incident in canonical main.
  if ! python3 scripts/site_alerts.py . --notify; then
    echo "Prepared state changed before notify ($attempt/4); recompute from fresh main."
    continue
  fi
  if publish_state 'Site alerts: persist delivery receipt'; then
    exit 0
  fi
  echo "Receipt CAS rejected ($attempt/4); recompute from fresh main."
done

echo '::error title=site-alerts::could not persist delivery state after four CAS attempts'
exit 1
