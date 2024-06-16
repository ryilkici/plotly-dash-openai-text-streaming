import time
import uuid
from dash_socketio import DashSocketIO
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, clientside_callback, html, no_update
from flask_socketio import SocketIO, emit
from openai import OpenAI

client = OpenAI(
    api_key = 'YOUR_API_KEY'
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server.secret_key = "Test!"

socketio = SocketIO(app.server)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-prompt', type='text', placeholder='Ask something...', style={'marginBottom': '10px'}),
            dbc.Button('Send', id='submit-button', n_clicks=0, disabled=True, color='primary')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='output-response'),
            html.Div(id="notification_wrapper"),
            DashSocketIO(id='socketio', eventNames=["notification", "stream"]),
        ], width=12)
    ])
], className="mt-5")


@socketio.on("connect")
def on_connect():
    print("Client connected")

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")


@callback(
    Output("output-response", "children"),
    Output("notification_wrapper", "children", allow_duplicate=True),
    Input("submit-button", "n_clicks"),
    State("input-prompt", "value"),
    State("socketio", "socketId"),
    running=[[Output("output-response", "children"), "", None]],
    prevent_initial_call=True,
)
def display_status(n_clicks, prompt, socket_id):
    if not n_clicks or not socket_id:
        return no_update, []
    
    response = client.chat.completions.create(
        model='MODEL_NAME',
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    result = ""
    for chunk in response:
        if len(chunk.choices) > 0:
            text = chunk.choices[0].delta.content
            if text:
                result += text
                
                emit("stream", text, namespace="/", to=socket_id)
                time.sleep(0.05)

    return result, []

clientside_callback(
    """connected => !connected""",
    Output("submit-button", "disabled"),
    Input("socketio", "connected"),
)

clientside_callback(
    """(notification) => {
        if (!notification) return dash_clientside.no_update
        return notification
    }""",
    Output("notification_wrapper", "children", allow_duplicate=True),
    Input("socketio", "data-notification"),
    prevent_initial_call=True,
)

clientside_callback(
    """(word, text) => text + word""",
    Output("output-response", "children", allow_duplicate=True),
    Input("socketio", "data-stream"),
    State("output-response", "children"),
    prevent_initial_call=True,
)


if __name__ == '__main__':
    app.run_server(debug=False)
