import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";

interface Magazine {
  id: string;
  name: string;
  date: string;
  publisher: string;
  edition?: string;
  abstract?: string;
  genres: string[];
  categories: string[];
}

function EditMagazinePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [magazine, setMagazine] = useState<Magazine | null>(null);
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [publisher, setPublisher] = useState("");
  const [edition, setEdition] = useState("");
  const [abstract, setAbstract] = useState("");
  const [genres, setGenres] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      axiosInstance
        .get(`/magazines/${id}`)
        .then((res) => {
          setMagazine(res.data.magazine);
          setName(res.data.magazine.name);
          setDate(res.data.magazine.date.split("T")[0]);
          setPublisher(res.data.magazine.publisher);
          setEdition(res.data.magazine.edition || "");
          setAbstract(res.data.magazine.abstract || "");
          setGenres(res.data.magazine.genres);
          setCategories(res.data.magazine.categories);
        })
        .catch((err) => {
          console.error("Error retrieving the magazine:", err);
          setError("Error retrieving the magazine.");
        });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!id) {
      setError("Magazine ID is missing.");
      return;
    }

    const updatedMagazine = {
      name,
      date,
      publisher,
      edition: edition || null,
      abstract: abstract || null,
      genres,
      categories,
    };

    try {
      const res = await axiosInstance.put(`/magazines/${id}`, updatedMagazine);

      if (res.status === 200) {
        setSuccessMessage("Magazine updated successfully!");
        setTimeout(() => {
          navigate("/manageMagazines");
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
    <FormTemplate
      title="Edit Magazine"
      onSubmit={handleSubmit}
      button={null}
    >
      <div className="mb-3">
        <label className="form-label">Name</label>
        <input
          type="text"
          className="form-control"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Publisher</label>
        <input
          type="text"
          className="form-control"
          value={publisher}
          onChange={(e) => setPublisher(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Edition</label>
        <input
          type="text"
          className="form-control"
          value={edition}
          onChange={(e) => setEdition(e.target.value)}
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Date</label>
        <input
          type="date"
          className="form-control"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Genres</label>
        <input
          type="text"
          className="form-control"
          value={genres.join(", ")}
          onChange={(e) =>
            setGenres(
              e.target.value
                .split(",")
                .map((g) => g.trim())
                .filter((g) => g)
            )
          }
          placeholder="Enter genres separated by commas"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Categories</label>
        <input
          type="text"
          className="form-control"
          value={categories.join(", ")}
          onChange={(e) =>
            setCategories(
              e.target.value
                .split(",")
                .map((c) => c.trim())
                .filter((c) => c)
            )
          }
          placeholder="Enter categories separated by commas"
        />
      </div>
      <div className="mb-3">
        <label className="form-label">Abstract</label>
        <textarea
          className="form-control"
          value={abstract}
          onChange={(e) => setAbstract(e.target.value)}
          rows={3}
        ></textarea>
      </div>
      <div className="mb-3">
        {/* Empty div for padding */}
      </div>
      <div className="d-flex align-items-center mt-3">
        <button type="submit" className="btn btn-primary">
          Save Changes
        </button>
        {error && <div className="alert alert-danger ms-3 mb-0">{error}</div>}
        {successMessage && (
          <div className="alert alert-success ms-3 mb-0">
            {successMessage}
          </div>
        )}
      </div>
    </FormTemplate>
  );
}

export default EditMagazinePage;
