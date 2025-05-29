import axios from 'axios'


export const login = async (username, password) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/login/', { username , password}, );
        const token = response.data.token;
        console.log('Token when logging in:', token);
        // Store token in localStorage
        localStorage.setItem("authToken", token);
        return response.data;
    } catch (error) {
        console.error('Login failed:', error.response?.data || error.message);
        console.error('Error details:', error.response.request.responseText);
        throw error;
    }
}

export const register = async (username, password) => {
    try{
        const response = await axios.post('http://127.0.0.1:8000/api/register/', { username , password}, );
        const token = response.data.token;
        // Store token in localStorage
        localStorage.setItem("authToken", token);
        return response.data;
    } catch (error) {
        console.error('Login failed:', error.response?.data || error.message);
        console.error('Error details:', error.response.request.responseText);
        throw error;
    }
}

