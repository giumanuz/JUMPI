import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";


function EditArticlePage() {
  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);
  const id = queryParams.get("magazine_id");
  const navigate = useNavigate();

  const [article, setArticle] = useState<Article | null>(null);
  const [pageRange, setPageRange] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      axiosInstance
        .get(`/articleInfo?id=${id}`)
        .then((res) => {
          setArticle(res.data);
          setPageRange(res.data.page_range.join("-"));
        })
        .catch((err) => {
          console.error("Error retrieving article:", err);
          setError("Error retrieving the article.");
        });
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!id) {
      setError("Article ID is missing.");
      return;
    }

    const pageRangeRegex = /^\d+-\d+$/;
    if (!pageRangeRegex.test(pageRange)) {
      setError('Page Range should be in the format "start-end", e.g., "1-5".');
      return;
    }

    const pageRangeArray = pageRange.split("-").map(Number);

    const updatedArticle = {
      ...article,
      page_range: pageRangeArray,
    };

    try {
      const res = await axiosInstance.put(`/updateArticle`, updatedArticle);

      if (res.status === 200) {
        setSuccessMessage("Article updated successfully!");
        setTimeout(() => {
          navigate(`/manageArticles/${article?.magazineId}`);
        }, 600);
      } else {
        setError("Error updating the article.");
      }
    } catch (err) {
      console.error("Error updating the article:", err);
      setError("Error updating the article.");
    }
  };

  if (!article) {
    return <div className="container mt-4">Loading...</div>;
  }

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
              value={article.title}
              onChange={(e) =>
                setArticle({ ...article, title: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Author</label>
            <input
              type="text"
              className="form-control"
              value={article.author}
              onChange={(e) =>
                setArticle({ ...article, author: e.target.value })
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
              value={article.content}
              onChange={(e) =>
                setArticle({ ...article, content: e.target.value })
              }
              rows={5}
            ></textarea>
          </div>
        </div>

        <div className="col-md-4">
          {article.pageScans && article.pageScans.length > 0 ? (
            <div className="mb-3">
              <label className="form-label">Image</label>
              <img
                src={`data:image/jpeg;base64,${article.pageScans[0].imageData}`}
                alt="Article Image"
                className="img-fluid" 
                style={{
                  width: '100%',  
                  height: 'auto',
                  borderRadius: '5px',
                  maxHeight: '500px',
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
