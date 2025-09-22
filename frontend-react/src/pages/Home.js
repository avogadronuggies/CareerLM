import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();
  return (
    <div className="bg-radial-gradient home-page">
      {/* Hero Section */}
      <section className="hero-section" id="home">
        <div className="hero-content">
          <div className="hero-badge">
            <span>🚀 Your Career Journey Starts Here</span>
          </div>
          <h1>
            Optimize your career with{" "}
            <span className="brand-highlight">CareerLM</span>
          </h1>
          <p>
            Resume optimizer, skill gap analyzer, mock interview, cold email
            generator, study planner, and dashboard — all in one platform.
          </p>
          <div className="cta-buttons">
            <button className="signup-btn" onClick={() => navigate("/auth")}>
              <span>Get Started</span>
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M5 12H19M19 12L12 5M19 12L12 19"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <button className="login-btn" onClick={() => navigate("/auth")}>
              <span>Sign In</span>
            </button>
          </div>
          <div className="hero-stats">
            <div className="stat-item">
              <span className="stat-number">10K+</span>
              <span className="stat-label">Users</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">95%</span>
              <span className="stat-label">Success Rate</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">24/7</span>
              <span className="stat-label">Support</span>
            </div>
          </div>
        </div>
        <div className="hero-image">
          <div className="image-container">
            <img
              src="https://via.placeholder.com/400x300.png?text=CareerLM+Illustration"
              alt="CareerLM"
            />
            <div className="floating-card card-1">
              <div className="card-icon">📊</div>
              <span>Analytics</span>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">🎯</div>
              <span>Goals</span>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">⚡</div>
              <span>Fast Results</span>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="about-section" id="about">
        <div className="section-header">
          <span className="section-badge">About Us</span>
          <h2>Empowering Your Career Journey</h2>
          <p className="section-description">
            CareerLM is your comprehensive career assistant, combining
            cutting-edge AI technology with proven career development strategies
            to help you achieve your professional goals.
          </p>
        </div>
        <div className="about-content">
          <div className="about-features">
            <div className="about-feature">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered</h3>
              <p>
                Advanced algorithms analyze your profile and provide
                personalized recommendations
              </p>
            </div>
            <div className="about-feature">
              <div className="feature-icon">📈</div>
              <h3>Data-Driven</h3>
              <p>
                Make informed decisions with comprehensive analytics and
                insights
              </p>
            </div>
            <div className="about-feature">
              <div className="feature-icon">🎯</div>
              <h3>Goal-Oriented</h3>
              <p>
                Set and track your career milestones with our structured
                approach
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section" id="features">
        <div className="section-header">
          <span className="section-badge">Features</span>
          <h2>Everything You Need to Succeed</h2>
          <p className="section-description">
            Comprehensive tools designed to accelerate your career growth and
            help you stand out in today's competitive market.
          </p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <h3>Resume Optimizer</h3>
            <p>
              AI-powered resume analysis and optimization for maximum impact
            </p>
            <div className="feature-arrow">→</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Skill Gap Analyzer</h3>
            <p>
              Identify missing skills and get personalized learning
              recommendations
            </p>
            <div className="feature-arrow">→</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎤</div>
            <h3>Mock Interview</h3>
            <p>
              Practice with AI-powered interviews tailored to your target role
            </p>
            <div className="feature-arrow">→</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">✉</div>
            <h3>Cold Email Generator</h3>
            <p>Create compelling outreach emails that get responses</p>
            <div className="feature-arrow">→</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3>Study Planner</h3>
            <p>Structured learning paths to develop in-demand skills</p>
            <div className="feature-arrow">→</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Dashboard</h3>
            <p>Track your progress and visualize your career growth</p>
            <div className="feature-arrow">→</div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="contact-section" id="contact">
        <div className="contact-container">
          <div className="contact-content">
            <div className="section-header">
              <span className="section-badge">Get in Touch</span>
              <h2>Ready to Transform Your Career?</h2>
              <p className="section-description">
                Have questions or need support? Our team is here to help you
                succeed.
              </p>
            </div>
            <div className="contact-info">
              <div className="contact-item">
                <div className="contact-icon">📧</div>
                <div className="contact-details">
                  <span className="contact-label">Email</span>
                  <span className="contact-value">support@careerLM.com</span>
                </div>
              </div>
              <div className="contact-item">
                <div className="contact-icon">📞</div>
                <div className="contact-details">
                  <span className="contact-label">Phone</span>
                  <span className="contact-value">+91 12345 67890</span>
                </div>
              </div>
            </div>
          </div>
          <div className="contact-cta">
            <button className="contact-btn">Start Your Journey</button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
