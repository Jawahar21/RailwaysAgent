from flask import request, jsonify
from pnr_tasks import PNRActivities
from eta_tasks import EtaActivities
from train_status_tasks import TrainStatusActivities

class Activites:

    def checkActivity(self):
        webhook_req = request.get_json()
        action = webhook_req.get('queryResult').get('action')
        print(action)
        if 'pnr_status' in action :
            return Activites().callPNRActivities(action,webhook_req)
        if 'ETA' in action :
            return Activites().callEtaActivities(action,webhook_req)
        if 'train_status' in action :
            return Activites().callTrainStatusActivities(action, webhook_req)

    def callPNRActivities(self,activity,webhook_req):
        if activity == 'pnr_status_main':
            return PNRActivities().PNRMainActivity(webhook_req)
        if activity == 'pnr_status_number':
            return PNRActivities().PNRMainActivity(webhook_req)

    def callEtaActivities(self,activity,webhook_req):
        if activity == 'ETA_main':
            return EtaActivities().EtaMainActivity(webhook_req)
        if activity == 'ETA_station_input':
            return EtaActivities().EtaStationActivity(webhook_req)
        if activity == 'ETA_station_input.ETA_station_input-custom':
            return EtaActivities().EtaTrainStartDateActivity(webhook_req)
        if activity == 'ETA_station_input.ETA_train_start_date' :
            return EtaActivities().ETA_Response(webhook_req)
        if activity == 'ETA_main_train_number_station_autocorrect' :
            return EtaActivities().EtaTrainStartDateActivity(webhook_req)
        if activity == 'ETA_main_train_start_date' :
            return EtaActivities().ETA_Response(webhook_req)
        if activity == 'ETA_train_input':
            return EtaActivities().EtaTrainActivity(webhook_req)
        if activity == 'ETA_train_input.ETA_train_input-custom':
            return EtaActivities().EtaTrainStartDateActivity(webhook_req)
        if activity == 'ETA_train_input.ETA_train_startdate' :
            return EtaActivities().ETA_Response(webhook_req)

    def callTrainStatusActivities(self,activity,webhook_req):
        if activity == 'train_status_main':
            return TrainStatusActivities().trainStatusMainActivity(webhook_req)
        if activity == 'train_status.train_number_input':
            return TrainStatusActivities().TrainStartDateActivity(webhook_req)
        if activity == 'train_status.train_starting_date':
            return TrainStatusActivities().trainStatusResponse(webhook_req)

    def callDelayedResoponse(self):
        print("Resquest HIT")
        req_obj = request.get_json()
        print(req_obj)
        if req_obj.get('activity') == 'ETA_Delayed_Picker_Response' :
            return EtaActivities().etaDelayedPickerResoponse(req_obj)

        if req_obj.get('activity') == 'ETA_Delayed_Final_Response' :
            return EtaActivities().ETA_Delayed_Response(req_obj)

        if req_obj.get('activity') == 'TrainStatus_Delayed_Picker_Response' :
            return TrainStatusActivities().trainStatusPickerDelayedResponse(req_obj)

        if req_obj.get('activity') == 'TrainStatus_Delayed_Final_Response' :
            print("Inisde deplayed final response")
            return TrainStatusActivities().trainStatusDelayedResponse(req_obj)
