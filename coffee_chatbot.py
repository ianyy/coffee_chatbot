#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from openai import OpenAI
import os


# In[2]:


api_key=os.environ.get("OPENAI_API_KEY")
base_url=os.environ.get("OPENAI_BASE_URL")


# In[3]:


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
    base_url=base_url
)


# In[4]:


def get_completion_from_messages(messages,model='gpt-3.5-turbo',temperature=0):
    response=client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature)
    return response.choices[0].message.content


# In[5]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout = html.Div([
    dcc.Input(id='chat-input', value='', type='text', placeholder='Enter your message...'),
    html.Button('Submit', id='button', n_clicks=0),
    html.Div(id='chat-output'),
    html.Div(id='chat-history', children=[])
])


# In[6]:


messages=[{'role':'system','content':"""
You are OrderBot, an automated service to collect orders for a coffee shop called yang sg coffee. The coffee shop sells varies kinds of special coffee that incorporate Singapore style\
You first greet the customer, introduce the restaurant and then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. Remind the customer the store also provides sweeties and other type of drinks\
If it's a delivery, you ask for an address. \
Finally you tell the customer that they can pay at store or transfer the amount to paynow account 88885555.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly, and humorous style. Include some jokes in your response if possible\
When the customer asks you a question unrelated to the orders, use jokes to direct the topic back to order related questions.\
Operating hour is 9am to 9pm Monday to Saturday. Closed on Sunday and public holidays.
If the customers asks for recommendations of coffee, recommend he or she Laksa Affogato as this is the flagship product.
The menu includes \
Coffees:
Kaya Toast Espresso  12.95, 10.00, 7.00 \
Durian Frappuccino   10.95, 9.25, 6.50 \
Bandung Cappuccino   11.95, 9.75, 6.75 \
Nasi Lamark Latte 11.95, 9.75, 6.75 \
Laksa Affogato 11.95, 9.75, 6.75 \
Sweets: \
Durian Crepe Cake 4.00, \
Pandan Chiffon Cake Truffles 5.00 \
Singapore Sling Gummies 3.50 \
Drinks: \
coke 3.00, 2.00 \
sprite 3.00, 2.00 \
bottled water 1.00 \


"""}]


# In[7]:


@app.callback(
    Output('chat-history', 'children'),
    [Input('button', 'n_clicks')],
    [State('chat-input', 'value'),
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
    [Input('button', 'n_clicks')],
    [State('chat-input', 'value')]
)
def clear_input(n_clicks, value):
    if n_clicks > 0:
        return ''
    else:
        return value


# In[8]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




