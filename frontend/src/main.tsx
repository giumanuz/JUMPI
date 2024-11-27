import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.scss';
import HomePage from './HomePage';
import SearchPage from './SearchPage';
import UploadPage from './UploadPage';


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/upload" element={<UploadPage />} />
    </Routes>
    </BrowserRouter>
  </StrictMode>,
);
