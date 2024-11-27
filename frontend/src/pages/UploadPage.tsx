import { ChangeEvent, FormEvent, useState } from 'react';
import InputField from '../components/InputField';

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

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { id, value, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [id]: files ? files[0] : value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Uploading data:', formData);
    // Perform an upload operation (e.g., API call)
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
      </div>
    </div>
  );
};

export default UploadPage;
