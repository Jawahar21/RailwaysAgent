import React, {Component} from 'react';
import { Text, View,StyleSheet,TextInput,FlatList, TouchableOpacity, Image } from 'react-native';
import Modal from "react-native-modal";
import { Dialogflow_V2 } from 'react-native-dialogflow'
import { renderUserText, renderWelcomeText } from './renderText'
import { renderPNR } from './renderPNR'
import ETA  from './renderETA'
import TrainStatus  from './renderTrainStatus'

class Conversation extends Component{

  constructor(){
    super()
    this.state = {
      userQuery : '',
      flatListData : [],
      isLoading : false,
      actionsVisible : false
    }
    this.ETAPickerResponserHandler = this.ETAPickerResponserHandler.bind(this);
    this.toggleLoadingState = this.toggleLoadingState.bind(this);
  }

  componentDidMount(){
    Dialogflow_V2.requestQuery(
      "Hi",
      result => {
        this.parseDialogFlowResponse(result)
      },
      error=> { console.log("Error situation!!!!!!");console.log(error)}
    );
  }

  componentDidUpdate() {
    this.fl.scrollToEnd({ animated : true })
    setTimeout( () => this.fl.scrollToEnd({ animated : true }) ,500)
  }

  requestDialogflow(text){
    if( text == ''){
      return
    }
    this.textInput.clear();
    item = {
      'type' : 'userText',
      'data' : text
    }
    this.setState({
      flatListData : [...this.state.flatListData,item],
      userQuery : '',
      isLoading : true
    })
    Dialogflow_V2.requestQuery(
      text,
      result => {
        this.parseDialogFlowResponse(result)
      },
      error=> { console.log("Error situation!!!!!!");console.log(error)}
    );
  }

