import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';
import SettingsPage from './pages/Settings';
import HomePage from './pages/HomePage';
import DepartmentPage from './pages/DepartmentPage';
import PatientRecordsPage from './pages/PatientRecordsPage';
import PatientHistory from './pages/PatientHistoryPage';
import NewPatientFormPage from './pages/NewPatientFormPage';
import EditPatientPage from './pages/EditPatientPage';
import VisitDetailPage from './pages/VisitDetailsPage';
import NewVisitPage from './pages/NewVisitPage';
import DataConfirmationPage from './pages/DataConfirmationPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/departments" element={<DepartmentPage />} />
        <Route path="/patients/:staffId" element={<PatientRecordsPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/my-departments/:staffId" element={<DepartmentPage />} />
        <Route path="/patients/:staffId/patient/:patientId" element={<PatientHistory />} />
        <Route path="/patients/:staffId/new" element={<NewPatientFormPage />} />
        <Route path="/patients/:staffId/edit-patient/:patientId" element={<EditPatientPage />} />
        <Route path="/patients/:staffId/patient/:patientId/new-visit" element={<NewVisitPage />} />
        <Route path="/patients/:staffId/patient/:patientId/visit/:visitId" element={<VisitDetailPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/data-confirmation" element={<DataConfirmationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
