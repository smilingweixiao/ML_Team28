import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Image, Form, Navbar } from 'react-bootstrap';
import '../style/animation.css';
import '../style/line.css';
import FileUploader from '../../script/upload';
import HuggingfaceUploader from '../../script/HuggingFace';

const DefaultLayout = () => {
  // const [showImage, setShowImage] = useState(true);
  const [imageSrc, setImageSrc] = useState(null);
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

  const handlePng = (img) => {
    setPreprocessImage(img);
  }

  return (
    <>
      <Navbar expand={false} style={{ height: '45px', backgroundColor: '#4C230A' }}>
        <Navbar.Brand className='p-0 mx-2 mb-4' style={{ fontSize: '15px', color: '#F0E7D8', borderRadius: '10px' }} href="#">Where is mass</Navbar.Brand>
      </Navbar>
      <div className='d-flex align-items-center justify-content-center' style={{ minHeight: 'calc(100vh - 45px)', backgroundColor: '#F8F3EA' }}>
        <Container className='m-3'>
          <Row className='p-10 m-10 d-flex align-items-center justify-content-center'>
            <Col md={4} className='d-flex flex-column justify-content-center align-items-center' style={{ backgroundColor: '#F8F3EA' }}>
              <Image style={{ maxWidth: '90%', borderRadius: '10px' }} src={imageSrc || "https://via.placeholder.com/300"} fluid className='img-fluid p-auto m-auto' />
              <Form>
                <Form.Group controlId="input1">
                  <Form.Control className='m-2 p-2' type="text" placeholder="MLO/CC" style={{ maxWidth: '90%' }} onChange={(e) => setViewPos(e.target.value)} />
                  <Form.Control className='m-2 p-2' type="text" placeholder="Paddle" style={{ maxWidth: '90%' }} onChange={(e) => setPaddle(e.target.value)} />
                </Form.Group>
              </Form>
              <Col md={12}>
                <FileUploader viewPos={viewPos} paddle={paddle} onResponseReceived={handleImageReceived} returnPng={handlePng} />
              </Col>
            </Col>
            <Col md={2} className='d-flex flex-column justify-content-center align-items-center position-relative' style={{ backgroundColor: '#F8F3EA' }}>
              <div className="d-flex justify-content-center align-items-center position-relative magnifieranimation"></div>
            </Col>
            <Col md={4} className='d-flex flex-column justify-content-center align-items-center' style={{ backgroundColor: '#F8F3EA' }}>
              <Image style={{ maxWidth: '90%', borderRadius: '10px' }} src="https://via.placeholder.com/300" fluid className='img-fluid p-auto m-auto' />
              <label className='m-2 p-2' style={{ maxWidth: '90%' }}>pathology</label>
              <Col md={12}>
                <HuggingfaceUploader img={preprocess_img} />
              </Col>
            </Col>
          </Row>
          {/* <div className="separator"></div> */}
        </Container>
      </div>
    </>
  );
};

export default DefaultLayout;
