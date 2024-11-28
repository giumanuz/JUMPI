import { ChangeEvent, FormEvent, useState } from 'react';
import InputField from '../components/InputField';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const UploadPage = () => {
  const [formData, setFormData] = useState({
    name_magazine: '',
    year: '',
    publisher: '',
    genre: '',
    article_title: '',
    article_author: '',
    article_page_range: '',
    document: null as File | null,
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { id, value, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.document) {
      alert('Please upload a document.');
      return;
    }

    setLoading(true); // Start loading

    try {
      const metadata = JSON.stringify({
        name_magazine: formData.name_magazine,
        year: formData.year,
        publisher: formData.publisher,
        genre: formData.genre,
        article_title: formData.article_title,
        article_author: formData.article_author,
        article_page_range: formData.article_page_range,
      });

      const uploadData = new FormData();
      uploadData.append('metadata', metadata);
      uploadData.append('files', formData.document);

      const response = await axios.post('http://localhost:5123/analyze-documents', uploadData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Navigate to the result page with the data from the response
      navigate('/result', { state: response.data });
      
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Failed to analyze document. Please try again.');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card bg-body-secondary p-4 shadow-sm" style={{ width: '50rem' }}>
        <h3 className="text-center mb-4">Upload a New Article</h3>
        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-6">
              <InputField
                id="name_magazine"
                label="Magazine Name"
                placeholder="Enter magazine name"
                value={formData.name_magazine}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6">
              <InputField
                id="year"
                label="Year"
                placeholder="Enter year of publication"
                value={formData.year}
                onChange={handleChange}
                type="number"
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6">
              <InputField
                id="publisher"
                label="Publisher"
                placeholder="Enter publisher's name"
                value={formData.publisher}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6">
              <InputField
                id="genre"
                label="Genre"
                placeholder="Enter genre (e.g., Science)"
                value={formData.genre}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6">
              <InputField
                id="article_title"
                label="Article Title"
                placeholder="Enter article title"
                value={formData.article_title}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6">
              <InputField
                id="article_author"
                label="Article Author"
                placeholder="Enter author's name"
                value={formData.article_author}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-md-6">
              <InputField
                id="article_page_range"
                label="Article Page Range"
                placeholder="Enter page range (e.g., 1-10)"
                value={formData.article_page_range}
                onChange={handleChange}
              />
            </div>
            <div className="col-md-6">
              <div className="mb-3">
                <label htmlFor="document" className="form-label">
                  Upload Document (Image or PDF)
                </label>
                <input
                  type="file"
                  className="form-control"
                  id="document"
                  accept="image/png, image/jpeg, .pdf"
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>
          <button type="submit" className="btn btn-success w-100">
            Upload Article
          </button>
        </form>

        {loading && (
          <div className="text-center mt-3">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p>Processing your document...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
