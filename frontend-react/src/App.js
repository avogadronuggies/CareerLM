import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Auth from "./pages/Auth";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  const navigate = useNavigate();

  return (
    <div className="App">
      {/* Page content */}
      <Routes>
        {/* Home page with About & Contact sections */}
        <Route path="/" element={<Home />} />

        {/* Auth page (login/signup) */}
        <Route
          path="/auth"
          element={
            <Auth
              onLoginSuccess={(data) => {
                console.log("Login successful!", data);
                navigate("/dashboard"); // redirect after login
              }}
              onRegisterSuccess={(data) => {
                console.log("Registration successful!", data);
                navigate("/dashboard"); // redirect after signup
              }}
            />
          }
        />

        {/* Main dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
