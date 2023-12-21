import React, { useState } from 'react';

const YoloUploader = ({onResponseReceived}) => {
    // const [imageSrc, setImageSrc] = useState(null);

    const sendDataToApi = async () => {
        try {

            const response = await fetch('http://127.0.0.1:5000/yolo', {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const responseData = await response.json();
            console.log(responseData);

            onResponseReceived(`data:image/png;base64,${responseData.png}`);

        } catch (error) {
            console.error('Error making the request:', error);
        }
    };

    return (
        <div>
            {(
                <div id="responseOutput">
                    hello
                </div>
            )}
        </div>
    );
};

export default YoloUploader;
