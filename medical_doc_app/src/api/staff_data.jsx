import axios from 'axios';

const backend_url = 'http://127.0.0.1:8000/api/employees';
export const get_staff_data = async () => {
    // try {
    //     const response = await axios.get(`${backend_url}/me/`, {
    //         headers: {'Authorization': `Token ${localStorage.getItem("authToken")}`},
    //     });
    //     console.log("Staff data fetched successfully:", response.data);
    //     return response.data;
    try {
        const token = localStorage.getItem("authToken");
        console.log("Token being sent:", token); // ✅ Print the token

        const response = await axios.get(`${backend_url}/me/`, {
            headers: { 'Authorization': `Token ${token}` },
        });
        console.log("sent Token:", token); 

        console.log("Staff data fetched successfully:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error fetching staff data:", error.response.request.responseText);
        throw error;
    }
}


export const get_my_patients = async () => {
    try {
        const response = await axios.get(`${backend_url}/${localStorage.getItem('staff_id')}/my-patients/`, {
            headers: {'Authorization': `Token ${localStorage.getItem("authToken")}`},
        });
        console.log("My patients data fetched successfully:", response.data);
        return response.data;
    }
    catch (error) {
        console.error("Error fetching my patients data:", error.response.request.responseText);
        throw error;
    }
}

export const get_my_departments = async () => {
    try {
        const response = await axios.get(`${backend_url}/${localStorage.getItem('staff_id')}/my-departments/`, {
            headers: {'Authorization': `Token ${localStorage.getItem("authToken")}`},
        });
        console.log("My departments data fetched successfully:");
        return response.data;
    }
    catch (error) {
        console.error("Error fetching my departments data:", error.response.request.responseText);
        throw error;
    }
}

export const get_employee_details = async (employee_id) => {
    try {
        const response = await axios.get(`${backend_url}/find/${employee_id}/`, {
            headers: {'Authorization': `Token ${localStorage.getItem("authToken")}`},
        });
        console.log("Employee details fetched successfully:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error fetching employee details:", error.response.request.responseText);
        throw error;
    }
}