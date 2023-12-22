import React, { useState, useEffect } from 'react';
import { Grid, Typography } from '@mui/material';

const YoloUploader = ({onResponseReceived, img}) => {
    // const [imageSrc, setImageSrc] = useState(null);
    const [response, setResponse] = useState(null);

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
            setResponse(responseData)

            onResponseReceived(`data:image/png;base64,${responseData.png}`);

        } catch (error) {
            console.error('Error making the request:', error);
        }
    };

    return (
        <div>
        {response ? (
            <div id="responseOutput">
                
                {response.labels.map((item, index) => (
                    // <Grid container direction="row">
                    //     <Grid item xs={12} sx={{paddingTop:'20px', paddingBottom: '25px'}}>
                    //         <Typography sx={{paddingBottom:'5px', maxWidth: '90%', borderBottom: 'solid 1px', borderColor: 'gray'}} variant='body1'>
                    //             <div>
                    //                 xmin, xmax, ymin, ymax of the detection:
                    //             </div>
                    //             <div>
                    //                 {item.xmin.toFixed(2)}, {item.xmax.toFixed(2)}, {item.ymin.toFixed(2)}, {item.ymax.toFixed(2)}
                    //             </div>
                    //         </Typography>
                    //     </Grid>
                    //     <Grid item xs={12} sx={{paddingTop:'20px', paddingBottom: '25px'}}>
                    //         <Typography sx={{paddingBottom:'5px', maxWidth: '90%', borderBottom: 'solid 1px', borderColor: 'gray'}} variant='body1'>confidence is: {item.confidence.toFixed(2)}</Typography>
                    //     </Grid>
                    // </Grid>
                    <div></div>
                ))}
                
            </div>
        ):
        (<div>
            
            {/* <Grid container direction="row">
                <Grid item xs={12} sx={{paddingTop:'20px', paddingBottom: '25px'}}>
                    <Typography sx={{paddingBottom:'5px', maxWidth: '90%', borderBottom: 'solid 1px', borderColor: 'gray'}} variant='body1'>(xmin, xmax, ymin, ymax) of the detection:</Typography>
                </Grid>
                <Grid item xs={12} sx={{paddingTop:'20px', paddingBottom: '25px'}}>
                    <Typography sx={{paddingBottom:'5px', maxWidth: '90%', borderBottom: 'solid 1px', borderColor: 'gray'}}>confidence is:</Typography>
                </Grid>
            </Grid> */}
            
        </div>
        )}
    </div>
    );
};

export default YoloUploader;
