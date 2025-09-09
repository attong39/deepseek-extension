#!/usr/bin/env bash
# Thiết lập branch protection + required status checks cho main.
# Yêu cầu: gh CLI đăng nhập với quyền admin repo (GH_TOKEN/GITHUB_TOKEN).

set -euo pipefail
: "${GH_REPO:?Env GH_REPO=org/repo chưa đặt}"    # ví dụ: export GH_REPO=myorg/zeta-vn
BRANCH="${1:-main}"

# Bật required status checks: khớp tên workflow/check mà bạn đã cấu hình
CHECKS='["ci-final-gates","consistency-guard"]'

echo "[bp] Set protection for $GH_REPO:$BRANCH"
gh api -X PUT "repos/$GH_REPO/branches/$BRANCH/protection" \
  -H "Accept: application/vnd.github+json" \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts="$CHECKS" \
  -F enforce_admins=true \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F restrictions= | jq -r '.url' >/dev/null

echo "[bp] Done."
