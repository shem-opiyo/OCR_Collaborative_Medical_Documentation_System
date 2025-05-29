import React, {useEffect} from 'react';
import { get_patient_records } from '../api/records';
import { Link, useNavigate, useParams } from 'react-router-dom';

import '../styles/PatientDetails.css';

function PatientHistoryPage() {
  const { patientId } = useParams();
  const navigate = useNavigate()
  const [visits, setVisits] = React.useState([]);

  useEffect(() => {
    const fetchVisits = async () => {
      try {
        const response = await get_patient_records(patientId);
        console.log(response);
        setVisits(response);
      }  catch (error) {
        console.error("Error fetching patient records:", error);
      }
    }
    fetchVisits();
  }
  , [patientId]);


  return (
    <div className="patient-history-page">
      <div style={{justifyContent: 'center', display: 'flex', alignItems: 'center'}}>
        <div className='back-button' onClick={() => {navigate(`/patients/${localStorage.getItem('staff_id')}`)}}> ◀ </div>
        <h2>Patient Visit History</h2>
      </div>
      {visits.map((visit) => (
        <Link 
          key={visit.record_id} 
          to={`/patients/${localStorage.getItem('staff_id')}/patient/${patientId}/visit/${visit.record_id}`}
          className="visit-card"
        >
          <div>
            <h3>{visit.summary || "No Available summary"}</h3>
            {!visit.summary && 
              <p>Record ID: {visit.record_id}</p>}
            <p>Creator: {visit.staff} --- Date: {visit.created_at}</p>
          </div>
        </Link>
      ))}
      <div style={{justifyContent: 'space-between', display: 'flex'}}>
        <button className="add-visit-button" onClick={() => {navigate("new-visit")}}> Add New Visit </button>
        <button className="add-visit-button" onClick={() => {navigate("/home")}} style={{background: "#00c9a7"}}>Back to Dashboard</button>
      </div>
    </div>
  );
}

export default PatientHistoryPage;
