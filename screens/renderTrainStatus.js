import React, {Component} from 'react';
import { Text, View, Picker,TouchableOpacity } from 'react-native';
import { styles } from './message_style'
import { renderWelcomeText } from './renderText'
import { Dialogflow_V2 } from 'react-native-dialogflow'
import TrainLogo from './TrainLogo'


class TrainStatus extends Component {

  constructor(props){
    super(props)
    if ( props.item.item.queryResult.action == 'train_status_main' || props.item.item.queryResult.action == 'train_status_delayed_response' ){
      if ( props.item.item.queryResult.hasOwnProperty('webhookPayload') && props.item.item.queryResult.webhookPayload.actual_data ){
        trains = props.item.item.queryResult.webhookPayload.trains
        this.state = {
          pickerTrain : trains[0].number,
          confirmState : false,
          pickerEnabled : true
        }
      }
    }
    if ( props.item.item.queryResult.action == 'train_status.train_number_input' ){
      date = props.item.item.queryResult.webhookPayload.date
      this.state = {
        pickedDate : date[0],
        confirmState : false,
        pickerEnabled : true
      }
    }
  }
  requestDialogflow(query){
    console.log("Hit")
    this.props.toggle()
    this.setState({
      confirmState : true,
      pickerEnabled : false
    })
    Dialogflow_V2.requestQuery(
      query,
      result => {
        this.parseDialogFlowResponse(result)
      },
      error=>console.log(error)
    );
  }
  parseDialogFlowResponse(result){
    this.props.action(result)
    this.props.toggle()
    if ( result.queryResult.hasOwnProperty('webhookPayload')) {
      if( result.queryResult.webhookPayload.activity == 'TrainStatus_Delayed_Final_Response') {
        this.fetchTrainStatusFinalResponse(result)
      }
    }
  }
  fetchTrainStatusFinalResponse(result){
    this.props.toggle()
    fetch('https://6b85fe6c.ngrok.io/delayedResponse',{
      method:'POST',
      headers:{
        Accept:'application/json',
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({
        activity : result.queryResult.webhookPayload.activity,
        outputContexts : result.queryResult.outputContexts,
        date : result.queryResult.webhookPayload.date
      }),
    })
    .then((response) => response.json())
    .then((responseJson) => {
      this.props.action(responseJson)
      this.props.toggle()
    })
    .catch((error) => {
        console.error(error);
      });
  }
  render(){
    item = this.props.item
    if ( item.item.queryResult.action == 'train_status_main' || item.item.queryResult.action == 'train_status_delayed_response' ) {
      if ( item.item.queryResult.hasOwnProperty('webhookPayload') && item.item.queryResult.webhookPayload.actual_data ){
        trains = item.item.queryResult.webhookPayload.trains
        return (
          <View style = { styles.MessageContainerBot } >
            <TrainLogo />
            <View style = {{ flex:1 }} >
              <View style = { styles.MessageView } >
                <Text style = { styles.MessageText } >{item.item.queryResult.fulfillmentText}</Text>
              </View>
              <View >
                <Picker
                  style = {{ borderWidth : 3,borderColor: 'red' ,paddingRight: 20, flex:1 }}
                  selectedValue = {this.state.pickerTrain}
                  prompt = "Select Train"
                  mode = 'dialog'
                  onValueChange = { (itemValue, itemIndex) => {this.setState({pickerTrain: itemValue})} }
                  enabled = { this.state.pickerEnabled }
                >
                {
                  trains.map((p,i) => {
                    return(
                      <Picker.Item key={i} value={p.number} label={p.name + "-" + p.number} />
                    )
                  })
                }
                </Picker>
              </View>
              <TouchableOpacity
               onPress = { () => this.requestDialogflow( this.state.pickerTrain ) }
               disabled = {this.state.confirmState} >
                <View style = { styles.MessageView } >
                  <Text style = { styles.MessageText } >Confirm</Text>
                </View>
              </TouchableOpacity>
            </View>
          </View>
        )
      }
    }
    if ( item.item.queryResult.action == 'train_status.train_number_input' ){
      dates = item.item.queryResult.webhookPayload.date
      return (
        <View style = { styles.MessageContainerBot } >
          <TrainLogo />
          <View style = {{ flex:1 }} >
            <View style = { styles.MessageView } >
              <Text style = { styles.MessageText } >{item.item.queryResult.fulfillmentText}</Text>
            </View>
            <View>
              <Picker
                enabled = { this.state.pickerEnabled }
                selectedValue = {this.state.pickedDate}
                prompt = "Select Date"
                mode = 'dialog'
                onValueChange = { (itemValue, itemIndex) => {this.setState({pickedDate: itemValue})} }
              >
              {
                dates.map( (p,i) => {
                  return(
                    <Picker.Item key = {i} value = {p} label = {p} />
                  )
                })
              }
              </Picker>
            </View>
            <TouchableOpacity onPress = { () => this.requestDialogflow(this.state.pickedDate) } disabled = {this.state.confirmState} >
              <View style = { styles.MessageView } >
                <Text style = { styles.MessageText } >Confirm</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      )
    }
    return(
      renderWelcomeText(item)
    )
  }
}
export default TrainStatus
