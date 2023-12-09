import React from 'react';
import { Routes, BrowserRouter, Route } from 'react-router-dom';

import DefaultLayout from './layouts/default_test';


const Router_test = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<DefaultLayout />}>
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default Router_test;