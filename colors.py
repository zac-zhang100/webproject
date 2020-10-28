from flask import Flask, jsonify
from flasgger import Swagger
from app import app
swagger = Swagger(app)

@app.route('/player/add/')
def add():
    """Example endpoint returning a list of colors by palette
    方法名称:增加选手
    方法描述：调用此api增加一名选手
    ---
    tags：
      -接口名称：选手管理API
    parameters:
      - name: body
        in: body
        required：true
        schema:
          id: player
          required:
            - nickname
            - name
            - phone
          properties:
            nickname:
              type: string
              description: 昵称
              default: "XXX"
            name:
              type: string
              description: 姓名
              default: "XXX"
            nickname:
              type: string
              description: 电话
              default: "XXX"
    responses:
      200:
        description: 状态描述：成功返回json格式
        schema:
          id: Success
          properties:
            code:
              type: string
              description: 状态码
              default: 200
            msg:
              type: string
              description：信息
              default: "ok"
            error_code:
              type: string
              description：错误码
              default: o

    player = {
      "name" : "zac",
      "number" : "123456",
      "nickname" : "zac"
      }

    return jsonify(player)

app.run(debug=True)