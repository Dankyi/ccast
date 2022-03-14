import React, {useEffect, useState} from 'react'

function Main() {

    // Three states for trading: Idle, Dummy, and Live
    const [trading, setTrading] = useState('Idle')

    return (
        <div className='Main'>
            <h1> Welcome to CCAST </h1>
            
            <button > Start Trading!</button>
            <button > Start Trading with fake money!</button>
            <button > Stop Trading</button>
            
        </div>
    )
}

export default Main
