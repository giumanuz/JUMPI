// src/pages/ResultPage.tsx

import { useLocation, useNavigate } from "react-router-dom";
import "../styles/ResultPage.scss";

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Type guard to ensure state exists
  const { scanResults } = location.state as { scanResults: ScanResult[] };

  if (!scanResults) {
    // If state is undefined, redirect back or show an error
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
          <h5>Extracted Text:</h5>
          {scanResults.map(({ text }, index) => (
            <div className="text-container" key={index}>
              <pre>{text}</pre>
            </div>
          ))}
        </div>

        <div className="mb-4">
          <h5>Image Comparisons:</h5>
          <div className="image-container d-flex flex-wrap gap-3">
            {scanResults?.map(({ comparisonImage }, index: number) => (
              <img
                key={index}
                src={`data:image/jpeg;base64,${comparisonImage}`}
                alt={`Image comparison ${index + 1}`}
                className="img-fluid"
                style={{
                  maxWidth: "100%",
                  maxHeight: "300px",
                  objectFit: "contain",
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
