import React, { useState } from "react";
import axiosInstance from "../axiosInstance";
import { useNavigate } from "react-router-dom";
import FormTemplate from "../pages/FormTemplate";

type Magazine = {
  id: string;
  name: string;
  publisher: string;
  edition: string;
  categories: string[];
  genres: string[];
  abstract: string;
  created_on: string;
  edited_on: string;
  date: string;
};

function AddMagazinePage() {
  const [newMagazineData, setNewMagazineData] = useState<Partial<Magazine>>({});
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleNewMagazineSubmit = async (
    e: React.FormEvent<HTMLFormElement>,
  ) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await axiosInstance.post("/addNewMagazine", newMagazineData);
      const newMagazine = res.data.magazine;
      navigate(`/uploadArticle?magazine_id=${newMagazine.id}`);
    } catch (err: any) {
      console.error("Error adding new magazine:", err);
      const errorMessage =
        err.response?.data?.error ||
        "Failed to add the magazine. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormTemplate
      title="Add New Magazine"
      onSubmit={handleNewMagazineSubmit}
      button={
        <>
          <button type="submit" className="btn btn-primary">
            Save
          </button>
          <button
            type="button"
            className="btn btn-secondary ms-2"
            onClick={() => navigate(-1)}
          >
            Cancel
          </button>
        </>
      }
      loading={loading}
      loadingDescription="Saving the magazine. Please wait..."
      preFormContent={
        error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )
      }
    >
      <div>
        <label className="form-label">Name</label>
        <input
          type="text"
          className="form-control"
          value={newMagazineData.name || ""}
          onChange={(e) =>
            setNewMagazineData({ ...newMagazineData, name: e.target.value })
          }
          required
        />
      </div>
      <div>
        <label className="form-label">Publisher</label>
        <input
          type="text"
          className="form-control"
          value={newMagazineData.publisher || ""}
          onChange={(e) =>
            setNewMagazineData({
              ...newMagazineData,
              publisher: e.target.value,
            })
          }
          required
        />
      </div>
      <div>
        <label className="form-label">Edition</label>
        <input
          type="text"
          className="form-control"
          value={newMagazineData.edition || ""}
          onChange={(e) =>
            setNewMagazineData({ ...newMagazineData, edition: e.target.value })
          }
          required
        />
      </div>
      <div>
        <label className="form-label">Categories (separated by commas)</label>
        <input
          type="text"
          className="form-control"
          value={newMagazineData.categories?.join(", ") || ""}
          onChange={(e) =>
            setNewMagazineData({
              ...newMagazineData,
              categories: e.target.value
                .split(",")
                .map((cat) => cat.trim())
                .filter((cat) => cat !== ""),
            })
          }
        />
      </div>
      <div>
        <label className="form-label">Genres (separated by commas)</label>
        <input
          type="text"
          className="form-control"
          value={newMagazineData.genres?.join(", ") || ""}
          onChange={(e) =>
            setNewMagazineData({
              ...newMagazineData,
              genres: e.target.value
                .split(",")
                .map((genre) => genre.trim())
                .filter((genre) => genre !== ""),
            })
          }
        />
      </div>
      <div>
        <label className="form-label">Date</label>
        <input
          type="date"
          className="form-control"
          value={newMagazineData.date ? newMagazineData.date.split("T")[0] : ""}
          onChange={(e) =>
            setNewMagazineData({
              ...newMagazineData,
              date: new Date(e.target.value).toISOString(),
            })
          }
          required
        />
      </div>
      <div>
        <label className="form-label">Abstract</label>
        <textarea
          className="form-control"
          value={newMagazineData.abstract || ""}
          onChange={(e) =>
            setNewMagazineData({ ...newMagazineData, abstract: e.target.value })
          }
          required
        />
      </div>
    </FormTemplate>
  );
}

export default AddMagazinePage;
