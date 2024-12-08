import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";
import { getMagazineFromId } from "../webApi";

function EditMagazinePage() {
  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);
  const id = queryParams.get("magazine_id");
  const navigate = useNavigate();

  const [magazine, setMagazine] = useState<Magazine | null>(null);
  const [genresString, setGenresString] = useState<string>("");
  const [categoriesString, setCategoriesString] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      getMagazineFromId(id).then((res: Magazine) => {
        setMagazine(res);
        setGenresString(res.genres.join(", "));
        setCategoriesString(res.categories.join(", "));
      });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!id) {
      setError("Magazine ID is missing.");
      return;
    }

    if (!magazine) {
      setError("Magazine data is missing.");
      return;
    }

    const updatedMagazine = {
      ...magazine,
      genres: genresString
        .split(",")
        .map((g) => g.trim())
        .filter((g) => g),
      categories: categoriesString
        .split(",")
        .map((c) => c.trim())
        .filter((c) => c),
    };

    try {
      const res = await axiosInstance.post(`/updateMagazine`, updatedMagazine);

      if (res.status === 200) {
        setSuccessMessage("Magazine updated successfully!");
        setTimeout(() => {
          navigate("/upload");
        }, 600);
      } else {
        setError("Error updating the magazine.");
      }
    } catch (err) {
      console.error("Error updating the magazine:", err);
      setError("Error updating the magazine.");
    }
  };

  if (!magazine) {
    return <div className="container mt-4">Loading...</div>;
  }

  return (
    <FormTemplate title="Edit Magazine" onSubmit={handleSubmit} button={null}>
      <div className="mb-3">
        <label className="form-label">Name</label>
        <input
          type="text"
          className="form-control"
          value={magazine.name}
          onChange={(e) => setMagazine({ ...magazine, name: e.target.value })}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Publisher</label>
        <input
          type="text"
          className="form-control"
          value={magazine.publisher}
          onChange={(e) =>
            setMagazine({ ...magazine, publisher: e.target.value })
          }
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Edition</label>
        <input
          type="text"
          className="form-control"
          value={magazine.edition || ""}
          onChange={(e) =>
            setMagazine({ ...magazine, edition: e.target.value })
          }
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Date</label>
        <input
          type="date"
          className="form-control"
          value={magazine.date.toLocaleDateString()}
          onChange={(e) =>
            setMagazine({ ...magazine, date: new Date(e.target.value) })
          }
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Genres</label>
        <input
          type="text"
          className="form-control"
          value={genresString}
          onChange={(e) => setGenresString(e.target.value)}
          placeholder="Enter genres separated by commas"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Categories</label>
        <input
          type="text"
          className="form-control"
          value={categoriesString}
          onChange={(e) => setCategoriesString(e.target.value)}
          placeholder="Enter categories separated by commas"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Abstract</label>
        <textarea
          className="form-control"
          value={magazine.abstract || ""}
          onChange={(e) =>
            setMagazine({ ...magazine, abstract: e.target.value })
          }
          rows={3}
        ></textarea>
      </div>
      <div className="d-flex align-items-center mt-3">
        <button type="submit" className="btn btn-primary">
          Save Changes
        </button>
        {error && <div className="alert alert-danger ms-3 mb-0">{error}</div>}
        {successMessage && (
          <div className="alert alert-success ms-3 mb-0">{successMessage}</div>
        )}
      </div>
    </FormTemplate>
  );
}

export default EditMagazinePage;
