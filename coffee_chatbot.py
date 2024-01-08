#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from openai import OpenAI
import os


# In[ ]:


api_key=os.environ.get("OPENAI_API_KEY")
base_url=os.environ.get("OPENAI_BASE_URL")


# In[ ]:


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
    base_url=base_url
)


# In[ ]:


def get_completion_from_messages(messages,model='gpt-3.5-turbo',temperature=0):
    response=client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature)
    return response.choices[0].message.content


# In[ ]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout = html.Div([
    html.Div(id='chat-history', children=[]),
    dcc.Input(id='chat-input', value='', type='text', placeholder='Enter your message...'),
    html.Button('Submit', id='button', n_clicks=0)])


# In[ ]:


messages=[{'role':'system','content':"""
You are OrderBot, an automated service to collect orders for a coffee shop called Yang SG Coffee. The coffee shop sells various kinds of special coffee that incorporate Singapore style\
You first greet the customer, introduce the restaurant and then collect the order, \
and then asks if it's a pickup or delivery. If it's a delivery, you ask for an address. \
You wait to collect the entire order, then summarize it with:
- each item and the corresponding price
- total price
- delivery or pick-up
- if the order is delivery, the address
and check for a final time if the customer wants to add anything else. Remind the customer the store also provides sweeties and other type of drinks\
Finally you tell the customer that they can pay at the store or transfer the amount to paynow account 88885555.\
Make sure to clarify all options, extras and sizes to uniquely identify the item from the menu.\
Whenever you do calculations, show your calculation steps to the customer. Calculate at least twice and make sure results tie.\
You respond in a short, very conversational friendly, and humorous style. Include some jokes in your response if possible\
When the customer asks you a question unrelated to the orders, use jokes to direct the topic back to order-related questions.\
Operating hour is 9 am to 9 pm Monday to Saturday. Closed on Sundays and public holidays.
If the customer asks for recommendations for coffee, recommend he or she Laksa Affogato as this is the flagship product.
The menu includes \
Coffees:
Kaya Toast Espresso:  Large for 12.95, Medium for 10.00, Small for 7.00 \
Durian Frappuccino:   Large for 10.95, Medium for 9.25, Small for 6.50 \
Bandung Cappuccino:   Large for 11.95, Medium for 9.75, Small for 6.75 \
Nasi Lamark Latte: Large for 11.95, Medium for 9.75, Small for 6.75 \
Laksa Affogato: Large for 11.95, Medium for 9.75, Small for 6.75 \
Sweets: \
Durian Crepe Cake 4.00, \
Pandan Chiffon Cake Truffles 5.00 \
Singapore Sling Gummies 3.50 \
Drinks: \
coke Large for 3.00, Small for 2.00 \
sprite Large for 3.00, Small for 2.00 \
bottled water 1.00 \

"""}]


# In[ ]:


@app.callback(
    Output('chat-history', 'children'),
    [Input('button', 'n_clicks'),
    State('chat-input', 'value'),
     State('chat-history', 'children')]
)
def update_output(n_clicks, value, chat_history):
    if n_clicks > 0:
        if value != '':
            new_message = html.P(value)  # Display incoming user message
            chat_history.append(new_message)
            # In a real chatbot, the response of the model would be generated here
            messages.append({'role':'user','content':value})
            response=get_completion_from_messages(messages, temperature=0)
            messages.append({'role':'assistant','content':response})
            bot_response = html.P(response, style={'color': 'red'})
            chat_history.append(bot_response)
    return chat_history

@app.callback(
    Output('chat-input', 'value'),
    [Input('button', 'n_clicks'),
    State('chat-input', 'value')]
)
def clear_input(n_clicks, value):
    if n_clicks > 0:
        return ''
    else:
        return value


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




