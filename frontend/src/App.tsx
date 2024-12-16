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
import QueryResultPage from "./pages/QueryResultsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

import PrivateRoute from "./PrivateRoute";
import { isApiKeySet, reloadApiKey } from "./apiKeyUtils";

const protectedRoutes = [
  { path: "/search", element: <SearchPage /> },
  { path: "/upload", element: <MagazineListPage /> },
  { path: "/resultPage", element: <ResultPage /> },
  { path: "/addNewMagazine", element: <AddMagazinePage /> },
  { path: "/uploadArticle", element: <UploadArticlePage /> },
  { path: "/queryResults", element: <QueryResultPage /> },
  { path: "/editMagazine", element: <EditMagazinePage /> },
  { path: "/manageArticles", element: <ManageArticlePage /> },
  { path: "/editArticle", element: <EditArticlePage /> },
];

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
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Routes */}
          {protectedRoutes.map(({ path, element }) => (
            <Route
              key={path}
              path={path}
              element={<PrivateRoute>{element}</PrivateRoute>}
            />
          ))}
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
