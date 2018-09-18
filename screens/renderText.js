import React, {Component} from 'react';
import { Text, View } from 'react-native';
import { styles } from './message_style'
import UserLogo from './userLogo'
import TrainLogo from './TrainLogo'

export const renderUserText = (item) => {
  return(
    <View style = { styles.MessageContainerUser }>
      <View style = { styles.MessageViewUser } >
        <Text style = { styles.MessageText } >{item.item.data}</Text>
      </View>
      <UserLogo />
    </View>
  );
}

export const renderWelcomeText = (item) => {
  return(
    <View style = { styles.MessageContainerBot } >
      <TrainLogo />
      <View style = { styles.MessageViewBot }>
        <Text style = { styles.MessageText } >{item.item.queryResult.fulfillmentText}</Text>
      </View>
    </View>
  );
}
