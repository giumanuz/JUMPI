import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import FormTemplate from "../pages/FormTemplate";
import InputField from "../components/InputField";
import {
  uploadArticleAndGetResults,
  UploadArticleRequiredKeys,
} from "../webApi";

function UploadArticlePage() {
  const [searchParams] = useSearchParams();
  const magazineId = searchParams.get("magazine_id");
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [pageRange, setPageRange] = useState("");
  const [scans, setScans] = useState<FileList>();
  const [error, setError] = useState<string>();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setScans(e.target.files);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!magazineId) {
      setError("Magazine ID is missing.");
      return;
    }

    if (!scans || scans.length === 0) {
      setError("Please upload at least one image.");
      return;
    }

    let pageRangeInts: number[];
    try {
      pageRangeInts = pageRange.split("-").map(Number);
    } catch {
      setError('Page Range should be in the format "start-end", e.g., "1-5".');
      return;
    }

    const article: Pick<Article, UploadArticleRequiredKeys> = {
      title,
      author,
      pageRange: pageRangeInts,
      magazineId: magazineId as string,
    };

    try {
      const result = await uploadArticleAndGetResults(article, scans);

      navigate("/resultPage", {
        state: { scanResults: result.scanResults },
      });
    } catch (err) {
      console.error(err);
      setError("Failed to upload the article. Please try again.");
    }
  };

  return (
    <FormTemplate
      title="Upload Article"
      onSubmit={handleSubmit}
      button={
        <button type="submit" className="btn btn-primary mt-3">
          Submit
        </button>
      }
    >
      {error && <div className="alert alert-danger">{error}</div>}
      <InputField
        label="Title"
        value={title}
        placeholder="Casabella Continuità"
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <InputField
        label="Author"
        value={author}
        placeholder="John Doe"
        onChange={(e) => setAuthor(e.target.value)}
        required
      />
      <InputField
        label="Page Range"
        value={pageRange}
        placeholder="1-5"
        onChange={(e) => setPageRange(e.target.value)}
        required
      />
      <div className="mb-3">
        <label className="form-label">Upload Images</label>
        <input
          type="file"
          className="form-control"
          multiple
          accept="image/*"
          onChange={handleImageChange}
        />
      </div>
    </FormTemplate>
  );
}

export default UploadArticlePage;
