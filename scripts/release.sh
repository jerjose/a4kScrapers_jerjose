#!/bin/bash

token=$1
ver=$(echo "$2" | sed "s/release: //")
user="jerjose"
repo="a4kScrapers_jerjose"
tag_ver="${ver#?}"
tag="a4kScrapers_jerjose-$tag_ver"
api="https://api.github.com/repos/$user/$repo"

generate_release_data()
{
  cat <<EOF
{
  "tag_name": "$tag",
  "name": "$ver"
}
EOF
}

post_data="$(generate_release_data)"

echo "Create release"
echo "$post_data"

curl \
    --header "Authorization: token $token" \
    --header "Accept: application/vnd.github.v3+json" \
    --data "$post_data" \
    "$api/releases"
