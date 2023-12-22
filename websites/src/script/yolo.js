import React, { useState, useEffect } from 'react';

const YoloUploader = ({onResponseReceived, img}) => {
    // const [imageSrc, setImageSrc] = useState(null);

    useEffect(() => {
        if (img) {
            sendDataToApi(img);
        }
    }, [img]);

    const sendDataToApi = async () => {
        try {
            console.log('yolo')
            const formData = new FormData();
            const response = await fetch('http://127.0.0.1:5000//api//detect', {
                method: 'POST',
                body: formData,
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
