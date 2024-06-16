# Plotly/Dash and OpenAI API Live Text Streaming Application Examples

There are two different solutions for live text streaming with using Dash and OpenAI API in this repository.

### 1. dash_text_streaming_with_set_props.py

In this example, I used set_props which is a advaced callback subject in Dash. This solution is not cool, because it has high latency. So, texts are loading chunk by chunk as you can see below:

![1](https://github.com/ryilkici/plotly-dash-openai-text-streaming/assets/24529498/c851026e-3b4c-4d55-a0ac-e67dc2d4c102)

### 2. dash_text_streaming_with_socketio.py

In this example, I used flask_socketio and dash_socketio. This is cool solution because websocket is better solution for live streaming. Texts are loading word by word as you can see below:

![2](https://github.com/ryilkici/plotly-dash-openai-text-streaming/assets/24529498/3925fec3-392c-4716-9df2-534329922cf0)
