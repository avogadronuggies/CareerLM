import React from "react";
import { Routes, Route } from "react-router-dom"; // <-- only import Routes & Route
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Auth from "./pages/Auth";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  return (
    <>
      {/* Sticky Navbar on top */}
      <Navbar />

      {/* Page content */}
      <Routes>
        <Route path="/" element={<Home />} /> 
        <Route path="/auth" element={<Auth />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </>
  );
}

export default App;
