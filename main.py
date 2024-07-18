from flask import * 

app=Flask(__name__,template_folder="templates")

from public import public


app.register_blueprint(public)
app.run(debug=True,port=5002)
