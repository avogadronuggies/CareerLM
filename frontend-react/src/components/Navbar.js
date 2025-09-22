import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  // Function to scroll to sections within the home page
  const scrollToSection = (id) => {
    const section = document.getElementById(id);
    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">CareerLM</Link>
      </div>
      <div className="navbar-links">
        {/* Scroll to sections */}
        <button onClick={() => scrollToSection("home")}>Home</button>
        <button onClick={() => scrollToSection("about")}>About</button>
        <button onClick={() => scrollToSection("contact")}>Contact</button>

        {/* Navigate to auth page */}
        <button className="login-btn" onClick={() => navigate("/auth")}>
          Login
        </button>
        <button className="signup-btn" onClick={() => navigate("/auth")}>
          Sign Up
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
