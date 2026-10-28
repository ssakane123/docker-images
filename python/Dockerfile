# ベースは同じリポジトリの rocky9 イメージ
ARG BASE_IMAGE=rocky9:latest
FROM ${BASE_IMAGE}

ARG PYTHON_VERSION=3.14

ARG UV_VERSION=0.11.11
ARG UV_INSTALLER_SHA256=3a020f8d69019caca567c9038999d130b0ea85866483caf2042c386cb685aef4

# --- Python と CI 用のツール ----------------------------------------
RUN dnf -y --refresh --setopt=install_weak_deps=False install \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-pip \
        git \
        openssh-clients \
    && dnf clean all \
    && rm -rf /var/cache/dnf


# --- python / pip で叩けるようにする -----------------------------------------
RUN ln -sf /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python \
    && ln -sf /usr/bin/pip${PYTHON_VERSION}  /usr/local/bin/pip


# -- uv のインストール ------------------------------------------------
RUN curl -fsSL -o /tmp/uv-install.sh "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-installer.sh" \
    && printf '%s  %s\n' "${UV_INSTALLER_SHA256}" /tmp/uv-install.sh | sha256sum -c - \
    && UV_UNMANAGED_INSTALL=/usr/local/bin sh /tmp/uv-install.sh \
    && rm -f /tmp/uv-install.sh


# ENTRYPOINT はベースの ["/tini", "--"] をそのまま継承する。
CMD ["python", "--version"]
