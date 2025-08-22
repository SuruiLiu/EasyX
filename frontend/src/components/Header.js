import React from 'react';

const Header = ({ title }) => {
  return (
    <header style={{ padding: '20px', backgroundColor: '#f0f0f0', textAlign: 'center' }}>
      <h1>{title}</h1>
    </header>
  );
};

export default Header;
