# ベースは同じリポジトリの rocky9 イメージ。
ARG BASE_IMAGE=rocky9:latest
FROM ${BASE_IMAGE}

ENV GOROOT=/opt/go
ENV GOPATH=/go
ENV PATH=${PATH}:${GOROOT}/bin:${GOPATH}/bin

# --- 取得ステージ ------------------------------------------------------------
# --- Go ----------------------------------------------------------------------
ARG GO_VERSION=1.27.3
ARG GO_SHA256=a06e99309dbcbdca1a8ccd2282c3ee146e55930886e26b4f1193269587165f49
RUN set -eu; \
    curl -fsSL -o /tmp/go.tar.gz \
      "https://go.dev/dl/go${GO_VERSION}.linux-arm64.tar.gz"; \
    echo "${GO_SHA256}  /tmp/go.tar.gz" | sha256sum -c -; \
    tar -C /opt -xzf /tmp/go.tar.gz; \
    rm /tmp/go.tar.gz

# --- golangci-lint -----------------------------------------------------------
ARG GOLANGCI_LINT_VERSION=2.13.2
ARG GOLANGCI_LINT_SHA256=a2a4e0065aa41be71f7c5ac90f271b61751331e5d04314e62afe4027855f0893
RUN set -eu; \
    dir="golangci-lint-${GOLANGCI_LINT_VERSION}-linux-arm64"; \
    curl -fsSL -o /tmp/golangci-lint.tar.gz \
      "https://github.com/golangci/golangci-lint/releases/download/v${GOLANGCI_LINT_VERSION}/${dir}.tar.gz"; \
    echo "${GOLANGCI_LINT_SHA256}  /tmp/golangci-lint.tar.gz" | sha256sum -c -; \
    tar -C /tmp -xzf /tmp/golangci-lint.tar.gz; \
    mkdir -p /go/bin; \
    mv "/tmp/${dir}/golangci-lint" "${GOPATH}/bin/golangci-lint"; \
    rm -rf /tmp/golangci-lint.tar.gz "/tmp/${dir}"
