import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import FormTemplate from "../pages/FormTemplate";
import axiosInstance from "../axiosInstance";

function EditArticlePage() {
  const location = useLocation();
  const navigate = useNavigate();

  const { article } = location.state as { article: Article };

  const [updatedArticle, setUpdatedArticle] = useState<Article>(article);
  const [pageRange, setPageRange] = useState<string>(
    article.pageRange ? article.pageRange.join("-") : ""
  );
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const pageRangeRegex = /^\d+-\d+$/;
    if (!pageRangeRegex.test(pageRange)) {
      setError('Page Range should be in the format "start-end", e.g., "1-5".');
      return;
    }

    const pageRangeArray = pageRange.split("-").map(Number);

    const updatedData = {
      id: updatedArticle.id,
      title: updatedArticle.title,
      author: updatedArticle.author,
      page_range: pageRangeArray,
      content: updatedArticle.content,
    };

    console.log("Payload being sent to backend:", updatedData);

    try {
      const res = await axiosInstance.put(`/updateArticle`, updatedData);

      if (res.status === 200) {
        setSuccessMessage("Article updated successfully!");
        setTimeout(() => {
          navigate(`/`);
        }, 600);
      } else {
        setError("Error updating the article.");
      }
    } catch (err) {
      console.error("Error updating the article:", err);
      setError("Error updating the article.");
    }
  };

  return (
    <FormTemplate
      title="Edit Article"
      onSubmit={handleSubmit}
      button={
        <button type="submit" className="btn btn-primary mt-3">
          Save Changes
        </button>
      }
    >
      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && (
        <div className="alert alert-success">{successMessage}</div>
      )}
      <div className="row">
        <div className="col-md-8">
          <div className="mb-3">
            <label className="form-label">Title</label>
            <input
              type="text"
              className="form-control"
              value={updatedArticle.title}
              onChange={(e) =>
                setUpdatedArticle({ ...updatedArticle, title: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Author</label>
            <input
              type="text"
              className="form-control"
              value={updatedArticle.author}
              onChange={(e) =>
                setUpdatedArticle({ ...updatedArticle, author: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Page Range (e.g. "1-5")</label>
            <input
              type="text"
              className="form-control"
              value={pageRange}
              onChange={(e) => setPageRange(e.target.value)}
              placeholder="e.g. 1-5"
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Content</label>
            <textarea
              className="form-control"
              value={updatedArticle.content}
              onChange={(e) =>
                setUpdatedArticle({
                  ...updatedArticle,
                  content: e.target.value,
                })
              }
              rows={5}
            ></textarea>
          </div>
        </div>

        <div className="col-md-4">
          {updatedArticle.pageScans && updatedArticle.pageScans.length > 0 ? (
            <div className="mb-3">
              <label className="form-label">Image</label>
              <img
                src={`data:image/jpeg;base64,${updatedArticle.pageScans[0].imageData}`}
                alt="Article Image"
                className="img-fluid"
                style={{
                  width: "100%",
                  height: "auto",
                  borderRadius: "5px",
                  maxHeight: "500px",
                }}
              />
            </div>
          ) : (
            <p>No image available for this article.</p>
          )}
        </div>
      </div>
    </FormTemplate>
  );
}

export default EditArticlePage;
