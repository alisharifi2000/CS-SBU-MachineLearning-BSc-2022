import re
from flask import Flask, request
from utils.common import response_message, read_json_time_series,config_final_result,gregorian_to_jalali,read_and_anomoly_detection,read_and_balance
from utils.interpolation_methods import interpolation
from utils.outlier_detection import anomoly_detection
from flask_restx import Resource, Api,fields
import json
app  = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
api = Api(app)
###########################################################################
###.......................service1,2 models.............................###
###########################################################################
time_series = api.model('time',{
    "0": fields.String("1397-01",description = "monthly jalali"),
    "1": fields.String("2021-01",description = "monthly gregorian"),
    "2": fields.String("2021-01-01 00:00:00",description = "daily hourly minutely gregorian"),
    "3": fields.String("1397-01-01 00:00:00",description = "daily hourly minutely jalali")
})
time_series2 = api.model('time_series2', {
    "0": fields.String("2021-01",description = "monthly"),
    "1": fields.String("2021-01-01 00:00:00",description = "daily hourly minutely")
})
vol_model = api.model('vol',{
    "0": fields.Integer(100),
    "1": fields.Integer(200),
    "2": fields.Integer(70),
    "3": fields.Integer(20),
})
type_model = api.schema_model("type",{
    'enum': ["gregorian", 'jalali'],
    'type': 'string'
})
time_model = api.schema_model("time_enum",{
    'enum': ["monthly", 'daily','hourly','minutely'],
    'type': 'string'
})
interpolation_model = api.schema_model("interpolation",{
    'enum': ["linear", 'spline','polynomial'],
    'type': 'string'
})
data1_model = api.model("data1",{
    "time": fields.Nested(time_series),
    "vol": fields.Nested(vol_model)
})
config1 = api.model('config',{
    "type": fields.Nested(type_model),
    "time": fields.Nested(time_model),
    "interpolation":fields.Nested(interpolation_model),
    "order": fields.Integer(1, description = "must set order ((number of data) - 1) or less otherwise error occurs only necessary for spline and polynomial")
})
config2 = api.model("config2", {
    "time": fields.Nested(time_model),
    "interpolation":fields.Nested(interpolation_model),
    "order": fields.Integer(1, description = "must set order ((number of data) - 1) or less otherwise error occurs only necessary for spline and polynomial")

})
data2_model = api.model('data2', {
    'time': fields.Nested(time_series2),
    'vol': fields.Nested(vol_model)
})
service1_model = api.model('Model',{
    "data": fields.Nested(data1_model),
    "config": fields.Nested(config1)
})
service2_model = api.model('service2Model', {
    "data": fields.Nested(data2_model),
    "config": fields.Nested(config2)
})
###########################################################################
###........................service3 models..............................###
###########################################################################
time3_model =api.model("time3_model", {
    "0": fields.String("2022-01-01 00:00:00",description = "time must be in this format")
})
id_model= api.model("id_model",{
    "0": fields.Integer(0, description = "id must be in this format")
})
feature_model = api.model("feature_model",{
    "0": fields.Integer(50, description = "can contain float too")
})
data3_model = api.model("data3_model",{
    "time": fields.Nested(time3_model, description = "required for timeseries"),
    "vol": fields.Nested(vol_model, description = "required for timeseries"),
    "id": fields.Nested(id_model, description = "required for not timeseries"),
    "feature": fields.Nested(feature_model, description = "must have at least one feature name of feature is changeable")
})
config3_model = api.model("config3_model", {
    "time_series": fields.Boolean(True),
    "method": fields.String(enum = ["seasonal","threshold", "persist", "zscore", "IQR"], description = "seasonal, threshold and persist are anomoly detections for time series and zscore and IQR are outlier detection for other data"),
    "feature": fields.String("feature",description = "required for not time series - name of feature you want to detect anomoly for"),
    "freq": fields.Integer(5, description = "required for seasonal method ; is the frequency of season which means at which frequency data repeats pattern (checks per data not per day)"),
    "high": fields.Integer(500,description = "required for threshold; simply if vol is above high it considers it as anomoly"),
    "low": fields.Integer(50, description = "required for threshold; simply if vol is below low it considers it as anomoly"),
})
service3_model = api.model('service3Model',{
    "data": fields.Nested(data3_model),
    "config": fields.Nested(config3_model)
})
###########################################################################
###........................service4 models..............................###
###########################################################################
class_model = api.model("class_model", {
    "0": fields.Integer(1),
    "1": fields.Integer(0),
    "2": fields.Integer(1),
})
data4_model = api.model("data4_model", {
    "id": fields.Nested(id_model),
    "feature1": fields.Nested(vol_model),
    "feature2": fields.Nested(vol_model),
    "class": fields.Nested(class_model)
})
config4_model= api.model("config4_model" ,{
    "method": fields.String("SMOTE", enum = ["RandomOverSample","SMOTE","ADASYN" ,"RandomUnderSample", "ClusterCentroids","NearMiss"]),
    "class_name": fields.String("class", description = "name of the class column")
})
service4_model = api.model('service4Model',{
    "data": fields.Nested(data4_model, description= "no limit on number of features"),
    "config": fields.Nested(config4_model)
})
def JsonResponse(data):
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/service1', methods=['POST'])
class Interpolation(Resource):
    @api.doc(id = "get something", body = service1_model, description = "gets time series returns interpolated timeseries make sure to check model first\n you should pass one of 4 types that are shown in data time\n ****SEE INPUT EXAMPLES IN INPUT_OUTPUT FOLDER IN PROJECT***")
    def post(self):
        req = request.get_json()
        config = req['config']
        try:
            data = read_json_time_series(req['data'],config)
            result = interpolation(data, config)
            result = result.to_json(orient='index', date_format='iso', date_unit = 's')
            response = app.response_class(
                response=json.dumps(config_final_result(result,config)),
                status=200,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            return str(e)
@api.route('/service2', methods=  ['POST'])
class InterplationToJalali(Resource):
    @api.doc(body = service2_model, description = "gets gregorian time series and returns jalali time series make sure to check models first\n you should pass one of 2 types that are shown in data time\n ****SEE INPUT EXAMPLES IN INPUT_OUTPUT FOLDER IN PROJECT***")
    def post(self):
        try:
            req = request.get_json()
            config = req["config"]
            data = read_json_time_series(req['data'],config)
            result = interpolation(data, config)
            result = result.to_json(orient='index', date_format='iso', date_unit = 's')
            return JsonResponse(gregorian_to_jalali(result,config))
        except Exception as e:
            return str(e)
@api.route('/service3', methods=  ['POST'])
class OutlierDetection(Resource):
    @api.doc(body =service3_model, description = "Method for outlier detection in time series and other data\nTime series: intrepolates timeseries per day first and then detects anomolies \n       1-seasonal: This detector uses a seasonal decomposition transformer to remove seasonal pattern (as well as trend optional), and identifies a time point as anomalous when the residual of seasonal decomposition is anomalously large \n     \t   2-threshold: This detector compares time series values with user-given thresholds, and identifies time points as anomalous when values are beyond the thresholds\n     3-persist: This detector compares time series values with the values of their preceding time windows, and identifies a time point as anomalous if the change of value from its preceding average or median is anomalously large \n Other data: detects outliers in data \n 1-zscore: calculates zscore((data_point -mean) / std. deviation) for each record if zscore is above 3 detects it as anomoly consider that if number of data is too low zscore might not even reach 3 \n 2-IQR: Inter Quartile Range detects outlier if not in range ((Q1-1.5*IQR)-(Q3 +1.5*IQR))\n ****SEE INPUT EXAMPLES IN INPUT_OUTPUT FOLDER IN PROJECT***")
    def post(self):
        try:
            req = request.get_json()
            data = read_and_anomoly_detection(req["data"],req["config"])
            if req["config"]["time_series"]:
                data = data.to_json(orient='index', date_format='iso', date_unit = 's')
            else:
                data = data.to_json(orient='index')
            return JsonResponse(json.loads(data))
        except Exception as e:
            return str(e)
@api.route('/service4',methods = ["POST"])
class Imbalanced(Resource):
    @api.doc(body = service4_model, description = "Method for balancing imbalanced data\nOver Sampling methods:\n 1-RandomOverSample: generates new samples by randomly sampling with replacement the current available samples\n 2-SMOTE: Synthetic Minority Oversampling Technique using interpolation between nearest neighbors ***note that at least 6 samples must be in minority class***\n 3-ADASYN: Adaptive Synthetic similar to SMOTE but it generates different number of samples depending on an estimate of the local distribution of the class to be oversampled ***note that at least one of neighbors of minority class must be from majority class and  at least 6 samples must be in minority class*** \n Under sampling methods:\n1-RandomUnderSample:Under-sample the majority class(es) by randomly picking samples without replacement\n2-ClusterCentroids: Method that under samples the majority class by replacing a cluster of majority samples by the cluster centroid of a KMeans algorithm. This algorithm keeps N majority samples by fitting the KMeans algorithm with N cluster to the majority class and using the coordinates of the N cluster centroids as the new majority samples \n3-NearMiss: selects the majority samples for which the average distance to the N closest samples of the minority class is the smallest.****SEE INPUT EXAMPLES IN INPUT_OUTPUT FOLDER IN PROJECT***")
    def post(self):
        req = request.get_json()
        config = req["config"]
        data = req["data"]
        try:
            return JsonResponse(read_and_balance(data,config))
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug = False)
