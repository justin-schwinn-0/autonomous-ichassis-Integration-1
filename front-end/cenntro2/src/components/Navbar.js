import React, { useState } from "react";
import Logo from "../assets/iChassisFlatBedmini.jpg";
import { Link } from "react-router-dom";
import ReorderIcon from "@mui/icons-material/Reorder";
import "../styles/Navbar.css";

function Navbar() {
  const [openLinks, setOpenLinks] = useState(false);

  const toggleNavbar = () => {
    setOpenLinks(!openLinks);
  };
  return (
    <div className="navbar">
      <div className="leftSide" id={openLinks ? "open" : "close"}>
        <h1 className="navTitle">UTD Senior Design </h1>
        <img src={Logo} alt="Cenntro's iChassis flatbed used as website icon." />
        <div className="hiddenLinks">
          <Link to="/"> Home </Link>
          <Link to="/present"> Present </Link>
          <Link to="/about"> About Us </Link>
        </div>
      </div>
      <div className="rightSide">
        <Link to="/"> Home </Link>
        <Link to="/present"> Present </Link>
        <Link to="/about"> About Us </Link>

        <button onClick={toggleNavbar}>
          <ReorderIcon />
        </button>
      </div>
    </div>
  );
}

export default Navbar;