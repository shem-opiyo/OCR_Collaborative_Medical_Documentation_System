import axios from 'axios';

const backend_url = "/api/patients";
const token = localStorage.getItem("authToken");

export const delete_patient = async (patientId) => {
    try {
        const response = await axios.delete(`http://127.0.0.1:8000/api/patients/delete/${patientId}/`, {
            headers: {'Authorization': `Token ${token}`},
        });
        if (response.status === 204) {
            console.log("Patient deleted successfully");
        } else {
            console.error("Error deleting patient:", response.status);}
        return response.data;
    }
    catch (error) {
        console.error("Error deleting patient:", error.response.request.responseText);
        throw error;
    }
}
export const create_patient = async (patientData) => {
    try {
        const output = [];

        const response = await axios.post(`http://127.0.0.1:8000/api/patients/create/`, patientData, {
            headers: { 'Authorization': `Token ${token}` },
        });

        if (response.status !== 200 && response.status !== 201) {
            throw new Error("Patient creation failed");
        }

        output[0] = response.data;
        const patient_id = response.data.pk;
        const staff_id = localStorage.getItem("staff_id");

        try {
            const response2 = await axios.post(
                `http://127.0.0.1:8000/api/employees/${staff_id}/add-patient/${patient_id}/`,
                {},
                {
                    headers: { 'Authorization': `Token ${token}` },
                }
            );

            output[1] = response2.data;
        } catch (assignErr) {
            console.error("Error assigning patient, rolling back:", assignErr);
            try {
                await delete_patient(patient_id);
                console.log("Rollback delete successful");
            } catch (deleteErr) {
                console.error("Rollback delete failed:", deleteErr);
            }
        }

        return output;

    } catch (error) {
        console.error("Error creating patient:", error.response.request.responseText);
        throw error;
    }
}


export const find_patient = async (patientId) => {
    try {
        const response = await axios.get(`${backend_url}/find/${patientId}/`, {
            headers: {'Authorization': `Token ${token}`},
        });
        return response.data;
    } catch (error) {
        console.error("Error finding patient:", error.response.request.responseText);
        throw error;
    }
}

export const get_patients = async () => {
    try {
        const response = await axios.get(`${backend_url}/list`);
        return response.data;
    } catch (error) {
        console.error("Error fetching patients:", error.response.request.responseText);
        throw error;
    }
}

export const update_patient = async (patientId, data) => {
    try{
        const response = await axios.patch(`${backend_url}/update/${patientId}`, data, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        return response
    } catch (error){
        console.error("Error fetching patients:", error.response.request.responseText);
        throw error;
    }

}