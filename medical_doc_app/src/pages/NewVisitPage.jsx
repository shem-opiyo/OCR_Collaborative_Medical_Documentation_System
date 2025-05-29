import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/NewVisit.css';
import { create_record } from '../api/records';
import { upload_audio, upload_image } from '../api/input_processing';

function NewVisitPage() {
  const navigate = useNavigate()
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [returnMessage, setReturnMessage] = useState('');
  const [imageBlobs, setImageBlobs] = useState([]);
  const [showImageModal, setShowImageModal] = useState(false);
  const [showVideoModal, setShowVideoModal] = useState(false);

  
  const staffId = localStorage.getItem("staff_id")
  const patientId = window.location.href.split("/")[6]
  
  const [formData, setFormData] = useState({
    symptoms: '',
    patientHistory: '',
    familyHistory: '',
    medications: '',
    diagnosis: '',
  });

  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const defaults = {
      patient: patientId,
      staff: staffId,
      record_type: 'TEXT',
    }
    setFormData(prev => ({ ...prev, [name]: value }));
    setFormData(prev => ({ ...prev, ...defaults }));
  };

  const submitFile = async() =>{

  }

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);

    mediaRecorderRef.current.ondataavailable = (e) => {
      if (e.data.size > 0) {
        sendAudioChunk(e.data);
      }
    };

    mediaRecorderRef.current.start(2000); // sends data every 2s
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  const sendAudioChunk = async (blob) => {
    const audioFile = new File([blob], `captured_audio_chunk_${Date.now()}.webm`, {
      type: 'audio/webm',
    });
    const formData = new FormData();
    formData.append('audio', audioFile);

    try {
      const response = await upload_audio(formData)

      if (!response.ok) {
        const error = await response.json();
        console.error("Audio chunk upload failed", error);
      }
    } catch (err) {
      console.error("Network error uploading audio chunk", err);
    }
  };

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;
      setShowVideoModal(true); // Show video modal first
      // Wait for modal to render before setting video source
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      }, 100);
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };
  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const captureFromVideo = () => {
    const video = videoRef.current;
    if (!video || video.readyState < 2) {
      console.warn("Video not ready yet");
      return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      setImageBlobs(prev => [...prev, blob]);
    }, 'image/jpeg');
  };


  const sendAllImages = async () => {
    for (const blob of imageBlobs) {
      const imageFile = new File([blob], `captured_image_${Date.now()}.jpg`, { type: 'image/jpeg' });
      const formData = new FormData();
      formData.append('image', imageFile);
      const response = await upload_image(formData)
      console.log(response)

    }
    closeCamera();
    setShowImageModal(false);
    setImageBlobs([]); // Reset images
  };



  const handleSave = async () => {
    setLoading(true);
    const response = await create_record(formData);
    if (response !== undefined) setReturnMessage("Record saved successfully");
  }

  return (
    <div className="new-visit-container">
      <h2>New Visit Record</h2>
      { loading && (
        <div className='modal-overlay'>
          <div className='modal-content'>
            {returnMessage === "" ?  (
              <p>Saving...</p>
            ):(
              <div className='modal-content' style={{justifyContent: 'center', alignItems: 'center'}}>
                <p>{returnMessage}</p>
                <button onClick={() => {navigate(`/patients/${staffId}/patient/${patientId}`)}}>Back to Patient Records</button>
              </div>
            )}
          </div>
        </div>
      )}

      {showVideoModal && (
        <div className="modal-overlay">
          <div className="image-modal-content">
            <h3>Capture Images</h3>
            <video ref={videoRef} autoPlay playsInline style={{ width: '70%', justifyContent: 'center', zIndex: '1000' }} />
            <div style={{ marginTop: '1rem', display: 'flex', gap: '10px' }}>
              <button  className='modal-buttons' onClick={captureFromVideo}>Capture</button>
              <button  className='modal-buttons' onClick={() => {
                closeCamera();
                setShowVideoModal(false);
                if (imageBlobs.length > 0) setShowImageModal(true);
              }}>View Captured ({imageBlobs.length})</button>
              <button className='modal-buttons' onClick={() => {
                closeCamera();
                setShowVideoModal(false);
                setImageBlobs([]);
              }}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showImageModal && (
        <div className="modal-overlay">
          <div className="image-modal-content">
            <h3>Captured Images</h3>
            <div style={{ display: 'flex', flexDirection: 'row', gap: '10px', overflowX: 'auto' }}>
              {imageBlobs.map((blob, index) => (
                <img
                  key={index}
                  src={URL.createObjectURL(blob)}
                  alt={`Captured ${index}`}
                  style={{ width: '200px', height: '150px', objectFit: 'cover' }}
                />
              ))}
            </div>
            <div style={{ marginTop: '1rem', display: 'flex', gap: '10px' }}>
              <button  className='modal-buttons' onClick={sendAllImages}>Send All</button>
              <button  className='modal-buttons' onClick={() => {
                setShowImageModal(false);
                setImageBlobs([]);
              }}>Discard All</button>
              <button  className='modal-buttons' onClick={() => {
                setShowImageModal(false);
                openCamera(); // Re-open camera if needed
              }}>Add More</button>
            </div>
          </div>
        </div>
      )}

      <div className="form-scrollable">
        {Object.keys(formData).map((field) => (
          <div key={field} className="input-box">
            <label>{field.replace(/([A-Z])/g, ' $1')}</label>
            <textarea 
              name={field}
              value={formData[field]}
              onChange={handleChange}
              rows={3}
            />
          </div>
        ))}
      </div>

      {!showImageModal && !showVideoModal && (
        <div className="floating-controls">
          <button onClick={() => {navigate(`/patients/${staffId}/patient/${patientId}`)}}> Discard Record </button>
          <button 
            className={`record-btn ${recording ? 'recording' : ''}`} 
            onClick={recording ? stopRecording : startRecording}
          >
            {recording ? 'Stop Recording' : 'Record Audio'}
          </button>

          <button className="image-btn" onClick={openCamera}>
            Capture Image
          </button>

          <button className='image-button' onClick={submitFile}>
            Attatch file
          </button>

          <button onClick={handleSave}> Save Record</button>
        </div>
      )}
    </div>
  );
}

export default NewVisitPage;