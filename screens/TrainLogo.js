import React, {Component} from 'react';
import { View,Image } from 'react-native';
import { styles } from './message_style'

class TrainLogo extends Component{
  render(){
    return(
      <View style = { styles.iconViewStyle } >
        <Image style = { styles.iconStyle } source = { require('./assistant.png') } />
      </View>
    )
  }
}
export default TrainLogo
