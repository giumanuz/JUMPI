import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosInstance from "../axiosInstance";
import FormTemplate from "../pages/FormTemplate";

interface Article {
  id: string;
  magazine_id: string;
  title: string;
  author: string;
  page_range: number[];
  content: string;
  page_offsets: number[];
  figures: any[]; // Define it properly as needed
  created_on: string;
  edited_on: string;
  page_scans?: { page: number; imageData: string; uploadedOn: string }[]; // Assuming the image is in this format
}

function EditArticlePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [article, setArticle] = useState<Article | null>(null);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [pageRange, setPageRange] = useState("");
  const [content, setContent] = useState("");
  const [imageData, setImageData] = useState<string | null>(null); // State for the image
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      axiosInstance
        .get(`/articles/${id}`)
        .then((res) => {
          const articleData = res.data.article;
          setArticle(articleData);
          setTitle(articleData.title);
          setAuthor(articleData.author);
          setPageRange(articleData.page_range.join("-"));
          setContent(articleData.content);
          
          if (articleData.page_scans && articleData.page_scans.length > 0) {
            setImageData(articleData.page_scans[0].imageData);
          }
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

    const updatedArticle = {
      title,
      author,
      page_range: pageRange.split("-").map(Number),
      content,
      // Include other fields as needed
    };

    try {
      const res = await axiosInstance.put(`/articles/${id}`, updatedArticle);

      if (res.status === 200) {
        setSuccessMessage("Article updated successfully!");
        setTimeout(() => {
          navigate(`/manageArticles/${article?.magazine_id}`);
        }, 2000);
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
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
    </div>
    <div className="mb-3">
      <label className="form-label">Author</label>
      <input
        type="text"
        className="form-control"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
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
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={5}
      ></textarea>
    </div>
  </div>

    <div className="col-md-4">
        {imageData ? (
            <div className="mb-3">
                <label className="form-label">Image</label>
                <img
                    src={`data:image/jpeg;base64,${imageData}`}
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
