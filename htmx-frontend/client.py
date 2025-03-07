import sys

from fasthtml.common import (
    Div,
    FastHTML,
    Form,
    Input,
    Script,
    Titled,
)


if __name__ == "__main__":
    sys.exit("Run this app with `uvicorn main:app`")

htmx_ws = Script(src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js")
app = FastHTML(exts="ws")
rt = app.route


@app.ws("/ws")
async def ws(msg: str, send):
    """
    WebSocket handler that will be overridden in main.py
    to integrate with Preswald service
    """
    # This implementation will be replaced in main.py
    await send(f"Echo: {msg}")


@app.get("/")
def home():
    cts = Div(
        Div(id="notifications"),
        Form(
            Input(id="msg", placeholder="Type a message..."),
            Input(type="submit", value="Send"),
            id="form",
            ws_send=True,
        ),
        Div(id="preswald-content", style="margin-top: 20px;"),
        hx_ext="ws",
        ws_connect="/ws",
    )
    return Titled("Preswald WebSocket Test", cts)
