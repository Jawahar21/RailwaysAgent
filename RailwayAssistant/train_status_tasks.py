from flask import request, jsonify
from railAPI_activities import RailwayDB


class TrainStatusActivities :


    def trainStatusMainActivity(self,webhook_req):
        trains = []
        parameters = webhook_req.get('queryResult').get('parameters')
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        if ( parameters.get('train_number') ):
            train_detail = RailwayDB().getTrainNameNumber(parameters.get('train_number'))
            trains.append(train_detail)
            if ( type(train_detail) is dict ):
                return jsonify({
                    "fulfillmentText" : "Do you mean?",
                    "outputContexts" : outputContexts,
                    "payload" : {
                        "actual_data" : True,
                        "trains" : trains
                    }
                })
            else :
                return jsonify({
                    "fulfillmentText" : trains,
                })
        if ( parameters.get('train_name') ):
            train_name = parameters.get('train_name')
            return jsonify({
                "fulfillmentText": "Wait for a moment!",
                "outputContexts" : outputContexts,
                "payload" : {
                    "actual_data" : False,
                    "train_name" : train_name,
                    "activity" : "TrainStatus_Delayed_Picker_Response"
                }
            })

        return jsonify({
            "fulfillmentText" : "Testing"
        })

    def trainStatusPickerDelayedResponse(self,data):
        trains = RailwayDB().getTrainAutoSuggest(data.get('train_name'))
        print(trains)
        if ( type(trains) is list ):
            return jsonify({
                "queryResult" : {
                    "action" : "train_status_delayed_response",
                    "fulfillmentText": "Do you mean?",
                    "webhookPayload" : {
                        "actual_data" : True,
                        "trains" : trains,
                    }
                }
            })
        else :
            return jsonify({
                "queryResult" : {
                    "action" : "train_status_delayed_response",
                    "fulfillmentText": trains
                }
            })

    def TrainStartDateActivity(self,webhook_req):
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        return jsonify({
            "fulfillmentText": "When did this train start?",
            "outputContexts" : outputContexts,
            "payload" : {
                "date" : ["Today","Yesterday","2 days Ago","3 days ago"]
            }
        })

    def trainStatusResponse(self,webhook_req):
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        date = webhook_req.get('queryResult').get('parameters').get('date')
        print(date)
        parsed_date = date[8:10] + "-"+date[5:7]+"-"+date[0:4]
        return jsonify({
            "fulfillmentText": "Wait for a moment!",
            "outputContexts" : outputContexts,
            "payload" : {
                "actual_data" : False,
                "date" : parsed_date,
                "activity" : "TrainStatus_Delayed_Final_Response"
            }
        })

    def trainStatusDelayedResponse(self,webhook_req):
        train_number = ''
        response = ''
        print("Herr")
        date = webhook_req.get('date')
        outputContexts = webhook_req.get('outputContexts')
        print(date)
        for context in outputContexts :
            if ( 'train_number_input-followup' in context.get('name') ):
                train_number = int(context.get('parameters').get('train_number'))
                break
        data = RailwayDB().getLiveTrainStatus(train_number, date)
        print(data)
        if data['response_code'] == 200 :
            position = data['position']
            print(position)
            if 'Source' in data['position'] :
                station_data = data.get('route')[0]
                station_name = station_data.get('station').get('name')
                words = position.split(" ")
                for word in words:
                    response = response + word + " "
                    if word == 'Source':
                        response = response + "i.e.., " + station_name + " "
                # response = position.replace( 'Source',station_name )
                print (response)
            elif 'Destination' in data['position'] :
                station_data = data.get('route')[ len(data.get('route')) - 1 ]
                station_name = station_data.get('station').get('name')
                words = position.split(" ")
                for word in words:
                    response = response + word + " "
                    if word == 'Destination':
                        response = response + "i.e.., " + station_name + " "
                # response = position.replace( 'Destination',station_name )
                print (response)
            else :
                response = position
        if data['response_code'] == 210 :
            response = "Looks like your train does not run on the date queried"
        if data['response_code'] == 230 :
            response = "Try again with a valid date."
        if data['response_code'] == 404 :
            response = "I could not find any live status for the requested Train"
        if data['response_code'] == 405 :
            response = "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
        return jsonify({
            "queryResult" : {
                "action" : "train_status.TrainStatus_Delayed_Final_Response",
                "fulfillmentText": response
            }
        })
