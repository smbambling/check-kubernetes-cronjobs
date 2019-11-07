#!/bin/bash

# Print plugin usage
usage() {
  cat <<EOF
Usage: $0 -k -n
where:
    -k Kubeconfig
      [default: $HOME/.kube/config]
    -n Kubernetes Namespace {required}
    -v check-kubernetes-cronjobs Docker image version
      [default: latest]
EOF
   exit 0
}

# Image name
IMAGE_NAME="smbambling/check-kubernetes-cronjobs"

# Set Warning and Critical Options
KUBECONFIG="$HOME/.kube/config"
VERSION="latest"
while getopts ":k:n:v:" arg; do
  case "${arg}" in
    k) KUBECONFIG=${OPTARG} ;;
    n) NAMESPACE=${OPTARG} ;;
    v) VERSION=${OPTARG} ;;
    "?") usage ;;
    *) break ;;
  esac
done

if [ -z "${NAMESPACE}" ]; then
  echo "Missing option -n NAMESPACE"
  usage
fi

docker run --rm -it --hostname check-kubernetes-cronjobs \
-v "${KUBECONFIG}":/root/.kube/config \
"${IMAGE_NAME}":"${VERSION}" --namespace "${NAMESPACE}"
