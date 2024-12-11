import { useEffect } from "react";
import { AuthProvider } from "./authContext";
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
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

import PrivateRoute from "./PrivateRoute";

function App() {
  useEffect(() => {
    console.log("Checking if API key is set...");
    if (isApiKeySet()) {
      console.log("API key is set. Reloading it...");
      reloadApiKey();
      return;
    }
    console.log("API key is not set.");
  }, []);

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Rotte protette */}
          <Route
            path="/search"
            element={
              <PrivateRoute>
                <SearchPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/upload"
            element={
              <PrivateRoute>
                <MagazineListPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/resultPage"
            element={
              <PrivateRoute>
                <ResultPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/addNewMagazine"
            element={
              <PrivateRoute>
                <AddMagazinePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/uploadArticle"
            element={
              <PrivateRoute>
                <UploadArticlePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/queryResults"
            element={
              <PrivateRoute>
                <QueryResultPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/editMagazine"
            element={
              <PrivateRoute>
                <EditMagazinePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/manageArticles"
            element={
              <PrivateRoute>
                <ManageArticlePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/editArticle"
            element={
              <PrivateRoute>
                <EditArticlePage />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
