# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

app = dash.Dash(
    __name__,
    external_scripts=
        [
            {
                'src':'https://cdn.jsdelivr.net/npm/@iframe-resizer/child',
                'type':'text/javascript',
                'async': True
            }
        ],
    use_pages=True,
    suppress_callback_exceptions=True, # Optimizing initial loading times
)
server = app.server

colors = {"background": "#FFFFFF", "text": "#101010", "warning-text": "#FF4136"}

app.layout = dash.html.Div(
        [dash.dcc.Loading(dash.page_container, fullscreen=True, type="circle")], 
        style={"backgroundColor": colors["background"], "padding": "0.5rem", "fontFamily": "Verdana, Geneva, sans-serif"},
)

# Add CSP headers, should probably use .env file for this instead
@app.server.after_request
def modify_headers(response):
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://*.infectieradar.be https://infectieradarbe.staging.influenzanet.info"
    return response

if __name__ == "__main__":
    # local dev
    app.run(debug=True)
    # production
    # app.run_server(host='0.0.0.0', port=9000, debug=False, use_reloader=False)
