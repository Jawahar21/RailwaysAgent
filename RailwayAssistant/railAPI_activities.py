from flask import Flask,jsonify
import requests

class RailwayDB:

    def getPnrStatus(self,pnr_number):
        try :
            api_key = '0dfscc3g6j'
            base_url = "https://api.railwayapi.com/v2/pnr-status/pnr/"
            complete_url = base_url + str(pnr_number) + "/apikey/" + api_key + "/"
            response_ob = requests.get(complete_url)
            result = response_ob.json()
            print(result)
            if result["response_code"] == 200:
                return jsonify({
                    "fulfillmentText": "Here is your PNR status",
                    "payload" : {
                        'type' : 'pnr_status',
                        'doj' : result.get('doj'),
                        'from_station' : result.get('from_station').get('name'),
                        'to_station' : result.get('to_station').get('name'),
                        'boarding_point': result.get('boarding_point').get('name'),
                        'reservation_upto': result.get('reservation_upto').get('name'),
                        'train': {
                            'name' : result.get('train').get('name'),
                            'number' : result.get('train').get('number')
                        },
                        'journey_class': result.get('journey_class'),
                        'passengers' : result.get('passengers')
                    }
                })
            if result["response_code"] == 220 :
                return jsonify({
                    "fulfillmentText": "Journey completed data not found"
                })
            if result["response_code"] == 221 :
                return jsonify({
                    "fulfillmentText": "PNR number you entered is not a valid one."
                })
            if result["response_code"] == 404 :
                return jsonify({
                    "fulfillmentText": "PNR status for the entered PNR not found."
                })
            if result["response_code"] == 405 or result["response_code"] == 500 :
                return jsonify({
                    "fulfillmentText": "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
                })
            else:
                return False
        except:
            return jsonify({
                "fulfillmentText": "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
            })

    def getTrainNameNumber(self,train_detail):
        try :
            api_key = '0dfscc3g6j'
            base_url = 'https://api.railwayapi.com/v2/name-number/train/'
            complete_url = base_url + str(int(train_detail)) + "/apikey/" + api_key + "/"
            print(complete_url)
            response_ob = requests.get(complete_url)
            result = response_ob.json()
            # result = {
            #   "train": {
            #     "name": None,
            #     "days": [],
            #     "classes": [],
            #     "number": None
            #   },
            #   "debit": 1,
            #   "response_code": 404
            # }
            # result = {
            #   "response_code": 200,
            #   "debit" : 1,
            #   "train": {
            #     "number": "12155",
            #     "name": "BHOPAL EXPRESS",
            #     "days": [
            #       {
            #         "day-code": "MON",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "TUE",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "WED",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "THU",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "FRI",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "SAT",
            #         "runs": "Y"
            #       },
            #       {
            #         "day-code": "SUN",
            #         "runs": "Y"
            #       }
            #     ]
            #   }
            # }
            print( result )
            if result["response_code"] == 200 :
                return {
                    "name" : result.get('train').get('name'),
                    "number" : result.get('train').get('number')
                }
            if result["response_code"] == 404 :
                return "Oops! There's no train with the mentioned train number."
            if result["response_code"] == 405 or result["response_code"] == 500 :
                return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
        except:
            return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."

    def getTrainAutoSuggest(self,train_name):
        try:
            trains = []
            api_key = '0dfscc3g6j'
            base_url = 'https://api.railwayapi.com/v2/suggest-train/train/'
            complete_url = base_url + str(train_name) + "/apikey/" + api_key + "/"
            print(complete_url)
            response_ob = requests.get(complete_url)
            result = response_ob.json()
            # result = {
            #   "response_code": 200,
            #   "debit": 1,
            #   "total": 4,
            #   "trains": [
            #     {
            #       "number": "12559",
            #       "name": "SHIV GANGA EXP"
            #     },
            #     {
            #       "number": "12560",
            #       "name": "SHIV GANGA EXP"
            #     },
            #     {
            #       "number": "52451",
            #       "name": "SHIVALK DLX EXP"
            #     },
            #     {
            #       "number": "52452",
            #       "name": "SHIVALK DLX EXP"
            #     }
            #   ]
            # }
            print(result)
            if result["response_code"] == 200 :
                if len( result['trains'] ) == 0 :
                    return "Oops! There's no train with the mentioned train details."
                for train in result.get('trains'):
                    trains.append({
                        'name' : train.get('name'),
                        'number' : train.get('number')
                    })
                return trains
            if result["response_code"] == 404 :
                return "Oops! There's no train with the mentioned train details",
            if result["response_code"] == 405 or result["response_code"] == 500 :
                return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
        except:
            return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."

    def getStationAutoSuggest(self,station_name):
        try:
            stations = []
            api_key = '0dfscc3g6j'
            base_url = 'https://api.railwayapi.com/v2/suggest-station/name/'
            complete_url = base_url + str(station_name) + "/apikey/" + api_key + "/"
            print(complete_url)
            response_ob = requests.get(complete_url)
            result = response_ob.json()
            # result = {
            #   "stations": [],
            #   "response_code": 200,
            #   "debit": 1
            # }
            # result = {
            #   "response_code": 200,
            #   "debit" : 1,
            #   "total": 2,
            #   "stations": [
            #     {
            #       "name": "MUMBAI CST",
            #       "code": "CSTM"
            #     },
            #     {
            #       "name": "MUMBAI CENTRAL",
            #       "code": "BCT"
            #     }
            #   ]
            # }

            print(result)
            if result["response_code"] == 200 :
                if len( result['stations'] ) == 0 :
                    return "Oops! I could not find the station from the entered Station Name."
                for station in result.get('stations'):
                    stations.append({
                        'name' : station.get('name'),
                    })
                return stations
            if result["response_code"] == 404 :
                return "Oops! I could not find the station from the entered Station Name.",
            if result["response_code"] == 405 or result["response_code"] == 500 :
                return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."
        except:
            return "Oops! I could not communicate with the Indian Railways. There seems to be an issue with them."

    def getLiveTrainStatus(self,train_number,date):
        try:
            api_key = '0dfscc3g6j'
            base_url = 'https://api.railwayapi.com/v2/live/train/'
            complete_url = base_url + str(train_number) + "/date/" + str(date) + "/apikey/" + api_key + "/"
            print(complete_url)
            response_ob = requests.get(complete_url)
            result = response_ob.json()
            # result = {
            #   "response_code": 200,
            #   "debit": 3,
            #   "position": "Train is at Source and late by 5 minutes",
            #   "train": {
            #     "number": "12046",
            #     "name": "CDG NDLS SHTBDI"
            #   },
            #   "route": [
            #     {
            #       "no": 1,
            #       "day": 0,
            #       "station": {
            #         "name": "CHANDIGARH",
            #         "code": "CDG"
            #       },
            #       "has_arrived": False,
            #       "has_departed": True,
            #       "distance": 0,
            #       "scharr": "Source",
            #       "schdep": "12:00",
            #       "actarr": "00:00",
            #       "actdep": "12:00",
            #       "scharr_date": "19 Nov 2015",
            #       "actarr_date": "19 Nov 2015",
            #       "latemin": 0
            #     },
            #     {
            #       "no": 2,
            #       "day": 0,
            #       "station": {
            #         "name": "AMBALA CANT JN",
            #         "code": "UMB"
            #       },
            #       "has_arrived": True,
            #       "has_departed": True,
            #       "distance": 67,
            #       "scharr": "12:40",
            #       "schdep": "12:42",
            #       "actarr": "12:40",
            #       "actdep": "12:42",
            #       "scharr_date": "19 Nov 2015",
            #       "actarr_date": "19 Nov 2015",
            #       "latemin": 0
            #     },
            #     {
            #       "no": 3,
            #       "day": 0,
            #       "station": {
            #         "name": "NEW DELHI",
            #         "code": "NDLS"
            #       },
            #       "has_arrived": True,
            #       "has_departed": False,
            #       "distance": 265,
            #       "scharr": "15:25",
            #       "schdep": "Destination",
            #       "actarr": "15:30",
            #       "actdep": "00:00",
            #       "scharr_date": "19 Nov 2015",
            #       "actarr_date": "19 Nov 2015",
            #       "latemin": 5
            #     }
            #   ]
            # }
            return result
        except:
            return {
                'response_code' : 405
            }
