import React from 'react';

function InputField({ type = "text", placeholder, value, onChange }) {
  return (
    <input 
      type={type} 
      placeholder={placeholder}
      value={value}
      onChange={onChange}
    />
  );
}

export default InputField;
