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

            // Values to prove the AI is running
            alive: False,
            startBal: 0,
            currentBal: 0,
            currentPrice: 0,
            gridAmount: 0,
            profit: 0

        };
        try {
            if (this.state.currentUser != null) {
                aiService.getStatus(this.state.currentUser.id)
                    .then(result => {
                        this.setState({ trading: result.data.data })
                    })

            }
        }
        catch (error) { }

    }


    render() {
        const { currentUser } = this.state;
        const { trading } = this.state;

        const { alive } = this.state;
        const { startBal } = this.state;
        const { currentBal } = this.state;
        const { currentPrice } = this.state;
        const { gridAmount } = this.state;
        const { profit } = this.state;


        const startReal = (e) => {
            if (this.state.trading == 'Live') { return }
            this.setState({ trading: 'Live' })
            var returned = aiService.startReal(currentUser.id, currentUser.marketToken, currentUser.marketSecret);
            console.log(returned)
        }

        const startFake = (e) => {
            if (this.state.trading == 'Dummy') { return }
            this.setState({ trading: 'Dummy' })
            var returned = aiService.startFake(currentUser.id, currentUser.marketToken, currentUser.marketSecret);
            console.log(returned)
        }
        const stopTrading = (e) => {
            if (this.state.trading == 'Idle') { return }
            this.setState({ trading: 'Idle' })
            var returned = aiService.stop(currentUser.id);
            console.log(returned)
        }

        const getInfo = async () => {
            return await aiService.getMarketInfo(currentUser.id)
        }

        const displayBalance = async (e) => {
            //this.setState({ currentBal: getMarketBalance() })
            
            await getInfo().then(
                (response) => {
                    console.log("Recieved the following: ", response)

                    this.setState({ startBal: response["BALANCE"][0]})
                    this.setState({ currentBal: response["BALANCE"][1]})
                }
            )

            console.log("Start Bal = ", this.state.startBal)            
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
                <button className='update' onClick={displayBalance} >Update</button>

            </div>
        )
    }
}
