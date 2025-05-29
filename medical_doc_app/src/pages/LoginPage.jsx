import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import InputField from '../components/InputField';
import { login } from '../api/authentication';

import "../styles/Login.css";

function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await login(username, password);
      console.log('Logged in:', response.data);
      navigate('/home');
    } catch (error) {
      console.error('Login failed:', error.response?.data || error.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <InputField placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <InputField type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <Button onClick={handleLogin}>Login</Button>
      <Button onClick={() => {navigate('/register')}}>Not Registered?</Button>
    </div>
  );
}

export default LoginPage;
