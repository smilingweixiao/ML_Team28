import React, { useState } from 'react';
import { Button, Grid } from '@mui/material';
import Input from '@mui/material/Input';


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
        <Grid item container direction="row" xs={12}>
            <Grid item 
                xs={6}
                container
                spacing={1}
                direction="column"
                // alignItems={'center'}
                marginTop={2}>
                    {/* <input type="file" id="dicomInput" onChange={handleFileChange} /> */}
                    {/* {imageSrc && <img src={imageSrc} alt="Processed" />} */}
                <Button
                    variant="contained"
                    component="label"
                    sx={{
                        backgroundColor: '#4C230A',
                        maxWidth: '90%',
                        fontSize: '10px'
                    }}
                >Upload file
                    <Input
                        type="file"
                        id="dicomInput"
                        onChange={handleFileChange}
                        hidden
                        sx={{
                            color: '#4C230A'
                        }}
                    />
                </Button>
            </Grid>
            <Grid item 
                xs={6}
                container
                spacing={1}
                direction="column"
                // alignItems={'center'}
                marginTop={2}>
                    {/* <input type="file" id="dicomInput" onChange={handleFileChange} /> */}
                    {/* {imageSrc && <img src={imageSrc} alt="Processed" />} */}
                <Button
                    variant="contained"
                    component="label"
                    sx={{
                        backgroundColor: '#4C230A',
                        maxWidth: '90%',
                        fontSize: '10px'
                    }}
                >Enter
                    <Input
                        type="file"
                        id="dicomInput"
                        onChange={handleFileChange}
                        hidden
                        sx={{
                            color: '#4C230A'
                        }}
                    />
                </Button>
            </Grid>
        </Grid>
    );
};

export default FileUploader;
