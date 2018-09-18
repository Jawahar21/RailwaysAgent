import React, {Component} from 'react';
import { createStackNavigator } from 'react-navigation';

import Conversation from './screens/conversation';
import SplashScreeen from './screens/splashscreen'

class Route extends Component{
  render(){
    return(
      <RootStack />
    );
  }
}
 const RootStack = createStackNavigator(
   {
     ConversationScreen : {
       screen : Conversation,
       navigationOptions: {
         title : 'Passengers Assistant',
         headerStyle: {
           backgroundColor: '#607D8B',
         },
         headerTintColor: '#ffffff'
       }
     },
     SplashScreeen : {
       screen : SplashScreeen,
       navigationOptions : {
         header: null,
       }
     }
   },
   {
     initialRouteName: 'SplashScreeen',
     headerMode: 'screen'
   }
 )

export default Route
