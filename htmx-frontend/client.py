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
    pass


@app.get("/")
def home():
    cts = Div(
        Div(id="notifications"),
        Form(Input(id="msg"), id="form", ws_send=True),
        hx_ext="ws",
        ws_connect="/ws",
    )
    return Titled("Websocket Test", cts)
