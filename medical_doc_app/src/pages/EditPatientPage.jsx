import React, {useEffect, useState} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { delete_patient, find_patient } from '../api/patients';

function EditPatientPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  let url = window.location.href
  const staffId = url.split("/")[4]
  const patientId = url.split("/")[6]

  const [patient, setPatient] = useState(null)

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        setPatient(await find_patient(patientId))
      }
      catch (error) {
        console.error("Error fetching patient data:", error);
      }
    }
    fetchPatient();
  }, [patientId]);

  async function handleDelete() {
    try{ 
      const response = await delete_patient(patientId)
      console.log("Patient deleted successfully:", response);
      navigate(`/patients/${staffId}`);
    }
    catch (error) {
      console.error("Error deleting patient:", error);}
  }
  return (
    <div className="edit-patient-container">
      <h2>{id === 'new' ? 'Add New Patient' : `Edit Patient ${id}`}</h2>
      <input type="text" placeholder={patient? patient.name: "Patient Name"} />
      <input type="date" />
      <input type="text" placeholder={patient? patient.phone: "Patient Phone Number"}/>
      <button onClick={() => navigate(`/patients/${staffId}`)}>Save Changes</button>
      <button style={{background: 'rgb(247, 115, 115)'}} onClick={handleDelete}>Delete Patient</button>
      <button onClick={() => navigate(`/patients/${staffId}`)}>Cancel</button>
    </div>
  );
}

export default EditPatientPage;
