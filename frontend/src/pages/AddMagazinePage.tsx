import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";
import InputField from "../components/InputField";
import TextAreaField from "../components/TextAreaField";

function splitStrings(input: string): string[] {
  return input
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item !== "");
}

function AddMagazinePage() {
  const [newMagazine, setNewMagazine] = useState<Partial<Magazine>>({});
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState<boolean>(false);
  const [categoriesString, setCategoriesString] = useState<string>("");
  const [genresString, setGenresString] = useState<string>("");
  const navigate = useNavigate();

  const handleNewMagazineSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    setLoading(true);
    setError(undefined);
    try {
      newMagazine.categories = splitStrings(categoriesString);
      newMagazine.genres = splitStrings(genresString);
      console.log("Adding new magazine:", newMagazine);
      const { data } = await axiosInstance.post("/uploadMagazine", newMagazine);
      const { id } = data as { id: string };
      navigate(`/uploadArticle?magazine_id=${id}`);
    } catch (err: any) {
      console.error("Error adding new magazine:", err);
      const errorMessage =
        err.response?.data?.error ??
        "Failed to add the magazine. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const SaveButton = () => (
    <button type="submit" className="btn btn-primary">
      Save
    </button>
  );

  const CancelButton = () => (
    <button
      type="button"
      className="btn btn-secondary ms-2"
      onClick={() => navigate(-1)}
    >
      Cancel
    </button>
  );

  return (
    <FormTemplate
      title="Add New Magazine"
      onSubmit={handleNewMagazineSubmit}
      loading={loading}
      loadingDescription="Saving the magazine. Please wait..."
      preFormContent={
        error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )
      }
      button={
        <>
          <SaveButton />
          <CancelButton />
        </>
      }
    >
      <InputField
        id="name"
        label="Name"
        placeholder="Enter the name of the magazine"
        value={newMagazine.name ?? ""}
        required
        onChange={(e) =>
          setNewMagazine({ ...newMagazine, name: e.target.value })
        }
      />
      <InputField
        id="publisher"
        label="Publisher"
        placeholder="Enter the name of the publisher"
        value={newMagazine.publisher ?? ""}
        required
        onChange={(e) =>
          setNewMagazine({ ...newMagazine, publisher: e.target.value })
        }
      />
      <InputField
        id="edition"
        label="Edition"
        placeholder="Enter the edition of the magazine"
        value={newMagazine.edition ?? ""}
        onChange={(e) =>
          setNewMagazine({ ...newMagazine, edition: e.target.value })
        }
      />
      <InputField
        id="categories"
        label="Categories (separated by commas)"
        placeholder="Enter the categories of the magazine"
        value={categoriesString}
        required
        onChange={(e) => setCategoriesString(e.target.value)}
      />
      <InputField
        id="genres"
        label="Genres (separated by commas)"
        placeholder="Enter the genres of the magazine"
        value={genresString}
        required
        onChange={(e) => setGenresString(e.target.value)}
      />
      <InputField
        id="date"
        label="Date"
        placeholder="Enter the date of the magazine"
        value={newMagazine.date?.toISOString().split("T")[0] ?? ""}
        required
        onChange={(e) =>
          setNewMagazine({
            ...newMagazine,
            date: new Date(e.target.value),
          })
        }
        type="date"
      />
      <TextAreaField
        id="abstract"
        label="Abstract"
        placeholder="Enter the abstract of the magazine"
        value={newMagazine.abstract ?? ""}
        required
        onChange={(e) =>
          setNewMagazine({ ...newMagazine, abstract: e.target.value })
        }
      />
    </FormTemplate>
  );
}

export default AddMagazinePage;
