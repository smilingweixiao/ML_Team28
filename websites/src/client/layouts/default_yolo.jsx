import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Image, Form, Navbar } from 'react-bootstrap';
import '../style/animation.css';
import '../style/line.css';
import FileUploader from '../../script/upload';
import HuggingfaceUploader from '../../script/HuggingFace';
import {Box, Typography} from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { Grid } from '@mui/material';
import Button from '@mui/material';
import Input from '@mui/material';

import YoloUploader from '../../script/yolo';

const DefaultLayout = () => {
  // const [showImage, setShowImage] = useState(true);
  const [imageSrc, setImageSrc] = useState(null);
  const [yoloSrc, setYoloSrc] = useState(null);
  const [viewPos, setViewPos] = useState('');
  const [paddle, setPaddle] = useState('');
  const [preprocess_img, setPreprocessImage] = useState(null);

  // useEffect(() => {
  //   console.log('showImage:', showImage);
  // }, [showImage]);

  const handleImageReceived = (imgSrc) => {
    setImageSrc(imgSrc);
    // setShowImage(true);
  };

  const handleYoloReceived = (yoloSrc) => {
    setYoloSrc(yoloSrc);
    // setShowImage(true);s
  };

  const handlePng = (img) => {
    setPreprocessImage(img);
  }

  const [imageError, setImageError] = useState(false);
  const [imageError2, setImageError2] = useState(false);

  const handleImageError = () => {
    setImageError(true); // 当图片加载失败时，设置状态为 true
  };
  const handleImageError2 = () => {
    setImageError2(true); // 当图片加载失败时，设置状态为 true
  };

  return (
    <>
      <Navbar className='d-flex align-items-center justify-content-center' expand={false} style={{ height: '45px', backgroundColor: '#4C230A' }}>
        <Navbar.Brand className='p-0 mx-2 mb-2' style={{ fontSize: '18px', color: '#F0E7D8', borderRadius: '10px' }} href="#">Where is mass</Navbar.Brand>
      </Navbar>
      <div className='d-flex align-items-center justify-content-center' style={{ minHeight: 'calc(100vh - 45px)', backgroundColor: '#F8F3EA' }}>
        <Container className='m-3'>
          <Row className='p-10 m-10 d-flex align-items-center justify-content-center'>
            <Col md={4} className='d-flex flex-column justify-content-center align-items-center' style={{ backgroundColor: '#F8F3EA' }}>
              {/* <Image style={{ maxWidth: '90%', borderRadius: '10px' }} src={imageSrc || "https://via.placeholder.com/300"} fluid className='img-fluid p-auto m-auto' /> */}
              <Grid container spacing={1} direction="column" alignContent={'center'} justifyItems={'center'} minWidth={'90%'}>
                <Grid item xs={6} justifyItems={'center'}>
                  <Box sx={{minHeight:'290px'}}>
                    {imageSrc ? (
                      <Image
                        justifyItems={'center'}
                        alignContent={'center'}
                        src={imageSrc}
                        alt="mammography dicom"
                        onError={handleImageError2}
                        style={{ 
                          width: '90%', 
                          height: '90%',
                          maxHeight: '290px',
                          minHeight: '90%',
                          borderRadius: '10px',
                        }}
                      />
                    ) : (
                      <Typography className='d-flex justify-content-center align-items-center' style={{width: '90%', minHeight:'290px', borderRadius: '10px', border: 'dashed 2px'}} variant="body1" component="div" sx={{ display: 'block', textAlign: 'center' }}>
                        dicom image
                      </Typography>
                    )}
                  </Box>
                </Grid>
                <Grid item xs={2}>
                  <FormControl variant="standard" sx={{
                    width: '90%',
                  }}>
                    <InputLabel id="viewPos">viewPos</InputLabel>
                    <Select
                      labelId="viewPos"
                      id="viewPos"
                      value={viewPos}
                      label="viewPos"
                      onChange={(e) => setViewPos(e.target.value)}
                    >
                      <MenuItem value={0}>Unknown</MenuItem>
                      <MenuItem value={1}>CC</MenuItem>
                      <MenuItem value={2}>MLO</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={2}>
                  <FormControl variant="standard" sx={{
                    width: '90%',
                    p: '1'
                  }}>
                    <InputLabel id="paddle">paddle</InputLabel>
                    <Select
                      labelId="paddle"
                      id="paddle"
                      value={paddle} 
                      label="paddle"
                      onChange={(e) => setPaddle(e.target.value)}
                    >
                      <MenuItem value={0}>Unknown</MenuItem>
                      <MenuItem value={1}>magnification</MenuItem>
                      <MenuItem value={2}>spot compression</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item container direction="row" xs={2}>
                    <FileUploader viewPos={viewPos} paddle={paddle} onResponseReceived={handleImageReceived} returnPng={handlePng} />
                </Grid>
              </Grid>
            </Col>
            <Col md={2} className='d-flex flex-column justify-content-center align-items-center position-relative' style={{ backgroundColor: '#F8F3EA' }}>
              <div className="d-flex justify-content-center align-items-center position-relative magnifieranimation"></div>
            </Col>
            <Col md={4} className='d-flex flex-column justify-content-center align-items-center' style={{ backgroundColor: '#F8F3EA' }}>
              <Grid container spacing={1} direction="column" alignContent={'center'} justifyItems={'center'} minWidth={'90%'}>
                <Grid item xs={6} justifyItems={'center'}>
                <Box sx={{minHeight:'290px'}}>
                  {yoloSrc ? (
                    <Image
                        justifyItems={'center'}
                        alignContent={'center'}
                        src={yoloSrc}
                        alt="mammography dicom"
                        onError={handleImageError2}
                        style={{ 
                          width: '90%', 
                          height: '90%',
                          maxHeight: '290px',
                          minHeight: '90%',
                          borderRadius: '10px',
                        }}
                      />
                  ) : (
                    <Typography className='d-flex justify-content-center align-items-center' style={{width: '90%', minHeight:'290px', borderRadius: '10px', border: 'dashed 2px'}} variant="body1" component="div" sx={{ display: 'block', textAlign: 'center' }}>
                      result image
                    </Typography>
                  )}
                </Box>
                </Grid>
                <Grid item container direction="row" xs={4} sx={{paddingBottom: '10px'}}>
                  <YoloUploader onResponseReceived={handleYoloReceived} img={preprocess_img} />
                  
                </Grid>
              </Grid>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
};

export default DefaultLayout;
