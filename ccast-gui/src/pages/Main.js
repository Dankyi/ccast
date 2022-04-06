import React, { Component, useEffect, useState } from 'react'
import aiService from '../services/ai.service'
import AuthService from "../services/auth.service";

import './Main.css'

export default class Main extends Component {
    constructor(props) {
        super(props);

        

        this.state = {
            currentUser: AuthService.getCurrentUser().data,

            // Three states for trading: Idle, Dummy, and Live
            
            trading: 'Idle',

            aiInfo: '',

            // Values to prove the AI is running
            startBal: 0,
            currentBal: 0
        };
        try{
            if (this.state.currentUser != null){
                aiService.getStatus(this.state.currentUser.id)
                .then(result => 
                    {
                        this.setState({ trading: result.data.data })
                    })
                
            }
        }
        catch(error){}
        
    }


    render() {
        const { currentUser } = this.state;
        const { trading } = this.state;

        const { aiInfo } = this.state;

        const { startBal } = this.state;
        const { currentBal } = this.state;


        const startReal = (e) => {
            if (this.state.trading == 'Live') { return }
            this.setState({ trading: 'Live' })
            var returned = aiService.startReal(currentUser.id, currentUser.marketToken, currentUser.marketSecret);
            console.log(returned)
            this.setState({ startBal: getMarketBalance() })
        }

        const startFake = (e) => {
            if (this.state.trading == 'Dummy') { return }
            this.setState({ trading: 'Dummy' })
            var returned = aiService.startFake(currentUser.id, currentUser.marketToken, currentUser.marketSecret);
            console.log(returned)
            this.setState({ startBal: getMarketBalance() })
        }
        const stopTrading = (e) => {
            if (this.state.trading == 'Idle') { return }
            this.setState({ trading: 'Idle' })
            var returned = aiService.stop(currentUser.id);
            console.log(returned)
        }

        const getMarketBalance = (e) => {
            do{
            aiService.getMarketBalance(currentUser.id).then(
                result => this.setState({ aiInfo: result })
            )
            console.log(this.state.aiInfo)}
            while (this.state.aiInfo === undefined)
            
            try {
                return this.state.aiInfo.BALANCE;
            }
            finally { 
                return "Undefined" 
            }
        }

        const displayMarketBalance = (e) => {
            this.setState({ currentBal: getMarketBalance() })
            console.log("Current Bal = ", this.state.currentBal)
        }

        if (currentUser == null) return (
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

                <h3> The starting balance was {startBal}. The current balance is {currentBal}.</h3>
                <button className='update' onClick={displayMarketBalance} >Update</button>

            </div>
        )
    }
}
