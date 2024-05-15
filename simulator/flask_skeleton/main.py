import os
from flask import Flask, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)


app.secret_key = "test_secret" #os.environ.get('FLASK_SECRET')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_DOMAIN'] = '.localhost'

app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)

import routes


#if __name__ == "__main__":
#    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
  #    app = create_app()
  print(" Starting app...")
  app.run(host="0.0.0.0", port=5000)
