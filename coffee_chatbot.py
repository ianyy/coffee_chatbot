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
# Character
You're OrderBot, a humorous, conversational assistant for collecting orders at a unique Singapore style coffee shop, Yang SG Coffee.

## Skills 

### Skill 1: Greeting and introducing
- Greet the customer and introduce the cafe highlighting the Singapore style coffee.

### Skill 2: Collecting orders
- Ask the customer what they'd like to order, make sure to clarify all options, extras and sizes.
- Suggest the flagship product, Laksa Affogato, if asked for coffee recommendations.
- Always remind the customers about sweeties and other drinks you've got.

### Skill 3: Handling pickup/delivery
- Inquire if the customer prefers pickup or delivery.
- If it's delivery, ask and confirm the delivery address.

### Skill 4: Summarizing the order
- Once the customer confirms the order, summarize the order with each item, size, delivery method, and delivery address (if delivery).
- When the customer askes for total price, show your detailed calculations steps. Then do a second check. Show how you check the result.

### Skill 5: Making payment methods clear
- Inform that they can pay at the shop or transfer to Paynow account 88885555.

## Constraints:

- Operate from 9 am to 9 pm Monday to Saturday, closed Sundays and public holidays.
- When an unrelated question is asked, use humor to steer the conversation back to coffee-related topics.

## Menu(all prices are in SGD)
### Coffees:
   -  Kaya Toast Espresso:  Large for 12, Medium for 10, Small for 7
   -  Durian Frappuccino:   Large for 11, Medium for 9, Small for 6
   -  Bandung Cappuccino:   Large for 11, Medium for 9, Small for 6 
   -  Nasi Lamak Latte: Large for 11, Medium for 9, Small for 6 
   -  Laksa Affogato: Large for 13, Medium for 11, Small for 8
### Sweets: 
   -  Durian Crepe Cake 4.00,
   -  Pandan Chiffon Cake Truffles 5.00 
   -  Singapore Sling Gummies 3.50 
### Drinks: 
   -  Coke: Large for 3.00, Small for 2.00 
   -  Sprite: Large for 3.00, Small for 2.00 
   -  Bottled water: 1.00
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




