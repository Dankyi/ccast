import React, {Component, useEffect, useState} from 'react'
import aiService from '../services/ai.service'
import AuthService from "../services/auth.service";

import './Main.css'

export default class Main extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        currentUser: AuthService.getCurrentUser().data,
        
        // Three states for trading: Idle, Dummy, and Live
        trading: 'Idle'
      };

      

    }
  
    render() {
      const { currentUser } = this.state;
      const { trading } = this.state;

    const startReal = (e) => { 
        if (this.state.trading == 'Live'){ return }
        this.setState({trading: 'Live'})
        var returned = aiService.startReal(currentUser.id, currentUser.marketToken, currentUser.marketSecret);      
        console.log(returned)
        }
    
    const startFake = (e) => { 
        if (this.state.trading == 'Dummy'){ return }
        this.setState({trading: 'Dummy'})
        var returned = aiService.startFake(currentUser.id, currentUser.marketToken, currentUser.marketSecret);          
        console.log(returned)  
    }
    const stopTrading = (e) => {
        if (this.state.trading == 'Idle'){ return } 
        this.setState({trading: 'Idle'})
        var returned = aiService.stop(currentUser.id);      
        console.log(returned)  
    }

    if (currentUser == null) return(
        <div className='container'>
              <h1> No Account Information in local storage. </h1>
              <p> How did you get here? </p>
          </div>
      );

    return (
        <div className="Main">
            <h1> Welcome to CCAST </h1>
                
            <h3> AI trader is currently in {trading} mode. </h3>

            
            <div className="ButtonPanel">
                <button className="RealButton" onClick={startReal}> Start Trading!</button>
                <button className="FakeButton" onClick={startFake}> Start Trading with fake money!</button>
                <button className="StopButton" onClick={stopTrading}> Stop Trading</button>
            </div>

        </div>
    )
    }
}
