from flask import Flask,make_response,request

app = Flask(__name__)


@app.route('/',methods=['GET'])
def get():
    a = request.args.get('dzd')
    rst = make_response(r'天王盖地虎')
    rst.headers['Access-Control-Allow-Origin']='*'
    rst.headers['Access-Control-Allow-Methods']='GET'
    rst.status='666333'
    return rst


app.run(host='127.0.0.1', port=233, debug=True)
