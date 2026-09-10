import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '80vh',
      backgroundColor: '#0A1F44', // navy blue
      color: '#FFFFFF',
      padding: '2rem',
    }}>
      <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Welcome to SIH 26136 Platform</h1>
      <p style={{ fontSize: '1.2rem', maxWidth: '600px', textAlign: 'center', marginBottom: '2rem' }}>
        Explore innovative startup ideas, evaluate challenges, and collaborate with officials and evaluators.
      </p>
      <Link
        to="/login"
        style={{
          backgroundColor: '#FF9933', // saffron
          color: '#0A1F44',
          padding: '0.75rem 1.5rem',
          borderRadius: '0.5rem',
          textDecoration: 'none',
          fontWeight: 'bold',
        }}
      >
        Get Started
      </Link>
    </div>
  );
};

export default LandingPage;
