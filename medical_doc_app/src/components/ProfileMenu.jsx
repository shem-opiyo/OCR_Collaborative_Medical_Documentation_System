import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import "../styles/Home.css"

function ProfileMenu() {
  const [open, setOpen] = useState(false);
  const [theme, setTheme] = useState('light'); // light, dark, muted
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    console.log('Logging out...');
    navigate('/');
  };

  const selectTheme = (selectedTheme) => {
    setTheme(selectedTheme);
    console.log(`Theme changed to: ${selectedTheme}`);
    // Optional: Apply theme classes globally
  };

  return (
    <div className="profile-menu">
      <button className="profile-button" onClick={() => setOpen(!open)}>
        ☰
      </button>

      {open && (
        <div className="profile-dropdown">
          <div className="theme-selector">
            <p>Theme:</p>
            <div className="theme-options">
              {['light', 'dark', 'muted'].map((t) => (
                <div
                  key={t}
                  className={`theme-circle ${t} ${theme === t ? 'selected' : ''}`}
                  onClick={() => selectTheme(t)}
                >
                  {theme === t && <span className="checkmark">✓</span>}
                </div>
              ))}
            </div>
          </div>

          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

export default ProfileMenu;
