import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { get_visit_details } from '../api/records';
import "../styles/PatientDetails.css"
import "../styles/Settings.css"

function VisitDetailPage() {
  const navigate = useNavigate()
  const patientId = window.location.href.split("/")[6]
  const record_id = window.location.href.split("/")[8]
  const [visitDetails, setVisitDetails] = React.useState({});

  useEffect(() => {
    const fetchVisitDetails = async () => {
      try {
        console.log("Attempting to fetch visit details for record ID:", record_id);
        const response = await get_visit_details(record_id);
        console.log("Fetched visit details:", response);
        setVisitDetails(response);
      } catch (error) {
        console.error("Error fetching visit details:", error);
      }
    };
    fetchVisitDetails();
  }, [record_id]);

  return (
    <div className="visit-detail-page">
    <div style={{ justifyContent: 'center', display: 'flex', alignItems: 'center' }}>
        <div className='back-button' onClick={() => { navigate(`/patients/${localStorage.getItem('staff_id')}/patient/${patientId}`) }}>◀</div>
        <h2 style={{ marginLeft: '10px' }}>Visit Details</h2>
    </div>
    {Object.entries(visitDetails).map(([key, value]) => {
        // Define keys that should be treated as comma-separated lists
        const commaSeparatedKeys = ['symptoms', 'diagnosis', 'treatment_plan', 'family_history', 'medication'];
        const isCommaSeparated = commaSeparatedKeys.includes(key);
        let valuesArray = [];

        if (typeof value === 'string' && isCommaSeparated) {
            valuesArray = value.split(',').map(item => item.trim());
        } else if (value !== null && value !== undefined) {
            valuesArray = [String(value)];
        } else {
            valuesArray = ['N/A'];
        }

        // Define keys to exclude or handle differently
        const excludedKeys = ['record_id', 'created_at', 'updated_at', 'staff', 'patient', 'departments', 'staff_access'];
        if (excludedKeys.includes(key)) {
            let displayValue = value;
            if (key === 'created_at' || key === 'updated_at') {
                displayValue = new Date(value).toLocaleString();
            }
            return (
                <div key={key} className="detail-item">
                    <strong>{key.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase())}:</strong>
                    <span className="detail-value">{displayValue}</span>
                </div>
            );
        }

        if (key === 'departments' && value && value.length > 0) {
            return (
                <div key={key} className="detail-item aqua-container">
                    <strong>Departments:</strong>
                    {value.map((deptId, index) => (
                        <span key={index} className="detail-body">{deptId}</span>
                    ))}
                </div>
            );
        }

        if (key === 'staff_access' && value && value.length > 0) {
            return (
                <div key={key} className="detail-item aqua-container">
                    <strong>Staff Access:</strong>
                    {value.map((staffId, index) => (
                        <span key={index} className="detail-body">{staffId}</span>
                    ))}
                </div>
            );
        }

        if (isCommaSeparated) {
            return (
                <div key={key} className="detail-item aqua-container">
                    <strong>{key.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase())}:</strong>
                    {valuesArray.map((item, index) => (
                        <span key={index} className="detail-body">{item}</span>
                    ))}
                </div>
            );
        }

        return null; // Skip other keys for now to avoid redundancy
    })}
    <div style={{ justifyContent: "space-between", display: "flex", width: '90%', marginLeft: '5%' }}>
        <button className="edit-button">Edit Record</button>
        <button className="log-button">Record Access Logs</button>
    </div>
</div>
  );
}

export default VisitDetailPage;
