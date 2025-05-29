import axios from "axios";

const token = localStorage.getItem('authToken')
const image_url = 'http://127.0.0.1:8000/api/image-processing'
const audio_url = 'http://127.0.0.1:8000/api/audio-processing'

export const upload_image = async(formData) => {
    try{
        const response = await axios.post(`${image_url}/upload-image/`, formData, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        return response

    } catch (error){
        console.error("Image upload failed", error.response.request.responseText)
        throw error
    }
}

export const upload_audio = async(formData) => {
    try{
        const response = await axios.post(`${audio_url}/transcribe/`, formData, {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        return response
    } catch (error){
        console.error("Audio chunk upload failed", error.response.request.responseText)
        throw error
    }
}
