# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os

import dash

from dotenv import load_dotenv
load_dotenv()

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

app.layout = dash.html.Div(
        dash.page_container, 
        style={"backgroundColor": "#FFFFFF", "padding": "0.5rem", "fontFamily": "Verdana, Geneva, sans-serif"},
)

# Add CSP headers to allow for iframe embedding
@app.server.after_request
def modify_headers(response):
    response.headers['Content-Security-Policy'] = f"frame-ancestors {os.getenv('CSP_FRAME_SRC')}"
    return response

if __name__ == "__main__":
    # local dev
    app.run(debug=True)
    # production
    # app.run_server(host='0.0.0.0', port=9000, debug=False, use_reloader=False)
