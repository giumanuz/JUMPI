import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import FormTemplate from "./FormTemplate";
import axiosInstance from "../axiosInstance.ts";

const EditPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const initialData = location.state?.data ?? {};

  const [formData, setFormData] = useState(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData((prev) => ({ ...prev, image: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axiosInstance.post("/edit", {
        magazine: {
          id: formData._id,
          name: formData.name,
          year: formData.year,
          publisher: formData.publisher,
          genre: formData.genre,
        },
        article: formData.articles?.[0] ?? null,
        image: formData.image,
      });
      console.log("Server response:", response.data);
      navigate(-1);
    } catch (err: any) {
      setError(err.response?.data?.error || "An unexpected error occurred");
      console.error("Error updating data:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <FormTemplate
      title="Edit Magazine"
      onSubmit={handleSubmit}
      loading={loading}
      loadingDescription="Saving changes..."
      button={
        <button
          type="submit"
          className="btn btn-primary w-100"
          disabled={loading}
        >
          Save
        </button>
      }
    >
      {[
        <div key="name" className="mb-3">
          <label htmlFor="name" className="form-label">
            Name
          </label>
          <input
            id="name"
            className="form-control"
            value={formData.name ?? ""}
            onChange={(e) => handleChange("name", e.target.value)}
          />
        </div>,
        <div key="year" className="mb-3">
          <label htmlFor="year" className="form-label">
            Year
          </label>
          <input
            id="year"
            type="number"
            className="form-control"
            value={formData.year ?? ""}
            onChange={(e) => handleChange("year", e.target.value)}
          />
        </div>,
        <div key="publisher" className="mb-3">
          <label htmlFor="publisher" className="form-label">
            Publisher
          </label>
          <input
            id="publisher"
            className="form-control"
            value={formData.publisher ?? ""}
            onChange={(e) => handleChange("publisher", e.target.value)}
          />
        </div>,
        <div key="genre" className="mb-3">
          <label htmlFor="genre" className="form-label">
            Genre
          </label>
          <input
            id="genre"
            className="form-control"
            value={formData.genre ?? ""}
            onChange={(e) => handleChange("genre", e.target.value)}
          />
        </div>,
        <div key="articleTitle" className="mb-3">
          <label htmlFor="articleTitle" className="form-label">
            First Article Title
          </label>
          <input
            id="articleTitle"
            className="form-control"
            value={formData.articles?.[0]?.title ?? ""}
            onChange={(e) =>
              handleChange("articles", [
                { ...formData.articles?.[0], title: e.target.value },
              ])
            }
          />
        </div>,
        <div key="image" className="mb-3">
          <label htmlFor="image" className="form-label">
            Image
          </label>
          <div className="mb-2">
            <img
              src={formData.image || "https://via.placeholder.com/150"}
              alt="Magazine"
              className="img-fluid rounded"
              style={{ maxHeight: "150px" }}
            />
          </div>
          <input
            id="image"
            type="file"
            className="form-control"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>,
      ]}
      {error && <div className="alert alert-danger mt-3">{error}</div>}
    </FormTemplate>
  );
};

export default EditPage;
