ARG BUILD_FROM=python:3.13-slim-bookworm
FROM ${BUILD_FROM}

ARG BUILD_ARCH=amd64
ARG SPOTDL_VERSION=4.6.0
ARG DENO_VERSION=v2.9.8

# ffmpeg converts to MP3; yt-dlp needs Deno to read YouTube's player.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip ca-certificates \
    && case "${BUILD_ARCH}" in \
        amd64) deno_target=x86_64-unknown-linux-gnu ;; \
        aarch64) deno_target=aarch64-unknown-linux-gnu ;; \
        *) echo "Unsupported architecture: ${BUILD_ARCH}" >&2; exit 1 ;; \
       esac \
    && curl -fsSL "https://dl.deno.land/release/${DENO_VERSION}/deno-${deno_target}.zip" -o /tmp/deno.zip \
    && unzip /tmp/deno.zip -d /usr/local/bin \
    && rm /tmp/deno.zip \
    && apt-get purge -y curl unzip \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "spotdl==${SPOTDL_VERSION}" "yt-dlp[default]"

# spotDL keeps its cache and settings in ~/.spotdl; /data survives restarts and updates.
ENV HOME=/data
COPY run.py /app/run.py
CMD ["python3", "/app/run.py"]
