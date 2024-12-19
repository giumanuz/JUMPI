import { useLocation, useNavigate } from "react-router-dom";
import "../styles/ResultPage.scss";
import { useState } from "react";

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { result } = location.state as { result: ArticleResultPage };
  const { articleId, scanResults, text, figures } = result;

  const [editableText, setEditableText] = useState(text);
  const [editableFigures, setEditableFigures] = useState(
    figures || []
  );

  const [editableScanResults] = useState(scanResults);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  if (!scanResults || !text) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="card bg-body-secondary p-4 shadow-sm text-center">
          <h3 className="mb-4">No Data Available</h3>
          <p>
            It seems you navigated to this page without submitting an article.
          </p>
          <button className="btn btn-primary mt-3" onClick={() => navigate("/")}>
            Go Back to Upload
          </button>
        </div>
      </div>
    );
  }

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(false);

    const payload = {
      articleId: articleId,
      text: editableText,
      figures: editableFigures,
    };

    try {
      const response = await fetch("/editedArticle", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Errore nella richiesta: ${response.statusText}`);
      }

      setSubmitSuccess(true);
    } catch (error: any) {
      setSubmitError(error.message || "Errore sconosciuto");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container vh-100 d-flex justify-content-center align-items-center">
      <div className="card bg-body-secondary p-4 shadow-sm w-100" style={{ maxWidth: "1200px" }}>
        <h3 className="text-center mb-4">Document Analysis Results</h3>
        <div className="d-flex flex-row">
          {/* Colonna Sinistra: Contenuti Testuali */}
          <div className="flex-grow-1 me-4">
            <div className="mb-4">
              <h5>Article ID:</h5>
              <input
                type="text"
                className="form-control"
                value={articleId}
              />
            </div>

            <div className="mb-4">
              <h5>Extracted Text:</h5>
              <textarea
                className="form-control"
                rows={10}
                value={editableText}
                onChange={(e) => setEditableText(e.target.value)}
              ></textarea>
            </div>

            {/* Sezione Figure e Didascalie */}
            {editableFigures && editableFigures.length > 0 && (
              <div className="mb-4">
                <h5>Figures:</h5>
                {editableFigures.map((figure, index) => (
                  <div key={index} className="mb-3">
                    <img
                      src={`data:image/jpeg;base64,${figure.imageData}`}
                      alt={`Figure ${index + 1}`}
                      className="img-fluid mb-2"
                    />
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Figure caption"
                      value={figure.caption || ""}
                      onChange={(e) => {
                        const newFigures = [...editableFigures];
                        newFigures[index].caption = e.target.value;
                        setEditableFigures(newFigures);
                      }}
                    />
                  </div>
                ))}
              </div>
            )}

            {/* Pulsante di Invio */}
            <div className="mb-4">
              <button
                className="btn btn-success"
                onClick={handleSubmit}
                disabled={isSubmitting}
              >
                {isSubmitting ? "Submitting..." : "Submit Edits"}
              </button>
              {submitError && (
                <div className="alert alert-danger mt-2" role="alert">
                  {submitError}
                </div>
              )}
              {submitSuccess && (
                <div className="alert alert-success mt-2" role="alert">
                  Edits submitted successfully!
                </div>
              )}
            </div>
          </div>

          {/* Colonna Destra: Immagini */}
          <div className="flex-shrink-0" style={{ width: "600px", overflowY: "auto" }}>
            <h5>Image Comparisons:</h5>
            <div className="d-flex flex-column gap-4">
              {editableScanResults.map(({ comparisonImage, page }, index) => (
                <div key={index} className="text-center">
                  <img
                    src={`data:image/jpeg;base64,${comparisonImage}`}
                    alt={`Comparison for page ${page}`}
                    className="img-fluid border border-white"
                    style={{ maxHeight: "500px", objectFit: "cover" }}
                  />
                  <p>Page {page}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
