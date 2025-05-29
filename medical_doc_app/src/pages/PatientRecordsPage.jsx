import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import PatientCard from '../components/PatientCard';
import { get_my_patients } from '../api/staff_data';

function PatientListPage() {
  const navigate = useNavigate();
  const staffId = window.location.href.split('/')[4]; // Extract staffId from URL
  const [patients, setPatients] = useState()

  useEffect(() => {
    const getPatients = async() => {
      const data = await get_my_patients();
      setPatients(data);
    };

    getPatients();
  }, []);
  if (!patients) {
    return <div>Loading patients...</div>;
  }
  return (
    <div className="patients-container">
      <h2>Patient Records</h2>
      {patients.length === 0 ? (
        <div style={{borderWidth: ''}}>Sorry, No patients found. Try adding a patient or have a collegue share one's record with you</div>
      ) : (
        <ul>
        {patients.map((patient) => (
            <PatientCard key={patient.pk} patient={patient} />
        ))}
      </ul>
      )}
      <button onClick={() => navigate(`/patients/${staffId}/new`)}>Add New Patient</button>
      <button onClick={() => navigate('/home')}>Back to Dashboard</button>
    </div>
  );
}

export default PatientListPage;
