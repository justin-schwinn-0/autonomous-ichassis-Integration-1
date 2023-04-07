import React from 'react'
import Banner from "../assets/background.jpg";
import { Link } from "react-router-dom";
import '../styles/home.css';

function home() {
  return (
    <div className="home" style={{ backgroundImage: `url(${Banner})` }}>
      <div className="headerContainer" >
        <h1>Cenntro's iChassis</h1>
        <p>AI Driven Vehicles</p>
        {/* // need to fix external linking */}
        <Link to={{ pathname: 'https://cenntroauto.com/' }}>
          <button> Cenntro Official Website </button>
        </Link>
      </div>
    </div>
    
  )
}

export default home