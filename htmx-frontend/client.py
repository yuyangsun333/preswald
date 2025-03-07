import json
import re
import sys
from typing import Any, Dict

from fasthtml.common import (
    H1,
    Button,
    Div,
    FastHTML,
    P,
    Script,
    Titled,
)


if __name__ == "__main__":
    sys.exit("Run this app with `uvicorn main:app`")

# Create FastHTML app
app = FastHTML()

# Add HTMX for other features
htmx_js = Script(src="https://unpkg.com/htmx.org@1.9.10")

# Add Tailwind CSS for styling
tailwind_css = Script(src="https://cdn.tailwindcss.com")

# Add Plotly for charts
plotly_js = Script(src="https://cdn.plot.ly/plotly-latest.min.js")

# Direct WebSocket connection script
websocket_script = Script("""
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up WebSocket connection');

    const display = document.getElementById('components-display');
    let socket = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;

    function connectWebSocket() {
        // Create WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = protocol + '//' + window.location.host + '/ws';
        console.log('Connecting to WebSocket at:', wsUrl);

        // Show connecting status
        display.innerHTML = `
            <div class="text-center my-10">
                <p class="text-gray-500">Connecting to Preswald...</p>
                <p class="text-xs text-gray-400 mt-2">WebSocket URL: ${wsUrl}</p>
            </div>
        `;

        try {
            socket = new WebSocket(wsUrl);
            window.wsSocket = socket;

            // Connection opened
            socket.addEventListener('open', function(event) {
                console.log('WebSocket connection opened');
                reconnectAttempts = 0;

                // Show connection status
                const statusDiv = document.createElement('div');
                statusDiv.className = 'fixed bottom-4 right-4 bg-green-100 border-l-4 border-green-500 text-green-700 p-4';
                statusDiv.innerHTML = 'WebSocket connected';
                document.body.appendChild(statusDiv);

                // Remove the status message after 3 seconds
                setTimeout(() => {
                    if (document.body.contains(statusDiv)) {
                        document.body.removeChild(statusDiv);
                    }
                }, 3000);

                // Send empty message to get initial data
                console.log('Sending empty message to get initial data');
                socket.send('');
            });

            // Listen for messages
            socket.addEventListener('message', function(event) {
                console.log('WebSocket message received, length:', event.data.length);
                if (event.data.length < 1000) {
                    console.log('Message content:', event.data);
                } else {
                    console.log('First 500 chars:', event.data.substring(0, 500));
                }

                try {
                    // Check if the message is a simple response (like "pong")
                    if (event.data === "pong") {
                        console.log('Received pong response');
                        return;
                    }

                    // Replace the entire content with the HTML received
                    display.innerHTML = event.data;
                    console.log('Updated display with received HTML');

                    // Initialize any Plotly charts if present
                    initializePlotly();

                    // Initialize interactive elements
                    initializeInteractiveElements();
                } catch (e) {
                    console.error('Error processing message:', e);
                    display.innerHTML = `
                        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                            <p class="font-bold">Error processing message</p>
                            <p>${e.message}</p>
                            <pre class="mt-2 text-xs overflow-auto max-h-40">${event.data.substring(0, 500)}...</pre>
                        </div>
                    `;
                }
            });

            // Connection closed
            socket.addEventListener('close', function(event) {
                console.log('WebSocket connection closed, code:', event.code, 'reason:', event.reason);

                // Show disconnection status
                const statusDiv = document.createElement('div');
                statusDiv.className = 'fixed bottom-4 right-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4';
                statusDiv.innerHTML = 'WebSocket disconnected. Reconnecting...';
                document.body.appendChild(statusDiv);

                // Update the display with connection status
                display.innerHTML = `
                    <div class="text-center my-10">
                        <p class="text-yellow-500 font-bold">WebSocket disconnected</p>
                        <p class="text-gray-500 mt-2">Attempting to reconnect (${reconnectAttempts+1}/${maxReconnectAttempts})...</p>
                        <button onclick="window.location.reload()" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Refresh Page
                        </button>
                    </div>
                `;

                // Try to reconnect if not at max attempts
                if (reconnectAttempts < maxReconnectAttempts) {
                    reconnectAttempts++;
                    console.log(`Reconnect attempt ${reconnectAttempts}/${maxReconnectAttempts}`);
                    setTimeout(connectWebSocket, 2000);
                } else {
                    console.log('Max reconnect attempts reached');
                    display.innerHTML = `
                        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                            <p class="font-bold">Connection lost</p>
                            <p>Unable to reconnect to the server after ${maxReconnectAttempts} attempts.</p>
                            <button onclick="window.location.reload()" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                                Refresh Page
                            </button>
                        </div>
                    `;
                }
            });

            // Connection error
            socket.addEventListener('error', function(event) {
                console.error('WebSocket error:', event);
                display.innerHTML = `
                    <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                        <p class="font-bold">WebSocket error</p>
                        <p>An error occurred with the WebSocket connection.</p>
                        <button onclick="window.location.reload()" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Refresh Page
                        </button>
                    </div>
                `;
            });

            // Set up a ping interval to keep the connection alive
            const pingInterval = setInterval(() => {
                if (socket && socket.readyState === WebSocket.OPEN) {
                    socket.send('ping');
                    console.log('Sent ping to keep connection alive');
                } else {
                    clearInterval(pingInterval);
                }
            }, 30000);

            return socket;
        } catch (e) {
            console.error('Error creating WebSocket:', e);
            display.innerHTML = `
                <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                    <p class="font-bold">Error creating WebSocket connection</p>
                    <p>${e.message}</p>
                    <button onclick="window.location.reload()" class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Refresh Page
                    </button>
                </div>
            `;
            return null;
        }
    }

    // Start the WebSocket connection
    connectWebSocket();

    // Set up functions for component updates
    window.sendComponentUpdate = function(id, value) {
        console.log('Sending component update:', id, value);
        if (socket && socket.readyState === WebSocket.OPEN) {
            const message = JSON.stringify({
                id: id,
                value: value
            });
            socket.send(message);
        } else {
            console.error('Cannot send update - WebSocket not connected');
            alert('Cannot send update - WebSocket not connected. Please refresh the page.');
        }
    };

    window.refreshComponents = function() {
        console.log('Refreshing components');
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send('{}');

            // Show refreshing status
            const statusDiv = document.createElement('div');
            statusDiv.className = 'fixed bottom-4 right-4 bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4';
            statusDiv.innerHTML = 'Refreshing components...';
            document.body.appendChild(statusDiv);

            // Remove the status message after 2 seconds
            setTimeout(() => {
                if (document.body.contains(statusDiv)) {
                    document.body.removeChild(statusDiv);
                }
            }, 2000);
        } else {
            console.error('Cannot refresh - WebSocket not connected');
            alert('Cannot refresh - WebSocket not connected. Please refresh the page.');
        }
    };
});

function initializePlotly() {
    // Initialize any Plotly charts if present
    const plotElements = document.querySelectorAll('[data-plotly]');
    console.log('Found', plotElements.length, 'plot elements');
    plotElements.forEach(el => {
        try {
            const plotData = JSON.parse(el.getAttribute('data-plotly'));
            Plotly.newPlot(el.id, plotData.data, plotData.layout, plotData.config);
        } catch (e) {
            console.error('Error rendering plot:', e);
        }
    });
}

function initializeInteractiveElements() {
    // Handle sliders
    document.querySelectorAll('input[type="range"]').forEach(slider => {
        const valueDisplay = document.getElementById(`${slider.id}-value`);
        if (valueDisplay) {
            valueDisplay.textContent = slider.value;
            slider.addEventListener('input', () => {
                valueDisplay.textContent = slider.value;
            });
        }
    });
}
""")

