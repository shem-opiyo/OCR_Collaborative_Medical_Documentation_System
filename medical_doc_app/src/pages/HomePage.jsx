import React, {useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import ProfileMenu from '../components/ProfileMenu';
import {get_staff_data} from '../api/staff_data';
import StaffCard from '../components/StaffCard';
import "../styles/Home.css"

function HomePage() {
  const navigate = useNavigate()
  const [staffData, setStaffData] = useState(null); // State to hold the staff data
  const [loading, setLoading] = useState(true); // State to track loading
  const [error, setError] = useState(null);

  const goToSettings = () => navigate('/settings');
   useEffect(() => {
    const fetchStaffData = async () => {
      try {
        const data = await get_staff_data();
        setStaffData(data);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
        console.error("Error fetching staff data:", err);
      }
    };

    fetchStaffData();
  }, []); // Empty dependency array means this runs once after the initial render

  if (loading) {
    return <p>Loading staff data...</p>;
  }

  if (error) {
    return <p>Error loading staff data: {error.message || "Something went wrong."}</p>;
  }

  return (
    <div className="home-container">
      <header className="home-header">
        <Button onClick={goToSettings}>Settings</Button>
        <ProfileMenu />
      </header>
      {staffData && <StaffCard staff={staffData} />} {/* Pass the actual data */}

      <main className="dashboard-content">
        <h2>Welcome to the Medical Records Dashboard</h2>
        <div style={{ justifyContent: 'space-between', display: 'flex'}}>
          <Button onClick={() => navigate(`/patients/${staffData.id}`)}>View Patient Records</Button>
          <Button onClick={() => navigate(`/my-departments/${staffData.id}`)}>View My Departments</Button>
        </div>
      </main>
    </div>
  );
}

export default HomePage;
