import os
import flask
import pandas as pd

from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


dice_data = pd.read_csv('static/dice_scores.csv')

def get_dice_list(dice_scores,imageID):
     image_dice = dice_scores.loc[imageID].tolist()[1:]
     image_dice_precision = ['%.2f' % elem for elem in image_dice]
     return image_dice_precision

input_images = {"img":"static/brain_images/test_x_0.jpg",
                "partial":"static/pred_images_200/test_x_0.jpg",
                "full": "static/pred_images_1000/test_x_0.jpg",
                "ground": "static/label_images/test_y_0.jpg",
                "filter":"static/filter_plots/00_layer_filters_plot.png",
                "feature":"static/feature_maps_plots/00_image_00_layer_avg_feature_map_mse.png",
                "partial_dice": get_dice_list(dice_data,0)[0],
                "full_dice": get_dice_list(dice_data,0)[1]
                }



@app.route('/get_input_image',methods=['POST','GET'])
def get_input_image():
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        layer = str(data.get('layer'))
        zlayer = layer.zfill(2)
        image = str(data.get('image'))
        zimage = image.zfill(2)
        print("L:" +layer+"\nI:"+image)
        dices = get_dice_list(dice_data,int(image))
        global input_images
        input_images = {"img":"static/brain_images/test_x_"+image+".jpg"}
        input_images.update({"partial":"static/pred_images_200/test_x_"+image+".jpg"})
        input_images.update({"full":"static/pred_images_1000/test_x_"+image+".jpg"})
        input_images.update({"ground":"static/label_images/test_y_"+image+".jpg"})
        input_images.update({"filter":"static/filter_plots/"+zlayer+"_layer_filters_plot.png"})
        input_images.update({"feature":"static/feature_maps_plots/"+zimage+"_image_"+zlayer+"_layer_avg_feature_map_mse.png"})
        input_images.update({"partial_dice": dices[0]})
        input_images.update({"full_dice": dices[1]})
        print(input_images)
        return flask.jsonify(input_images)
    else:
        return flask.jsonify(input_images)


if __name__=='__main__':
    app.run()
