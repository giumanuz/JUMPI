import { useEffect } from "react";
import axiosInstance from "./axiosInstance";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AddMagazinePage from "./pages/AddMagazinePage";
import EditArticlePage from "./pages/EditArticlePage";
import EditMagazinePage from "./pages/EditMagazinePage";
import MagazineListPage from "./pages/MagazineListPage";
import ResultPage from "./pages/ResultPage";
import SearchPage from "./pages/SearchPage";
import UploadArticlePage from "./pages/UploadArticlePage";
import ManageArticlePage from "./pages/ManageArticlePage";
import { isApiKeySet, reloadApiKey } from "./apiKeyUtils";
import QueryResultPage from "./pages/QueryResultsPage";

function App() {
  useEffect(() => {
    console.log("Checking if API key is set...");
    if (isApiKeySet()) {
        console.log("API key is set. Reloading it...");
        reloadApiKey();
        return
    }
    console.log("API key is not set.");
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/upload" element={<MagazineListPage />} />
        <Route path="/resultPage" element={<ResultPage />} />
        <Route path="/addNewMagazine" element={<AddMagazinePage />} />
        <Route path="/uploadArticle" element={<UploadArticlePage />} />
        <Route path="/queryResults" element={<QueryResultPage />} />

        <Route path="/editMagazine" element={<EditMagazinePage />} />
        <Route path="/manageArticles" element={<ManageArticlePage />} />
        <Route path="/editArticle" element={<EditArticlePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;