# Debug script for troubleshooting
debug_script = Script("""
function debugConnection() {
    console.log('Debug button clicked');

    // Create debug info container
    const debugInfo = document.createElement('div');
    debugInfo.className = 'bg-gray-100 p-4 rounded my-4';
    debugInfo.innerHTML = '<h3 class="font-bold mb-2">WebSocket Debug Information</h3>';

    // Check WebSocket connection
    if (window.wsSocket) {
        const readyState = window.wsSocket.readyState;
        const stateText = ['Connecting', 'Open', 'Closing', 'Closed'][readyState];
        debugInfo.innerHTML += `<p>WebSocket state: ${stateText} (${readyState})</p>`;
        debugInfo.innerHTML += `<p>WebSocket URL: ${window.wsSocket.url}</p>`;

        // Try to send a test message if the connection is open
        if (readyState === 1) {
            debugInfo.innerHTML += "<p>WebSocket is open, sending test message...</p>";
            try {
                window.wsSocket.send('debug-ping');
                debugInfo.innerHTML += "<p class='text-green-500'>✓ Test message sent</p>";
            } catch (e) {
                debugInfo.innerHTML += `<p class='text-red-500'>✗ Error sending test message: ${e.message}</p>`;
            }
        } else {
            // Try to reconnect
            debugInfo.innerHTML += "<p>WebSocket is not open. Attempting to reconnect...</p>";
            try {
                // Create a new WebSocket connection
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = protocol + '//' + window.location.host + '/ws';
                const newSocket = new WebSocket(wsUrl);

                newSocket.addEventListener('open', function() {
                    debugInfo.innerHTML += "<p class='text-green-500'>✓ New connection established!</p>";
                    window.wsSocket = newSocket;
                    newSocket.send('');
                });

                newSocket.addEventListener('error', function(e) {
                    debugInfo.innerHTML += `<p class='text-red-500'>✗ Error creating new connection: ${e}</p>`;
                });
            } catch (e) {
                debugInfo.innerHTML += `<p class='text-red-500'>✗ Error attempting reconnect: ${e.message}</p>`;
            }
        }
    } else {
        debugInfo.innerHTML += "<p class='text-red-500'>✗ No WebSocket connection found</p>";

        // Try to create a new connection
        debugInfo.innerHTML += "<p>Attempting to create a new connection...</p>";
        try {
            // Create a new WebSocket connection
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = protocol + '//' + window.location.host + '/ws';
            debugInfo.innerHTML += `<p>Connecting to: ${wsUrl}</p>`;

            const newSocket = new WebSocket(wsUrl);

            newSocket.addEventListener('open', function() {
                debugInfo.innerHTML += "<p class='text-green-500'>✓ New connection established!</p>";
                window.wsSocket = newSocket;
                newSocket.send('');
            });

            newSocket.addEventListener('error', function(e) {
                debugInfo.innerHTML += `<p class='text-red-500'>✗ Error creating new connection: ${e}</p>`;
            });
        } catch (e) {
            debugInfo.innerHTML += `<p class='text-red-500'>✗ Error creating connection: ${e.message}</p>`;
        }
    }

    // Add browser information
    debugInfo.innerHTML += "<h3 class='font-bold mt-4 mb-2'>Browser Information</h3>";
    debugInfo.innerHTML += `<p>User Agent: ${navigator.userAgent}</p>`;
    debugInfo.innerHTML += `<p>WebSocket Support: ${window.WebSocket ? 'Yes' : 'No'}</p>`;

    // Add the debug info to the page
    const display = document.getElementById('components-display');
    display.prepend(debugInfo);
}
""")


