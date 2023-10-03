#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import base64
import muggle_ocr
from PIL import Image
from io import BytesIO
from flask import Flask, request

sdk_Captcha = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
sdk_OCR = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)

app = Flask(__name__)

@app.route("/muggle_ocr/<mode>",methods=["POST"])
def index1(mode="captcha"):
    if request.get_data():
        text = ''
        try:
            if mode == "captcha":
                image_data = base64.b64decode(request.get_data().decode())
                image = Image.open(BytesIO(image_data))

                # 创建一个白色底图像
                background = Image.new('RGB', image.size, (255, 255, 255))

                # 将图像粘贴到白色底图像上，忽略透明度
                background.paste(image, (0, 0), mask=image.convert('RGBA'))

                # 将图像转换为字节流
                output_buffer = BytesIO()
                background.save(output_buffer, format='PNG')
                image_data = output_buffer.getvalue()

                text = sdk_Captcha.predict(image_bytes=image_data)
            if mode == "ocr":
                text = sdk_OCR.predict(image_bytes=base64.b64decode(request.get_data().decode()))
        except Exception as e:
            print('[-] error:{}'.format(e))
        return text

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
