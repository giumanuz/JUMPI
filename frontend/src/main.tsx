import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./styles/index.scss";
import HomePage from "./pages/HomePage";
import SearchPage from "./pages/SearchPage";
import MagazineListPage from "./pages/MagazineListPage";
import ResultPage from "./pages/ResultPage";
import UploadArticlePage from "./pages/UploadArticlePage";
import AddMagazinePage from "./pages/AddMagazinePage";
import EditMagazinePage from "./pages/EditMagazinePage";
import EditArticlePage from "./pages/EditArticlePage";
import ManageMagazinesPage from "./pages/ManageMagazinePage";
import ManageArticlesPage from "./pages/ManageArticlePage";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/upload" element={<MagazineListPage />} />
        <Route path="/resultPage" element={<ResultPage />} />
        <Route path="/addNewMagazine" element={<AddMagazinePage />} />
        <Route path="/uploadArticle" element={<UploadArticlePage />} />
        
        <Route path="/manageMagazines" element={<ManageMagazinesPage />} />
        <Route path="/manageArticles/:magazineId" element={<ManageArticlesPage />} />
        <Route path="/editMagazine/:id" element={<EditMagazinePage />} />
        <Route path="/editArticle/:id" element={<EditArticlePage />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