def render_components(components_data: Dict[str, Any]) -> str:
    """
    Render Preswald components as HTML
    """
    if not components_data or "components" not in components_data:
        return "<p class='text-red-500'>No components data available</p>"

    html = []
    html.append("<div class='container mx-auto px-4 py-8'>")

    rows = components_data.get("components", {}).get("rows", [])
    for row in rows:
        html.append("<div class='flex flex-wrap -mx-2 mb-6'>")

        for component in row:
            comp_type = component.get("type")
            flex_value = component.get("flex", 1)
            width_class = f"w-full md:w-{int(flex_value * 12 / len(row))}/12 px-2 mb-4"

            html.append(f"<div class='{width_class}'>")
            component_html = render_component_html(comp_type, component)
            html.append(component_html)
            html.append("</div>")

        html.append("</div>")

    html.append("</div>")
    return "".join(html)


def render_component_html(comp_type: str, component: Dict[str, Any]) -> str:  # noqa: C901
    """Render a single component as HTML string"""
    comp_id = component.get("id", "")

    if comp_type == "text":
        markdown = component.get("markdown", "")
        html_content = convert_markdown_to_html(markdown)
        return f"<div id='{comp_id}' class='prose'>{html_content}</div>"

    elif comp_type == "table":
        data = component.get("data", [])
        if not data:
            return "<p class='text-gray-500'>No data available</p>"

        html = [f"<div id='{comp_id}' class='overflow-x-auto'>"]
        html.append("<table class='min-w-full bg-white border border-gray-300'>")

        # Create header row
        if data:
            html.append("<tr class='bg-gray-100'>")
            for key in data[0].keys():
                html.append(
                    f"<th class='px-4 py-2 text-left text-sm font-medium text-gray-600 uppercase tracking-wider'>{key}</th>"
                )
            html.append("</tr>")

        # Create data rows
        for item in data:
            html.append("<tr class='border-t border-gray-300'>")
            for value in item.values():
                html.append(f"<td class='px-4 py-2 text-sm text-gray-800'>{value}</td>")
            html.append("</tr>")

        html.append("</table>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "plot":
        plot_data = component.get("data", {})
        return f"<div id='{comp_id}' class='w-full h-96' data-plotly='{json.dumps(plot_data)}'></div>"

    elif comp_type == "slider":
        min_val = component.get("min", 0)
        max_val = component.get("max", 100)
        step = component.get("step", 1)
        value = component.get("value", min_val)
        label_text = component.get("label", "")

        html = ["<div class='mb-4'>"]
        html.append(
            f"<label for='{comp_id}' class='block text-sm font-medium text-gray-700 mb-1'>{label_text}</label>"
        )
        html.append("<div class='flex items-center'>")
        html.append(
            f"<input type='range' id='{comp_id}' min='{min_val}' max='{max_val}' step='{step}' value='{value}' "
            + "class='w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer' "
            + f"oninput=\"document.getElementById('{comp_id}-value').textContent = this.value\" "
            + f"onchange=\"sendComponentUpdate('{comp_id}', parseFloat(this.value))\">"
        )
        html.append(
            f"<span id='{comp_id}-value' class='ml-2 text-sm text-gray-600'>{value}</span>"
        )
        html.append("</div>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "selectbox":
        options = component.get("options", [])
        value = component.get("value", "")
        label_text = component.get("label", "")

        html = ["<div class='mb-4'>"]
        html.append(
            f"<label for='{comp_id}' class='block text-sm font-medium text-gray-700 mb-1'>{label_text}</label>"
        )
        html.append("<div class='relative'>")
        html.append(
            f"<select id='{comp_id}' class='block w-full px-3 py-2 text-base border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500' "
            + f"onchange=\"sendComponentUpdate('{comp_id}', this.value)\">"
        )

        for option in options:
            selected = "selected" if option == value else ""
            html.append(f"<option value='{option}' {selected}>{option}</option>")

        html.append("</select>")
        html.append("</div>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "checkbox":
        value = component.get("value", False)
        label_text = component.get("label", "")

        checked = "checked" if value else ""
        html = ["<div class='mb-4'>"]
        html.append("<div class='flex items-center'>")
        html.append(
            f"<input id='{comp_id}' type='checkbox' {checked} class='h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded' "
            + f"onchange=\"sendComponentUpdate('{comp_id}', this.checked)\">"
        )
        html.append(
            f"<label for='{comp_id}' class='ml-2 block text-sm text-gray-900'>{label_text}</label>"
        )
        html.append("</div>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "progress":
        value = component.get("value", 0)
        label = component.get("label", 0)

        html = ["<div class='mb-4'>"]
        html.append("<div class='w-full bg-gray-200 rounded-full h-2.5'>")
        html.append(
            f"<div class='h-full bg-indigo-600 rounded-full' style='width: {int(value * 100)}%'></div>"
        )
        html.append("</div>")
        html.append(f"<p class='text-sm text-gray-600 mt-1'>{int(label * 100)}%</p>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "alert":
        message = component.get("message", "")
        level = component.get("level", 1)

        # Determine alert color based on level
        colors = {
            1: "blue",  # info
            2: "yellow",  # warning
            3: "red",  # error
        }
        color = colors.get(level, "blue")

        html = [
            f"<div id='{comp_id}' role='alert' class='bg-{color}-100 border-l-4 border-{color}-500 text-{color}-700 p-4 mb-4'>"
        ]
        html.append(f"<p class='text-sm'>{message}</p>")
        html.append("</div>")
        return "".join(html)

    elif comp_type == "dag":
        # For DAG, we'll just show a placeholder since it requires more complex rendering
        html = [
            f"<div id='{comp_id}' class='border border-gray-300 rounded p-4 bg-gray-50'>"
        ]
        html.append(
            "<p class='text-center text-gray-500 my-4'>Workflow DAG visualization (interactive version not available in HTML-only mode)</p>"
        )
        html.append("</div>")
        return "".join(html)

    # Default case for unsupported component types
    return f"<p class='text-red-500'>Unsupported component type: {comp_type}</p>"


def convert_markdown_to_html(markdown: str) -> str:
    """
    Simple markdown to HTML converter
    """
    # Convert headers
    html = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", markdown, flags=re.MULTILINE)
    html = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)

    # Convert bold and italic
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

    # Convert links
    html = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', html)

    # Convert code blocks
    html = re.sub(r"```(.*?)```", r"<pre><code>\1</code></pre>", html, flags=re.DOTALL)
    html = re.sub(r"`(.*?)`", r"<code>\1</code>", html)

    # Convert paragraphs (simple approach)
    paragraphs = html.split("\n\n")
    for i, p in enumerate(paragraphs):
        if not p.startswith("<h") and not p.startswith("<pre"):
            paragraphs[i] = f"<p>{p}</p>"

    html = "\n".join(paragraphs)

    # Replace remaining newlines with <br>
    html = html.replace("\n", "<br>")

    return html


@app.get("/")
def home():
    """Render the home page with components display area using direct WebSocket"""
    content = Div(
        htmx_js,
        tailwind_css,
        plotly_js,
        websocket_script,
        debug_script,
        Div(
            H1(
                "Preswald Components Viewer",
                class_="text-2xl font-bold text-center my-4",
            ),
            Div(
                Button(
                    "Debug Connection",
                    onclick="debugConnection()",
                    class_="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2",
                ),
                Button(
                    "Refresh",
                    onclick="refreshComponents()",
                    class_="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded",
                ),
                class_="text-center mb-4",
            ),
            # This div will be updated by the WebSocket
            Div(
                P(
                    "Connecting to Preswald...",
                    class_="text-center text-gray-500 my-10",
                ),
                id="components-display",
                class_="min-h-screen",
            ),
            class_="container mx-auto",
        ),
    )
    return Titled("Preswald Components Viewer", content)
