#!/usr/bin/env bash
# Transfer the repositories selected by this workspace; GitHub keeps their identities.
set -euo pipefail

source_owner=AfonenkoA
target_owner=Afonenko-QCL-NEGF
mode=plan
workspace=$PWD
usage() {
  cat <<'EOF'
Usage: bash ops/transfer-github.sh [--plan|--apply|--sync-local] [--root DIRECTORY]
  --plan        Read-only preflight and transfer command preview (default).
  --apply       Transfer components, then qcl-negf; wait for completion; sync remotes.
  --sync-local  Verify completed transfers and update only local Git configuration.
Requires Bash 4+, git and authenticated gh. Run from a qcl-negf checkout.
EOF
}
die() { printf '%s\n' "ERROR: $*" >&2; exit 1; }
while (($#)); do
  case "$1" in
    --plan|--apply|--sync-local) mode=${1#--}; shift ;;
    --root) (($# >= 2)) || die '--root requires a directory'; workspace=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; die "Unknown argument: $1" ;;
  esac
done
command -v git >/dev/null || die 'git is required'
command -v gh >/dev/null || die 'gh is required; run gh auth login --hostname github.com'
workspace=$(git -C "$workspace" rev-parse --show-toplevel)
[[ -f "$workspace/.gitmodules" ]] || die 'No .gitmodules in the selected checkout'
export GH_PROMPT_DISABLED=1
export GH_PAGER=cat
gh auth status --hostname github.com
org=$(gh api --hostname github.com "orgs/$target_owner" --jq .login)
[[ ${org,,} == ${target_owner,,} ]] || die 'Target organization identity mismatch'
errors=$(mktemp)
trap 'rm -f "$errors"' EXIT

# Distinguish a confirmed 404 from authentication, policy, network and server errors.
# Prefix the selected metadata so HTTP headers cannot be mistaken for a repository.
repository_info() {
  local repository=$1 output status='' record='' line code=0 marker
  output=$(gh api --hostname github.com --include "repos/$repository" \
    --jq '"REPO\t\(.id)\t\(.full_name)\t\(.permissions.admin // false)\t\(.archived)"' \
    2>"$errors") || code=$?
  while IFS= read -r line; do
    line=${line%$'\r'}
    if [[ $line =~ ^HTTP/[0-9.]+\ ([0-9]{3})(\ |$) ]]; then status=${BASH_REMATCH[1]}; fi
    if [[ $line == REPO$'\t'* ]]; then record=$line; fi
  done <<< "$output"
  if [[ $status == 404 && $code != 0 ]]; then return 1; fi
  if [[ $status != 200 || $code != 0 || -z $record ]]; then
    cat "$errors" >&2
    die "Cannot inspect $repository (HTTP ${status:-unknown}); nothing inferred from this failure"
  fi
  IFS=$'\t' read -r marker repo_id repo_full repo_admin repo_archived <<< "$record"
  [[ $repo_id =~ ^[0-9]+$ && $repo_full == */* ]] || die "Malformed metadata for $repository"
}

declare -a names=() paths=() sections=() ids=() states=()
declare -A seen=()
configured=$(git -C "$workspace" config -f .gitmodules --get-regexp '^submodule\..*\.path$')
while read -r key path; do
  [[ $path =~ ^components/[A-Za-z0-9][A-Za-z0-9_.-]*$ ]] || die "Unexpected submodule path: $path"
  name=${path#components/}
  [[ $name != qcl-negf && ! ${seen[$name]+yes} ]] || die "Duplicate repository: $name"
  url=$(git -C "$workspace" config -f .gitmodules --get "${key%.path}.url")
  valid=false
  for owner in "$source_owner" "$target_owner"; do
    for suffix in '' .git; do
      [[ $url == "https://github.com/$owner/$name$suffix" || \
         $url == "git@github.com:$owner/$name$suffix" ]] && valid=true
    done
  done
  [[ $valid == true ]] || die "Unexpected submodule origin: $url"
  seen[$name]=1
  names+=("$name"); paths+=("$path"); sections+=("${key%.path}")
done <<< "$configured"
((${#names[@]} > 0)) || die 'No component repositories found'
names+=(qcl-negf); paths+=(.); sections+=('')

# A local fork or an unrelated checkout must not have its origin silently replaced.
for i in "${!names[@]}"; do
  name=${names[$i]}; path=${paths[$i]}
  [[ $path == . || -e "$workspace/$path/.git" ]] || continue
  url=$(git -C "$workspace/$path" config --get remote.origin.url)
  valid=false
  for owner in "$source_owner" "$target_owner"; do
    for suffix in '' .git; do
      [[ $url == "https://github.com/$owner/$name$suffix" || \
         $url == "git@github.com:$owner/$name$suffix" ]] && valid=true
    done
  done
  [[ $valid == true ]] || die "Unexpected local origin for $path: $url"
done

# Inspect the entire graph before the first transfer. Redirects are checked by ID.
for i in "${!names[@]}"; do
  name=${names[$i]}
  old_id='' old_full='' old_admin='' old_archived=''
  new_id='' new_full=''
  if repository_info "$source_owner/$name"; then
    old_id=$repo_id; old_full=$repo_full; old_admin=$repo_admin; old_archived=$repo_archived
  fi
  if repository_info "$target_owner/$name"; then new_id=$repo_id; new_full=$repo_full; fi
  [[ -n $old_id ]] || die "Original repository $source_owner/$name is inaccessible; identity cannot be verified"
  if [[ -n $new_id ]]; then
    [[ $new_full == "$target_owner/$name" && $new_id == "$old_id" && \
       $old_full == "$new_full" ]] || die "Target name is occupied by a different repository: $target_owner/$name"
    states+=(done)
  else
    [[ $old_full == "$source_owner/$name" ]] || die "Unexpected current owner: $old_full"
    [[ $old_admin == true && $old_archived == false ]] || die "An active repository with admin access is required: $old_full"
    states+=(pending)
  fi
  ids+=("$old_id")
  printf '%-24s %-7s %s -> %s\n' "$name" "${states[$i]}" "$source_owner" "$target_owner"
done

if [[ $mode == plan ]]; then
  for i in "${!names[@]}"; do
    [[ ${states[$i]} == pending ]] || continue
    printf 'gh api --hostname github.com --method POST repos/%s/%s/transfer -f new_owner=%s\n' \
      "$source_owner" "${names[$i]}" "$target_owner"
  done
  printf '%s\n' 'No repositories or local remotes changed. Use --apply to execute this plan.'
  exit 0
fi

for i in "${!names[@]}"; do
  name=${names[$i]}
  [[ ${states[$i]} == pending ]] || continue
  [[ $mode == apply ]] || die "Transfer is incomplete for $name; run --apply first"
  # Recheck immediately before POST; never submit a transfer to an unrelated identity.
  repository_info "$source_owner/$name" || die "Repository disappeared: $source_owner/$name"
  [[ $repo_id == "${ids[$i]}" ]] || die "Repository identity changed: $name"
  if [[ $repo_full == "$source_owner/$name" ]]; then
    gh api --hostname github.com --method POST "repos/$source_owner/$name/transfer" \
      -f "new_owner=$target_owner" --silent
  elif [[ $repo_full != "$target_owner/$name" ]]; then
    die "Repository moved to an unexpected owner: $repo_full"
  fi
  complete=false
  for ((attempt=0; attempt<20; attempt++)); do
    if repository_info "$target_owner/$name"; then
      [[ $repo_id == "${ids[$i]}" && $repo_full == "$target_owner/$name" ]] || die "Transferred repository identity mismatch: $name"
      complete=true; break
    fi
    sleep 3
  done
  [[ $complete == true ]] || die "Transfer of $name is still pending; inspect GitHub and rerun --plan before retrying"
  printf 'Transferred %s/%s (repository ID %s)\n' "$target_owner" "$name" "${ids[$i]}"
done

# Do not change tracked .gitmodules, worktrees, branches, gitlinks or release tags.
# HTTPS supports public reads; the explicit push URL uses the operator's SSH key.
for i in "${!names[@]}"; do
  name=${names[$i]}; path=${paths[$i]}
  fetch_url="https://github.com/$target_owner/$name.git"
  push_url="git@github.com:$target_owner/$name.git"
  if [[ -n ${sections[$i]} ]]; then
    git -C "$workspace" config "${sections[$i]}.url" "$fetch_url"
  fi
  if [[ $path != . && ! -e "$workspace/$path/.git" ]]; then
    printf 'Uninitialized submodule %s: URL recorded for future checkout\n' "$path"
    continue
  fi
  git -C "$workspace/$path" config --replace-all remote.origin.url "$fetch_url"
  git -C "$workspace/$path" config --replace-all remote.origin.pushurl "$push_url"
done
printf '%s\n' 'Transfers verified; local HTTPS fetch / SSH push URLs updated. Merge the coordinated PRs next.'
