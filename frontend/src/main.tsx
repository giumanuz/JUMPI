import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './styles/index.scss';
import HomePage from './pages/HomePage';
import SearchPage from './pages/SearchPage';
import UploadPage from './pages/UploadPage';
import ResultPage from './pages/ResultPage';
import QueryResultsPage from "./pages/QueryResultsPage.tsx";
import EditPage from './pages/EditPage';
import UploadArticlePage from './pages/UploadArticlePage';
import AddMagazinePage from './pages/AddMagazinePage';


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
    <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/search" element={<SearchPage/>}/>
        <Route path="/upload" element={<UploadPage/>}/>
        <Route path="/resultPage" element={<ResultPage/>}/>
        <Route path="/addNewMagazine" element={<AddMagazinePage />} />
        <Route path="/uploadArticle" element={<UploadArticlePage />} />
    </Routes>
    </BrowserRouter>
  </StrictMode>,
);
