from flask import request, jsonify
from railAPI_activities import RailwayDB

class EtaActivities:


    def EtaMainActivity(self,webhook_req):
        trains = []
        parameters = webhook_req.get('queryResult').get('parameters')
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        if ( parameters.get('train_number') ):
            if( parameters.get('station_name') ):
                #auto complete station name
                print( parameters.get('train_number') )
                print( parameters.get('station_name') )
                train_detail = RailwayDB().getTrainNameNumber(parameters.get('train_number'))
                stations = RailwayDB().getStationAutoSuggest(parameters.get('station_name'))
                print(train_detail)
                print(stations)
                trains.append(train_detail)
                print(trains)
                if ( type(train_detail) is dict and type(stations) is list ):
                    return jsonify({
                        "fulfillmentText" : "Do you mean?",
                        "outputContexts" : outputContexts,
                        "payload" : {
                            "actual_data" : True,
                            "trains" : trains,
                            "stations" : stations
                        }
                    })
                if ( type(train_detail) is not dict and type(stations) is list ):
                    return jsonify({
                        "fulfillmentText" : trains,
                    })
                if ( type(train_detail) is dict and type(stations) is not list ):
                    return jsonify({
                        "fulfillmentText" : stations,
                    })
                if ( type(train_detail) is not dict and type(stations) is not list ):
                    return jsonify({
                        "fulfillmentText" : "Oops! Looks like there are no trains and stations like you mentioned",
                    })

            else :
                return jsonify({
                    "fulfillmentText": "May I know the station name at which you are expecting the arrival?",
                    "outputContexts" : outputContexts,
                    "followupEventInput": {
                        "name": "ETA_fallback_error_station",
                        "languageCode": "en-US",
                    }
                })

        elif ( parameters.get( 'train_name' ) ):
            if( parameters.get('station_name') ):
                #auto complete station name
                #auto train name
                train_name = webhook_req.get('queryResult').get('parameters').get('train_name')
                station_name = webhook_req.get('queryResult').get('parameters').get('station_name')
                return jsonify({
                    "fulfillmentText": "Wait for a moment!",
                    "outputContexts" : outputContexts,
                    "payload" : {
                        "actual_data" : False,
                        "train_name" : train_name,
                        "station_name" : station_name,
                        "activity" : "ETA_Delayed_Picker_Response"
                    }
                })
                print( parameters.get('station_name') )
            else :
                return jsonify({
                    "fulfillmentText": "May I know the station name at which you are expecting the arrival?",
                    "outputContexts" : outputContexts,
                    "followupEventInput": {
                        "name": "ETA_fallback_error_station",
                        "languageCode": "en-US",
                    }
                })
                # call station name input intent
        elif ( parameters.get('station_name') ) :
            return jsonify({
                "fulfillmentText": "May I know the train name or number which you are expecting the arrival?",
                "outputContexts" : outputContexts,
                "followupEventInput": {
                    "name": "ETA_fallback_error_train",
                    "languageCode": "en-US",
                }
            })
            # auto complete station name
            # call train name input intent
            pass
        else :
            # call train name and station name input
            pass

        return jsonify({
            "fulfillmentText": "Checking Parameters"
        })

    def EtaStationActivity(self,webhook_req):
        train_name = ''
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        for context in outputContexts :
            if ( 'eta-followup' in context.get('name') ):
                train_name = context.get('parameters').get('train_name')
                break
        station_name = webhook_req.get('queryResult').get('parameters').get('station_name')
        return jsonify({
            "fulfillmentText": "Wait for a moment!",
            "outputContexts" : outputContexts,
            "payload" : {
                "actual_data" : False,
                "train_name" : train_name,
                "station_name" : station_name,
                "activity" : "ETA_Delayed_Picker_Response"
            }
        })

    def EtaTrainActivity(self,webhook_req):
        station_name = ''
        parameters = webhook_req.get('queryResult').get('parameters')
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        for context in outputContexts :
            if ( 'eta-followup' in context.get('name') ):
                station_name = context.get('parameters').get('station_name')
                break
        if( webhook_req.get('queryResult').get('parameters').get('train_number') ):
            trains = []
            train_number = webhook_req.get('queryResult').get('parameters').get('train_number')
            train_detail = RailwayDB().getTrainNameNumber(parameters.get('train_number'))
            stations = RailwayDB().getStationAutoSuggest(parameters.get('station_name'))
            print(train_detail)
            print(stations)
            trains.append(train_detail)
            print(trains)
            if ( type(train_detail) is dict and type(stations) is list ):
                return jsonify({
                    "fulfillmentText" : "Do you mean?",
                    "outputContexts" : outputContexts,
                    "payload" : {
                        "actual_data" : True,
                        "trains" : trains,
                        "stations" : stations
                    }
                })
            if ( type(train_detail) is not dict and type(stations) is list ):
                return jsonify({
                    "fulfillmentText" : trains,
                })
            if ( type(train_detail) is dict and type(stations) is not list ):
                return jsonify({
                    "fulfillmentText" : stations,
                })
            if ( type(train_detail) is not dict and type(stations) is not list ):
                return jsonify({
                    "fulfillmentText" : "Oops! Looks like there are no trains and stations like you mentioned",
                })
        else :
            train_name = webhook_req.get('queryResult').get('parameters').get('train_name')
            return jsonify({
                "fulfillmentText": "Wait for a moment!",
                "outputContexts" : outputContexts,
                "payload" : {
                    "actual_data" : False,
                    "train_name" : train_name,
                    "station_name" : station_name,
                    "activity" : "ETA_Delayed_Picker_Response"
                }
            })

    def etaDelayedPickerResoponse(self,data):
        print(data)
        trains = RailwayDB().getTrainAutoSuggest(data.get('train_name'))
        stations = RailwayDB().getStationAutoSuggest(data.get('station_name'))
        print(trains)
        print(stations)
        if ( type(trains) is list and type(stations) is list ):
            return jsonify({
                "queryResult" : {
                    "action" : "ETA_delayed_response",
                    "fulfillmentText": "Do you mean?",
                    "webhookPayload" : {
                        "actual_data" : True,
                        "trains" : trains,
                        "stations" : stations
                    }
                }
            })
        if ( type(trains) is list and type(stations) is not list ):
            return jsonify({
                "queryResult" : {
                    "action" : "ETA_delayed_response",
                    "fulfillmentText": stations
                }
            })
        if ( type(trains) is not list and type(stations) is list ):
            return jsonify({
                "queryResult" : {
                    "action" : "ETA_delayed_response",
                    "fulfillmentText": trains
                }
            })
        if ( type(trains) is not list and type(stations) is not list ):
            return jsonify({
                "queryResult" : {
                    "action" : "ETA_delayed_response",
                    "fulfillmentText": "Oops! Looks like there are no trains and stations like you mentioned",
                }
            })

    def EtaTrainStartDateActivity(self,webhook_req):
        outputContexts = webhook_req.get('queryResult').get('outputContexts')
        return jsonify({
            "fulfillmentText": "When did this train start?",
            "outputContexts" : outputContexts,
            "payload" : {
                "date" : ["Today","Yesterday","2 days Ago","3 days ago"]
            }
        })


    def ETA_Response(self,webhook_req):
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
                "activity" : "ETA_Delayed_Final_Response"
            }
        })

    def ETA_Delayed_Response(self,webhook_req):
        response = ''
        station_data = ''
        train_number = ''
        station_name = ''
        date = webhook_req.get('date')
        outputContexts = webhook_req.get('outputContexts')
        for context in outputContexts :
            if ( 'eta_station_inputeta_auto_station_train_input-followup' in context.get('name') ):
                train_number = int(context.get('parameters').get('train_number'))
                station_name = context.get('parameters').get('station_name')
                break
            if ( 'eta_train_station_autocorrect-followup' in context.get('name') ):
                train_number = int(context.get('parameters').get('train_number'))
                station_name = context.get('parameters').get('station_name')
                break
            if ( 'eta_train_inputeta_station_train_autocorrect-followup' in context.get('name') ):
                train_number = int(context.get('parameters').get('train_number'))
                station_name = context.get('parameters').get('station_name')
                break
        data = RailwayDB().getLiveTrainStatus(train_number, date)
        print(data)
        if data['response_code'] == 200 :
            for route in data.get('route'):
                if( route.get('station').get('name') == station_name ) :
                    station_data = route
                    break
            position = data['position']
            if ( station_data ):
                if station_data["scharr"] == "Source" :
                    responseText = "It reaches " + station_name + " station" + " on " + station_data['actarr_date'] + " ," + station_data['schdep']
                else :
                    responseText = "It reaches " + station_name + " station" + " on " + station_data['actarr_date'] + " ," + station_data['actarr']
                response = position + responseText
            else :
                response = station_name + " station is not in the route of the requested Train"
        if data['response_code'] == 210 :
            response = "Looks like your train does not run on the date you mentioned"
        if data['response_code'] == 230 :
            response = "Try again with a valid date"
        if data['response_code'] == 404 :
            response = "I could not find any details for the requested Train and Station entries"
        if data['response_code'] == 405 :
            response = "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
        return jsonify({
            "queryResult" : {
                "action" : "ETA_Delayed_Final_Response",
                "fulfillmentText": response
            }
        })
