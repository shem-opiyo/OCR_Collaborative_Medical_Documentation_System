import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import InputField from '../components/InputField';
import Button from '../components/Button';

import "../styles/Login.css";
import { register } from '../api/authentication';

function RegistrationPage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [department, setDepartment] = useState('');

  const handleRegister = async () => {
    try {
      const response = await register(name, password)
      console.log('Registered:', response.data);
      navigate('/home');
    } catch (error) {
      console.error('Registration failed:', error.response?.data || error.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Register</h2>
      <InputField placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <InputField type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <InputField placeholder="Department Name" value={department} onChange={e => setDepartment(e.target.value)} />
      <Button onClick={handleRegister}>Register</Button>
      <Button onClick={() => {navigate('/')}}>Already Registered?</Button>
    </div>
  );
}

export default RegistrationPage;
