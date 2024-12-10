import { useLocation, useNavigate } from "react-router-dom";
import "../styles/ResultPage.scss";

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { result } = location.state as { result: ArticleResultPage };
  const { articleId, scanResults, text } = result;

  if (!scanResults || !text) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="card bg-body-secondary p-4 shadow-sm text-center">
          <h3 className="mb-4">No Data Available</h3>
          <p>
            It seems you navigated to this page without submitting an article.
          </p>
          <button
            className="btn btn-primary mt-3"
            onClick={() => navigate("/")}
          >
            Go Back to Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div
        className="card bg-body-secondary p-4 shadow-sm"
        style={{ width: "50rem" }}
      >
        <h3 className="text-center mb-4">Document Analysis Results</h3>

        <div className="mb-4">
          <h5>Article ID:</h5>
          <p>{articleId}</p>
        </div>

        <div className="mb-4">
          <h5>Extracted Text:</h5>
          <textarea className="form-control">{text}</textarea>
        </div>

        <div className="mb-4">
          <h5>Image Comparisons:</h5>
          <div className="image-container d-flex flex-wrap gap-3 bg-danger">
            {scanResults.map(({ comparisonImage, page }, index) => (
              <div key={index} className="text-center w-100 vh-100">
                <img
                  src={`data:image/jpeg;base64,${comparisonImage}`}
                  alt={`Comparison for page ${page}`}
                  className="img-fluid mb-2 w-100 h-auto"
                />
                <p>Page {page}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
