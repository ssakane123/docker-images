# ベースは同じリポジトリの rocky9 イメージ
ARG BASE_IMAGE=rocky9:latest
FROM ${BASE_IMAGE}

ARG PYTHON_VERSION=3.14


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


# ENTRYPOINT はベースの ["/tini", "--"] をそのまま継承する。
CMD ["python", "--version"]
