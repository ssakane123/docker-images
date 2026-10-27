ARG ROCKY_BASE_IMAGE=docker.io/rockylinux/rockylinux:9
FROM ${ROCKY_BASE_IMAGE}

# --- ツールチェーン ------------------------------------------------
RUN dnf -y --refresh --setopt=install_weak_deps=False upgrade \
    && dnf -y --allowerasing --setopt=install_weak_deps=False install \
        gcc cpp make m4 patch \
        binutils gdb-minimal pkgconf-pkg-config libtool-ltdl \
        rpm-build rpmdevtools redhat-rpm-config \
        git vim-enhanced \
        python3 python3-pip python3-setuptools perl-interpreter \
        curl wget tar gzip bzip2 xz zip unzip \
        which less file hostname findutils diffutils procps-ng \
        glibc-langpack-en glibc-langpack-ja glibc-gconv-extra gawk-all-langpacks \
        tzdata \
    && dnf clean all \
    && rm -rf /var/cache/dnf


# --- ロケールとタイムゾーン --------------------------------------------------
ENV LANG=en_US.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime


# --- tini -----------------------------------
ARG TINI_VERSION=v0.19.0
ARG TINI_SHA256=07952557df20bfd2a95f9bef198b445e006171969499a1d361bd9e6f8e5e0e81

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-arm64 /tini

RUN set -eu; \
    echo "${TINI_SHA256}  /tini" | sha256sum -c -; \
    chmod +x /tini


ENTRYPOINT ["/tini", "--"]
CMD ["/bin/bash", "--login"]
