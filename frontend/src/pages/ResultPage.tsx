import { useLocation } from 'react-router-dom';
import '../styles/ResultPage.scss';
const ResultPage = () => {
  const location = useLocation();
  const { extracted_text, image_comparison } = location.state;

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: '50rem' }}>
        <h3 className="text-center mb-4">Document Analysis Results</h3>

        <div className="mb-4">
          <h5>Extracted Text:</h5>
          <div className="text-container">
            <pre>{extracted_text}</pre>
          </div>
        </div>

        <div className="mb-4">
          <h5>Image Comparison:</h5>
          <div className="image-container">
            <img
              src={`data:image/jpeg;base64,${image_comparison}`}
              alt="Image comparison"
              className="img-fluid"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