  fetchActualTrainStationData(result){
    this.setState({
      isLoading : true
    })
    fetch('https://6b85fe6c.ngrok.io/delayedResponse',{
      method:'POST',
      headers:{
        Accept:'application/json',
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({
        activity : result.queryResult.webhookPayload.activity,
        train_name : result.queryResult.webhookPayload.train_name,
        station_name : result.queryResult.webhookPayload.station_name,
      }),
    })
    .then((response) => response.json())
    .then((responseJson) => {
        this.setState({
          flatListData : [...this.state.flatListData,responseJson],
          isLoading : false
        })
    })
    .catch((error) => {
        console.error(error);
      });
  }

  parseDialogFlowResponse(result){
    if ( result.hasOwnProperty('webhookStatus') ){
      if ( result.webhookStatus.hasOwnProperty('code')){
          result.queryResult['fulfillmentText'] = "Oops! I missed it. Please try Again"
      }
    }
    this.setState({
      flatListData : [...this.state.flatListData,result],
      isLoading : false
    })
    if( result.queryResult.action == 'ETA_station_input' ){
      this.fetchActualTrainStationData(result)
    }
    if( result.queryResult.action == 'ETA_main' || result.queryResult.action == 'ETA_train_input' ){
      if ( result.queryResult.hasOwnProperty('webhookPayload')){
        if ( result.queryResult.webhookPayload.actual_data == false){
          this.fetchActualTrainStationData(result)
        }
      }
    }
    if( result.queryResult.action == 'train_status_main'  ){
      if ( result.queryResult.hasOwnProperty('webhookPayload')){
        if ( result.queryResult.webhookPayload.actual_data == false){
          this.fetchActualTrainStationData(result)
        }
      }
    }

  }
  renderConversation(item){
    console.log(item)
    if ( item.item.type == 'userText' ){
      return renderUserText(item)
    }
    if( item.item.queryResult.action == 'input.welcome' ){
      return renderWelcomeText(item)
    }
    if( item.item.queryResult.action == 'input.unknown' ){
      return renderWelcomeText(item)
    }
    if ( item.item.queryResult.action.includes('pnr_status')){
      return renderPNR(item)
    }
    if ( item.item.queryResult.action.includes('ETA')){
      return <ETA item = {item} action = {this.ETAPickerResponserHandler} toggle = {this.toggleLoadingState} />
    }
    if ( item.item.queryResult.action.includes('smalltalk')){
      return renderWelcomeText(item)
    }
    if ( item.item.queryResult.action.includes('train_status')) {
      return <TrainStatus item = {item} action = {this.ETAPickerResponserHandler} toggle = {this.toggleLoadingState} />
    }
  }
  renderFooter = () => {
    if ( this.state.isLoading == false ){
      return null
    }
    return (
      <View>
        <Text>Railways Agent is typing...</Text>
      </View>
    )
  }
  ETAPickerResponserHandler(result) {
    this.setState({
      flatListData : [...this.state.flatListData,result]
    })
    console.log(this.state.flatListData)
  }
  toggleLoadingState() {
    this.setState({
      isLoading : !this.state.isLoading
    })
    this.fl.scrollToEnd({ animated : true })
    setTimeout( () => this.fl.scrollToEnd({ animated : true }) ,500)
  }
  toggleActionsVisibilityState(){
    this.setState({
      actionsVisible : ! this.state.actionsVisible
    });
  }
  render(){
    return(
      <View style = {styles.container} >
        <Modal
          style = {{ paddingBottom: 50 , justifyContent : 'flex-end', alignItems : 'center' }}
          animationType = "slide"
          isVisible = { this.state.actionsVisible }
          onRequestClose = { () => this.toggleActionsVisibilityState() }
          transparent = { true }
          backdropColor = 'transparent'
          onBackdropPress = { () => this.toggleActionsVisibilityState() }
          onSwipe = { () => this.toggleActionsVisibilityState() }
          swipeDirection = 'down'
        >
          <View style = { styles.actionsView } >
            <TouchableOpacity>
              <View style = { styles.actionItem } >
                <Image style = { styles.iconSize } source = { require('./ETA.png') } />
                <Text style = { styles.actionsText } >ETA</Text>
              </View>
            </TouchableOpacity>
            <TouchableOpacity>
              <View style = { styles.actionItem } >
                <Image style = { styles.iconSize } source = { require('./live_status.png') } />
                <Text style = { styles.actionsText } >Live train status</Text>
              </View>
            </TouchableOpacity>
            <TouchableOpacity>
              <View style = { styles.actionItem } >
                <Image style = { styles.iconSize } source = { require('./pnr_status.png') } />
                <Text style = { styles.actionsText } >PNR status</Text>
              </View>
            </TouchableOpacity>
          </View>
        </Modal>
        <View style = {styles.flatListView}>
          <FlatList
            data = {this.state.flatListData}
            renderItem = { (item) => this.renderConversation(item) }
            keyExtractor = { (item, index) => index.toString() }
            ref = {(c) => this.fl = c}
            onLayout = { () => this.fl.scrollToEnd( { animated: true } ) }
            ListFooterComponent = { this.renderFooter }
          />
        </View>
        <View style = {styles.messageInputContainer}>
          <View style = {styles.TextInputView} >
            <View style = {styles.TextInputContainer} >
              <TextInput
                style = { styles.TextInput }
                onChangeText = { (text) =>  this.setState({userQuery:text}) }
                onSubmitEditing = { () => { this.requestDialogflow(this.state.userQuery)}}
                ref = {input => { this.textInput = input }}
                blurOnSubmit = {false}
                placeholder = 'Type your message here.'
                placeholderTextColor = '#949494'
              />
            </View>
            <View style = { styles.SendButtonContainer } >
              <TouchableOpacity onPress = { () => { this.requestDialogflow(this.state.userQuery)}} >
                <View>
                  <Image style = {{ width:30,height:30 }} source = { require('./send.png') } />
                </View>
              </TouchableOpacity>
            </View>
          </View>
          <View style = {styles.moreOptionsView} >
            <TouchableOpacity onPress = { () => this.toggleActionsVisibilityState() }>
              <View>
                <Image style = {{ width:30,height:40 }} source = { require('./more.png') } />
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    );
  }
}
const styles = StyleSheet.create(
  {
    container : {
      flex: 1,
      backgroundColor : '#F5F5F5',
      flexDirection: 'column',
      justifyContent: 'space-between',
    },
    TextInputView : {
      flexDirection : 'row',
      borderStyle : 'solid',
      borderColor : '#707070',
      borderWidth : 1,
      borderRadius : 100,
      flex : 7
    },
    moreOptionsView : {
      flex : 0.5,
      justifyContent : 'center'
    },
    flatListView : {
      flex : 7,
    },
    TextInput : {
      backgroundColor : '#ffffff',
    },
    TextInputContainer : {
      flex : 5,
      paddingLeft : 20
    },
    SendButtonContainer : {
      justifyContent : 'center',
      alignItems : 'center',
      flex : 1
    },
    messageInputContainer : {
      padding : 5,
      backgroundColor : '#ffffff',
      flexDirection : 'row'
    },
    actionsView : {
      backgroundColor : '#ffffff',
      flexDirection : 'row',
      justifyContent : 'space-between',
      padding : 5,
      elevation : 3,
      borderRadius : 8,

    },
    actionsText : {
      fontSize : 13,
      color : '#78849E',
    },
    actionItem : {
      justifyContent : 'center',
      alignItems : 'center',
      padding : 10
    },
    iconSize : {
      width: 20,
      height: 20
    }
  }
)
export default Conversation
