#!/bin/bash

# Docker Hub username
USERNAME="smbambling"

# Image name
IMAGE_NAME="check-kubernetes-cronjobs"

# Print plugin usage
usage() {
  cat <<EOF
Usage: $0 -b|-r -v
where:
    -b Build Docker image
    -r Build+Release Docker image
    -v Version bump level { major, minor, patch(default) }
EOF
   exit 0
}

# Set Warning and Critical Options
VER_BUMP="patch"
while getopts ":bhrv:" arg; do
  case "${arg}" in
    b)
      [ -n "${BUILDTYPE}" ] && usage || BUILDTYPE='build' ;;
    h) usage ;;
    r)
      [ -n "${BUILDTYPE}" ] && usage || BUILDTYPE='release' ;;
    v)
      VER_BUMP="${OPTARG}"
      ;;
    "?") usage ;;
    *) break ;;
  esac
done

bump() {
  # Get current version from VERSION file
  VERSION=$(cat VERSION)

  # Set version field based on version level
  if [ "${VER_BUMP}" == 'patch' ]; then
    VER_FIELD='3'
  elif [ "${VER_BUMP}" == 'minor' ]; then
    VER_FIELD='2'
  elif [ "${VER_BUMP}" == 'major' ]; then
    VER_FIELD='1'
  else
    echo "Could not set VER_FIELD, something went wrong"
    exit 1
  fi

  # Increment the version field based on version level
  VERSION=$(echo "$VERSION" | awk -v field="${VER_FIELD}" -F. '{$field++}1' OFS=.)

  # Update VERSION file
  echo "${VERSION}" > VERSION
}

build() {
  docker build -t "${USERNAME}/${IMAGE_NAME}:latest" .
  if [ -n "${VERSION}" ]; then
    echo "Successfully tagged ${USERNAME}/${IMAGE_NAME}:${VERSION}"
    docker tag "${USERNAME}/${IMAGE_NAME}:latest" "${USERNAME}/${IMAGE_NAME}:${VERSION}"
  fi
}

gittag() {
  git add VERSION
  git commit -m "Release ${VERSION}"
  git tag -a "${VERSION}" -m "release ${VERSION}"
  git push --tags
  git push -u origin master
  git checkout stable
  git merge master
  git push -u origin stable
  git checkout master
}

dockerpush() {
  docker push "${USERNAME}/${IMAGE_NAME}:latest"
  docker push "${USERNAME}/${IMAGE_NAME}:${VERSION}"
}

release() {
  MYBRANCH=$(git rev-parse --abbrev-ref HEAD)
  if [ "${MYBRANCH}" != "master" ]; then
    echo "Refusing to release off non master branch"
    exit 1
  fi
  bump
  build
  # testing
  gittag
  # dockerpush
}

if [[ ! "${VER_BUMP}" =~ ^(major|minor|patch)$ ]]; then
  echo -e "Incorrect version bump level set : ${VER_BUMP}\n"
  usage
fi

if [ "${BUILDTYPE}" == "build" ]; then
  build
  # dockerpush
elif [ "${BUILDTYPE}" == "release" ]; then
  release
else
  echo "ERROR: Not building or release, something went wrong"
  exit 1
fi
