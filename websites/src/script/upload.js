import React, { useState } from 'react';

const FileUploader = ({ viewPos, paddle, onResponseReceived, returnPng }) => {
    // const [imageSrc, setImageSrc] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        sendDataToApi(file, viewPos, paddle);
    };

    const sendDataToApi = async (dicomFile, viewPos, paddle) => {
        try {
            // Use FormData to send file and other data
            const formData = new FormData();
            formData.append('dicom', dicomFile); // Append the file
            formData.append('view_pos', viewPos); // Append other data
            formData.append('paddle', paddle);

            const response = await fetch('http://127.0.0.1:5000/api', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            console.log(responseData);

            onResponseReceived(`data:image/png;base64,${responseData.png}`);
            returnPng(`data:image/png;base64,${responseData.png}`)
        } catch (error) {
            console.error('Error making the request:', error);
        }
    };

    return (
        <div>
            <input type="file" id="dicomInput" onChange={handleFileChange} />
            {/* {imageSrc && <img src={imageSrc} alt="Processed" />} */}
        </div>
    );
};

export default FileUploader;
