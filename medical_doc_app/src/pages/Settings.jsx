import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Settings.css';

function SettingsPage() {
  const navigate = useNavigate();
  return (
    <div className="settings-page-container">
      <h2>Settings</h2>
      <div className="settings-section">
        <h3>Template Settings</h3>
        <div className='edit-card'>
          <label>Checkup Records</label>
          <div className='settings-buttons'>
            <button className='settings-button'>View Template</button>
            <button className='settings-button'>Edit Template</button>
            <button className='settings-button'>Delete Template</button>
          </div>
        </div>
        <div style={{display: 'flex'}}>
          <button className= "new-item-button" style={{alignSelf: "center"}}>Create New Template</button>
          <button className= "new-item-button" style={{alignSelf: "center"}}>Capture New Template</button>
        </div>
      </div>
      <div className='settings-section'>
        <h3> My groups </h3>
        <div style={{display: 'flex'}}>
          <button className= "new-item-button" style={{alignSelf: "center"}}>Join Group</button>
          <button className= "new-item-button" style={{alignSelf: "center"}}>Create New Group</button>
        </div>
      </div>
      < button  onClick={() => {navigate("/home")}}>Back To Dashboard</button>
    </div>
  );
}

export default SettingsPage;
