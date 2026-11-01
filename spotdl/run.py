"""Start spotDL's web interface inside Home Assistant, behind ingress."""

import importlib
import json
import os
import re
import sys
import webbrowser
from pathlib import Path, PurePosixPath

from uvicorn import Config

from spotdl.console import console_entry_point

OPTIONS_FILE = Path(os.environ.get("OPTIONS_FILE", "/data/options.json"))
PORT = 8800
INGRESS_PATH = re.compile(rb"^/api/hassio_ingress/[A-Za-z0-9_-]+$")

# spotDL writes absolute URLs into its pages and its server-sent events.
# Behind ingress they must start with the ingress path instead.
REWRITES = (
    (b'"/assets/', b'"%s/assets/'),
    (b'"../assets/', b'"%s/assets/'),
    (b"'/client/", b"'%s/client/"),
    (b"window.location = '/", b"window.location = '%s/"),
    (b"goto('/", b"goto('%s/"),
)
REWRITTEN_TYPES = (b"text/html", b"text/event-stream")


def rewrite(body, prefix):
    for old, new in REWRITES:
        body = body.replace(old, new % prefix)
    return body


class IngressPathMiddleware:
    """Prefixes spotDL's URLs with the X-Ingress-Path that Home Assistant sends."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        prefix = dict(scope["headers"]).get(b"x-ingress-path", b"").rstrip(b"/")
        if not INGRESS_PATH.match(prefix):
            await self.app(scope, receive, send)
            return

        rewriting = False

        async def send_rewritten(message):
            nonlocal rewriting
            if message["type"] == "http.response.start":
                headers = message["headers"]
                content_type = dict(headers).get(b"content-type", b"")
                rewriting = content_type.startswith(REWRITTEN_TYPES)
                if rewriting:
                    headers = [(k, v) for k, v in headers if k != b"content-length"]
                    message = {**message, "headers": headers}
            elif message["type"] == "http.response.body" and rewriting:
                message = {**message, "body": rewrite(message.get("body", b""), prefix)}
            await send(message)

        await self.app(scope, receive, send_rewritten)


def spotdl_arguments(options):
    output_dir = PurePosixPath(options["output_dir"])
    if output_dir.parts[:2] != ("/", "media"):
        sys.exit(f"output_dir must be inside /media, not {output_dir}")

    arguments = [
        "spotdl",
        "web",
        "--host", "0.0.0.0",
        "--port", str(PORT),
        "--keep-alive",
        "--web-use-output-dir",
        "--output", f"{output_dir}/{{artists}} - {{title}}.{{output-ext}}",
        "--format", options["format"],
        "--bitrate", options["bitrate"],
        "--log-level", options["log_level"],
    ]

    client_id = options.get("client_id", "")
    client_secret = options.get("client_secret", "")
    if client_id and client_secret:
        arguments += [
            "--use-official-api",
            "--client-id", client_id,
            "--client-secret", client_secret,
        ]
    elif client_id or client_secret:
        print("client_id and client_secret go together; using spotDL's shared client")

    return arguments


def main():
    options = json.loads(OPTIONS_FILE.read_text(encoding="utf-8"))
    sys.argv = spotdl_arguments(options)

    # The module, not the web() function that spotdl.console exports under the same name.
    web_module = importlib.import_module("spotdl.console.web")
    web_module.Config = lambda app, **kwargs: Config(
        app=IngressPathMiddleware(app), **kwargs
    )
    # There is no browser to open in the container.
    webbrowser.open = lambda *args, **kwargs: False

    console_entry_point()


if __name__ == "__main__":
    main()
