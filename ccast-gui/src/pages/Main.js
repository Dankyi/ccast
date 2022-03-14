import React, {useEffect, useState} from 'react'

function Main() {

    // Three states for trading: Idle, Dummy, and Live
    const [trading, setTrading] = useState('Idle')

    const startReal = (e) => { setTrading('Live') }
    const startFake = (e) => { setTrading('Dummy') }
    const stopTrading = (e) => { setTrading('Idle') }

    return (
        <div className='Main'>
            <h1> Welcome to CCAST </h1>
            <h3> AI trader is currently in {trading} mode. </h3>

            
            <button onClick={startReal}> Start Trading!</button>
            <button onClick={startFake}> Start Trading with fake money!</button>
            <button onClick={stopTrading}> Stop Trading</button>
            
        </div>
    )
}

export default Main
