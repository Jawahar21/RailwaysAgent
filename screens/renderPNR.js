import React, {Component} from 'react';
import { Text, View } from 'react-native';
import { styles } from './message_style'
import TrainLogo from './TrainLogo'

export const renderPNR = (item) => {
  response = item.item.queryResult
  console.log(response)
  if (response.hasOwnProperty('webhookPayload')){
    data = response.webhookPayload
    return(
      <View style = { styles.MessageContainerBot } >
        <TrainLogo />
        <View style = {styles.MessageView} >
          <Text style = { styles.MessageText } >{response.fulfillmentText}</Text>
          <Text style = { styles.MessageText } >Train Name: {data.train.name}</Text>
          <Text style = { styles.MessageText } >Train Number: {data.train.number}</Text>
          <Text style = { styles.MessageText } >DOJ: {data.doj}</Text>
          <Text style = { styles.MessageText } >From Station: {data.from_station}</Text>
          <Text style = { styles.MessageText } >To Station: {data.to_station}</Text>
          <Text style = { styles.MessageText } >Reservation Upto: {data.reservation_upto}</Text>
          {
            data.journey_class.name ?
            <Text style = { styles.MessageText } >Journey Class : { data.journey_class.name }</Text>
            :
            <Text style = {styles.MessageText} >Journey Class: { data.journey_class.code } </Text> }
          {
            data.passengers.map((p,i) => {
              return(
                <View key={i} >
                  <Text style = { styles.MessageText } >Passenger: {p.no}</Text>
                  <Text style = { styles.MessageText } >Current Status: {p.current_status}</Text>
                  <Text style = { styles.MessageText } >Booking Status: {p.booking_status}</Text>
                </View>
              )
            })
          }
        </View>
      </View>
    )
  }
  else{
    return(
      <View style = { styles.MessageContainerBot } >
        <TrainLogo />
        <View style = {styles.MessageViewBot }>
          <Text style = { styles.MessageText } >{response.fulfillmentText}</Text>
        </View>
      </View>
    )
  }
}
