import React, {Component} from 'react';
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create(
  {
    MessageContainerUser : {
      padding : 4,
      flexDirection: 'row',
      justifyContent : 'flex-end',
      alignItems : 'center',
    },
    MessageContainerBot : {
      padding : 4,
      flexDirection: 'row',
      justifyContent : 'flex-start',
      alignItems : 'center',
    },
    MessageText : {
      flex : 1,
      fontSize : 18,
      color : '#000000',
      flexWrap: 'wrap'
    },
    MessageViewUser : {
      padding : 10,
      marginLeft : 35,
      marginRight : 8,
      marginVertical : 2,
      backgroundColor : '#EFFFD0',
      borderRadius : 8,
      elevation: 3,

    },
    MessageViewBot : {
      padding : 10,
      marginLeft : 8,
      marginRight : 35,
      marginVertical : 1,
      backgroundColor : '#ffffff',
      borderRadius : 8,
      elevation: 3
    },
    iconViewStyle : {
      borderStyle : 'solid',
      borderColor : '#ffffff',
      borderWidth : 2,
      elevation:3,
      borderRadius : 50
    },
    iconStyle : {
      height : 30,
      width : 30,
    }
  }
)
