import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";
import { useNavigate } from "react-router-dom";

interface Magazine {
  id: string;
  name: string;
  publisher: string;
  edition?: string;
  abstract?: string;
  genres: string[];
  categories: string[];
  created_on: string;
  edited_on: string;
  date: string;
}

function ManageMagazinePage() {
  const [magazines, setMagazines] = useState<Magazine[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    axiosInstance
      .get("/getMagazines")
      .then((res) => {
        setMagazines(res.data.magazines);
      })
      .catch((err) => {
        console.error("Error retrieving magazines:", err);
        setError("Error retrieving magazines.");
      });
  }, []);

  const handleEditMagazine = (magazineId: string) => {
    navigate(`/editMagazine/${magazineId}`);
  };

  const handleManageArticles = (magazineId: string) => {
    navigate(`/manageArticles/${magazineId}`);
  };

  return (
    <div className="container mt-4">
      <h1>Manage Magazines</h1>
      {error && <div className="alert alert-danger">{error}</div>}
      <button
        className="btn btn-success mb-3"
        onClick={() => navigate("/addNewMagazine")}
      >
        + Add New Magazine
      </button>
      <div className="row">
        {magazines.map((mag) => (
          <div className="col-4 mb-3" key={mag.id}>
            <div className="card p-3 h-100 d-flex flex-column">
              <h5>{mag.name}</h5>
              <p>
                <strong>Publisher:</strong> {mag.publisher}
              </p>
              <p>
                <strong>Edition:</strong> {mag.edition || "N/A"}
              </p>
              <div className="mt-auto d-flex gap-2">
                <button
                  className="btn btn-primary"
                  onClick={() => handleEditMagazine(mag.id)}
                >
                  Edit Magazine
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={() => handleManageArticles(mag.id)}
                >
                  Manage Articles
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ManageMagazinePage;
