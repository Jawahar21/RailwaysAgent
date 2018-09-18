import React, {Component} from 'react';
import { View,Image } from 'react-native';
import { styles } from './message_style'

class UserLogo extends Component{
  render(){
    return(
      <View style = { styles.iconViewStyle } >
        <Image style = { styles.iconStyle } source = { require('./user.png') } />
      </View>
    )
  }
}
export default UserLogo
