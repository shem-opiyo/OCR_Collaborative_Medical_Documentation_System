import React from 'react';

function Button({ onClick, children, type = "button" }) {
  return (
    <button type={type} onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
