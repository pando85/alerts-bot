ARG BASE_IMAGE_PREFIX
FROM ${BASE_IMAGE_PREFIX}python:3

# see hooks/post_checkout
ARG ARCH

# HACK: don't fail when no qemu binary provided
COPY .gitignore qemu-${ARCH}-static* /usr/bin/

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alerts_bot ./alerts_bot

CMD [ "python", "-m", "alerts_bot" ]
