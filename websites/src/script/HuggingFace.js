import React, { useState, useEffect } from 'react';

const HuggingfaceUploader = ({ img }) => {
    const [response, setResponse] = useState(null);
    const url = "https://api-inference.huggingface.co/models/Tommybear1136/convnext_mass_detection";

    useEffect(() => {
        if (img) {
            sendDataToApi(img);
        }
    }, [img]);

    const sendDataToApi = (base64Img, retryCount = 0, maxRetries = 3) => {
        let max = 0;
        let res;

        const data = {
            inputs: {
                image: base64Img.split(',')[1]
            }
        };

        fetch(url, {
            headers: {
                Authorization: "Bearer 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",
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            method: "POST",
        })
            .then(response => response.json())
            .then(data => {
                if (data.error && data.error === "Model Tommybear1136/convnext_mass_detection is currently loading") {
                    if (retryCount < maxRetries) {
                        console.log(`Model is loading, retrying in ${data.estimated_time} seconds...`);
                        setTimeout(() => sendDataToApi(base64Img, retryCount + 1, maxRetries), data.estimated_time * 1000);
                    } else {
                        console.error('Model loading failed after maximum retries.');
                    }
                } else {
                    console.log(data);
                    // for (let i = 0; i < data.length; i++) {
                    //     if (data[i].score > max) {
                    //         max = data[i].score;
                    //         res = data[i].label;
                    //     }
                    // }
                    // setResponse(res);
                    setResponse(data);
                }
            })
            .catch((e) => {
                console.log(e);
            });
    };

    return (
        <div>
            {response && (
                <div id="responseOutput">
                    {response.map((item, index) => (
                        <div key={index}>
                            Label: {item.label}, Score: {item.score.toFixed(2)}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default HuggingfaceUploader;
