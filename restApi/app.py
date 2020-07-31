try:
    from flask import Flask
    from flask_restful import Resource, Api

    from flask_limiter.util import get_remote_address
    from flask_limiter import Limiter

    from flasgger import Swagger
    from flasgger.utils import swag_from
    from flask_restful_swagger import swagger

except Exception as e:
    print('There is some missing modules {}'.format(e))

app = Flask(__name__)
api = Api(app)

limiter = Limiter(app, key_func=get_remote_address)
limiter.init_app(app)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/docs')

data = []

class HelloWorld(Resource):

    decorators=[limiter.limit("100/days")]
    @swagger.model
    @swagger.operation(notes='some really good notes')

    def __init__(self):
        pass

    def get(self, name):
        if len(data) < 0 :
            return {
                'Response': 200,
                'Data': 'Null'
            }
        return {
            'Response': 200,
            'Data': data
        }

    def post(self, name):
        temp= {'Name': name}
        data.append(temp)
        return {
            'Response': 201,
            'Data': 'Added data with name {}'.format(name)
        }

    def delete(self, name):
        for ind,x in enumerate(data):
            if x['Name'] == name:
                temp = data.pop(ind)
                return {
                    'Response': 202,
                    'Note':'Deleted'
                }

api.add_resource(HelloWorld, '/name/<string:name>')
if __name__ == "__main__":
    app.run(debug=True)