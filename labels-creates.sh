#!/usr/bin/env bash
set -e
repo="$1" # Optional parameter: OWNER/REPO
if [ -z "$repo" ]; then
  echo "usage: ./labels-create.sh OWNER/REPO"
  exit 1
fi

labels=(
  "PBI:#0e8a16:Product Backlog Item"
  "bug:#d73a4a:Bug/Defect"
  "status:backlog:#e0e0e0:Backlog Stage"
  "status:ready:#0366d6:Ready"
  "status:in-progress:#fbca04:In Development"
  "status:in-review:#6f42c1:Acceptance/Review"
  "status:done:#0e8a16:Completed"
  "component:frontend:#1d76db:Frontend"
  "component:backend:#0052cc:Backend"
  "component:infra:#006b75:Infrastructure"
)

for item in "${labels[@]}"; do
  IFS=':' read -r name color desc <<< "$item"
  gh label create "$name" --color "${color//#/}" --description "$desc" --repo "$repo" || echo "label $name may already exist"
done

echo "labels created/checked for $repo"