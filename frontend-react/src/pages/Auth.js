"use client"

// src/pages/Auth.js
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import "./Auth.css" // Added CSS import

function Auth() {
  const [isLogin, setIsLogin] = useState(true) // toggle between login/signup
  const [email, setEmail] = useState("")
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    // Save mock user
    localStorage.setItem("user", JSON.stringify({ email }))
    navigate("/dashboard") // redirect to dashboard
  }

  return (
    <div className="auth-page">
      {" "}
      {/* Updated container class */}
      <div className="auth-container">
        {" "}
        {/* Added inner container */}
        <div className="auth-card">
          {" "}
          {/* Added card wrapper */}
          <div className="auth-header">
            {" "}
            {/* Added header section */}
            <h1 className="auth-title">{isLogin ? "Welcome Back" : "Create Account"}</h1>
            <p className="auth-subtitle">{isLogin ? "Sign in to your account" : "Join us today"}</p>
          </div>
          <form onSubmit={handleSubmit} className="auth-form">
            {" "}
            {/* Added form class */}
            <div className="input-group">
              {" "}
              {/* Added input wrapper */}
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="auth-input" // Added input class
              />
            </div>
            <button type="submit" className="auth-button">
              {" "}
              {/* Added button class */}
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>
          <div className="auth-toggle">
            {" "}
            {/* Added toggle section */}
            <p className="toggle-text">{isLogin ? "Don't have an account?" : "Already have an account?"}</p>
            <button
              type="button"
              className="toggle-button" // Replaced inline styles with class
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Sign Up" : "Sign In"} here
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Auth