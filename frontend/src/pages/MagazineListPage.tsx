import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";
import { useNavigate } from "react-router-dom";

function MagazineListPage() {
  const [magazines, setMagazines] = useState<Magazine[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Fetching magazines...");
    axiosInstance
      .get("/getMagazines")
      .then((res) => {
        console.log("Magazines received:", res.data.magazines);
        
        const magazinesWithDates: Magazine[] = res.data.magazines.map((m: any) => ({
          ...m,
          createdOn: new Date(m.createdOn),
          editedOn: new Date(m.editedOn),
          date: new Date(m.date),
        }));
        
        setMagazines(magazinesWithDates);
      })
      .catch((err) => {
        console.error("Error fetching magazines:", err);
      });
  }, []);
  
  const toggleExpansion = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const handleMagazineClick = (magazineId: string) => {
    navigate(`/uploadArticle?magazine_id=${magazineId}`);
  };

  const handleEditClick = (magazineId: string) => {
    navigate(`/editMagazine?magazine_id=${magazineId}`);
  };

  const handleManageArticlesClick = (magazineId: string) => {
    navigate(`/manageArticles?magazine_id=${magazineId}`);
  };

  return (
    <div className="container mt-4">
      <h1>Upload Magazines</h1>
      <button
        className="btn btn-success mb-3"
        onClick={() => navigate("/addNewMagazine")}
      >
        +
      </button>

      <div className="row">
        {magazines.map((m) => (
          <div className="col-4 mb-3" key={m.id}>
            <div className="card p-3">
              <h5>{m.name}</h5>
              <p>
                <strong>Publisher:</strong> {m.publisher}
              </p>
              <p>
                <strong>Edition:</strong> {m.edition}
              </p>
              <button
                className="btn btn-link p-0"
                onClick={() => toggleExpansion(m.id)}
              >
                {expandedId === m.id ? "Hide Details" : "Show Details"}
              </button>
              {expandedId === m.id && (
                <div className="mt-2">
                  <p>
                    <strong>Abstract:</strong> {m.abstract}
                  </p>
                  <p>
                    <strong>Categories:</strong> {m.categories.join(", ")}
                  </p>
                  <p>
                    <strong>Genres:</strong> {m.genres.join(", ")}
                  </p>
                  <p>
                    <strong>Created On:</strong> {m.createdOn.toDateString()}
                  </p>
                  <p>
                    <strong>Edited On:</strong> {m.editedOn.toDateString()}
                  </p>
                  <p>
                    <strong>Date:</strong> {m.date.toDateString()}
                  </p>
                </div>
              )}
              <button
                className="btn btn-primary mt-2"
                onClick={() => handleMagazineClick(m.id)}
              >
                Upload Article
              </button>
              <button
                className="btn btn-secondary mt-2 ms-2"
                onClick={() => handleEditClick(m.id)}
              >
                Edit Magazine
              </button>
              <button
                className="btn btn-warning mt-2 ms-2"
                onClick={() => handleManageArticlesClick(m.id)}
              >
                Manage Articles
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MagazineListPage;
