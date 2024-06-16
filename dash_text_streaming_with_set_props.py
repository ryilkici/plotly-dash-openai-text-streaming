from openai import OpenAI
import dash
from dash import dcc, html, Input, Output, State, DiskcacheManager, set_props
import dash_bootstrap_components as dbc
from uuid import uuid4
import diskcache
import time

launch_uid = uuid4()
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache, cache_by=[lambda: launch_uid], expire=60)

client = OpenAI(
    api_key = 'YOUR_API_KEY'
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,
                background_callback_manager=background_callback_manager)
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input-prompt', type='text', placeholder='Ask something...',
                      style={'marginBottom': '10px'}),
            dbc.Button('Send', id='submit-button', n_clicks=0, color='primary')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='output-response')
        ], width=12)
    ])
], className="mt-5")


@app.callback(
    Input('submit-button', 'n_clicks'),
    State('input-prompt', 'value'),
    background=True,
    interval=10,
    prevent_initial_call=True
)
def update_output(n_clicks, prompt):
    if n_clicks > 0:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        result = ""
        for chunk in response:
            if len(chunk.choices) > 0:
                text = chunk.choices[0].delta.content
                if text:
                    result += text

                    set_props('output-response', {'children': [dcc.Markdown(result)]})

        time.sleep(1)

        set_props('output-response', {'children': [dcc.Markdown(result)]})


if __name__ == '__main__':
    app.run_server(debug=False)
