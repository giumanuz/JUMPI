import { useEffect, useState } from "react";
import axiosInstance from "../axiosInstance";
import { useNavigate } from "react-router-dom";
import { getMagazines } from "../webApi";
import MagazineCard from "../components/MagazineCard";

function MagazineListPage() {
  const [magazines, setMagazines] = useState<Magazine[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    getMagazines().then(setMagazines);
  }, []);

  const toggleExpansion = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const onMagazineUploadArticle = (magazineId: string) => {
    navigate(`/uploadArticle?magazine_id=${magazineId}`);
  };

  const onMagazineEdit = (magazineId: string) => {
    navigate(`/editMagazine?magazine_id=${magazineId}`);
  };

  const onMagazineManageArticles = (magazineId: string) => {
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
        {magazines.map((m, i) => (
          <MagazineCard
            key={i}
            expanded={expandedId === m.id}
            toggleExpansion={() => toggleExpansion(m.id)}
            magazine={m}
            onEdit={() => onMagazineEdit(m.id)}
            onManageArticles={() => onMagazineManageArticles(m.id)}
            onUploadArticle={() => onMagazineUploadArticle(m.id)}
          />
        ))}
      </div>
    </div>
  );
}

export default MagazineListPage;
