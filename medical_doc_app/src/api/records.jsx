import axios from "axios";

const backend_url = 'http://127.0.0.1:8000/api/records'
const token = localStorage.getItem("authToken")
export const create_record = async (data) => {
    try {
        console.log(data)
        const response = await axios.post(`${backend_url}/create/`, data, {
        headers: {
            "Content-Type": "multipart/form-data",
            "Authorization": `Token ${token}`,
        },
        });
        return response.data;
    } catch (error) {
        console.error("Error creating record:", error.response.request.responseText);
        throw error;
    }
}

export const get_patient_records = async (patient_id) => {
    try {
        const response = await axios.get(`${backend_url}/patient/${patient_id}/get-records/`, {
            headers: {
                "Authorization": `Token ${token}`,
            },
        });
        return response.data;
    } catch(error) {
        console.error("Error fetching patient records:", error.response.request.responseText);
        throw error;
    }
}

export const get_visit_details = async (record_id) => {
    try {
        const response = await axios.get(`${backend_url}/get-record/${record_id}/`, {
            headers: {
                "Authorization": `Token ${token}`,
            },
        });
        return response.data;
    } catch(error) {
        console.error("Error fetching visit details:", error.response.request.responseText);
        throw error;
    }
}